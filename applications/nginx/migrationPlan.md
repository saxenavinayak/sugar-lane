I inspected the cluster using read-only commands. I recommend migrating to Gateway API using the Traefik installation you already have, keeping NGINX running until each application works through Traefik. No files or cluster resources were changed.

What I found:

| Component | Current state |
|---|---|
| Cluster | One node, K3s v1.34.4+k3s1 |
| NGINX | Two controller replicas, version v1.9.6 |
| Traefik | Already running, version 3.6.7 |
| Gateway API | Standard-channel v1.4.0 CRDs already installed |
| Gateway resources | No GatewayClasses, Gateways or HTTPRoutes |
| Traefik Gateway provider | Disabled |
| Traefik external exposure | LoadBalancer pending because the node’s required host ports are occupied |
| Application ownership | Tracker/Immich use Argo CD; Pi-hole/Jellyfin use Helm |

The intended result is:

Cloudflare Tunnel ──> Traefik Service ──> Traefik ──> application
                                           ↑
                                 Gateway + HTTPRoute

Below, each step describes work for you to perform later.

1. Record the current behavior and rollback destination

What to do: Before changing anything, record how you access each application and verify that its current path works.

| Hostname | Backend Service | Access path to verify |
|---|---|---|
| vinayaksaxena.uk | default/tracker-public-for-cloudflare:80 | Cloudflare Tunnel |
| immich.vinayaksaxena.uk | default/immich-server:2283 | Cloudflare Tunnel |
| blocker.com | default/pihole-web:80 | Confirm your LAN DNS/access method |
| jellyfin.com | jellyfin/jellyfin:8096 | Confirm your LAN DNS/access method |

Record the current tunnel origin:

http://ingress-nginx-controller.ingress-nginx.svc.cluster.local

For Immich, establish that uploads, downloads and playback work before migration.

Why: You need a baseline to distinguish a migration regression from an existing problem. The original tunnel origin is also your rollback destination.

2. Decide how configuration will be managed

What to do: Plan to manage Traefik through K3s’s HelmChartConfig, routes through your application configuration, and tunnel origins through Terraform.

Keep existing Ingress objects while adding new HTTPRoutes. For Helm applications, leave their Ingress enabled during testing.

Why: Editing a generated Deployment directly is temporary: K3s or Helm can overwrite it. Likewise, deleting an Argo CD or Helm-managed Ingress without changing its source can cause it to reappear.

K3s explicitly recommends HelmChartConfig for customizing its packaged Traefik installation. K3s configuration guidance.

3. Enable Traefik’s Gateway API provider

What to do: In the configuration for the existing Traefik chart, enable:

providers:
  kubernetesGateway:
    enabled: true

Check the installed chart’s values before applying it, including whether it automatically creates a GatewayClass or default Gateway.

Your Gateway API CRDs already exist and are owned by the traefik-crd Helm release. Keep that ownership intact rather than installing a second CRD bundle.

Why: CRDs let Kubernetes store Gateway objects. The provider makes Traefik watch those objects and turn them into working proxy configuration. Those are separate capabilities.

K3s documents this provider setting and Gateway API v1.4 support. K3s Gateway API guidance.

Checkpoint: Traefik remains healthy, and its startup arguments/logs show the Kubernetes Gateway provider enabled.

4. Give Traefik an internal Service for parallel testing

What to do: Configure Traefik’s Service as ClusterIP while you test alongside NGINX.

Your installed chart is version 38; inspect its values for the correct Service-type setting. Current chart v40 documentation uses a different values path, so avoid copying that setting blindly.

Why: NGINX currently occupies the node’s external ports. Traefik’s pending ServiceLB pod explicitly reports unavailable host ports. An internal Service lets both proxies run concurrently without competing for ports 80/443.

cloudflared can reach a ClusterIP Service from inside the cluster.

Checkpoint: The Traefik Service has ready endpoints. It does not need an external IP for this test path.

5. Create one shared Gateway

What to do: Use one Gateway—for example, homelab in a dedicated networking namespace—with:

- A GatewayClass managed by Traefik.
- An HTTP listener compatible with Traefik’s configured entry point.
- Permission for HTTPRoutes from selected application namespaces to attach.

For Traefik, confirm how the Gateway listener port maps to its entry point. Your current web entry point listens inside the container on 8000, while the Service exposes 80.

Label default and jellyfin as eligible namespaces and use an allowedRoutes namespace selector.

Why: One Gateway teaches shared infrastructure without creating a separate entry point for every application. Explicit namespace permissions demonstrate Gateway API’s attachment model.

Route-to-Gateway attachment uses parentRefs and allowedRoutes; it does not require a ReferenceGrant. Keeping each route beside its backend Service also avoids cross-namespace backend references. Cross-namespace routing guide.

Checkpoint: The GatewayClass is accepted and the Gateway/listener reports successful programming. Read condition messages if it does not.

6. Migrate Tracker’s configuration first

What to do: Adapt the generated Tracker HTTPRoute so it:

- Lives in default.
- References networking/homelab.
- Matches vinayaksaxena.uk.
- Routes / to tracker-public-for-cloudflare:80.

Remove the generated status section from the configuration you eventually manage; controllers populate status.

Why: Tracker has straightforward routing and no NGINX annotations. It isolates the basic concepts before you tackle Immich.

Inspect it using:

kubectl -n default describe httproute <tracker-route-name>

Checkpoint: Its parent status reports Accepted=True and ResolvedRefs=True.

7. Test Tracker without changing public traffic

What to do: Forward a local port to Traefik:

kubectl -n kube-system port-forward service/traefik 8088:80

In another terminal:

curl -i -H 'Host: vinayaksaxena.uk' http://127.0.0.1:8088/

Compare the response with the application through NGINX. Test an unmatched hostname too.

Why: The HTTP Host header selects your route. Visiting localhost without the hostname would test a different routing case.

This validates Traefik → backend connectivity while public requests continue using NGINX. It does not yet test Cloudflare headers or the tunnel.

8. Resolve Immich’s settings before switching it

What to do: Add Immich’s HTTPRoute, then deliberately review:

| Existing behavior | Migration task |
|---|---|
| Unlimited request body size | Check Traefik and middleware limits; test large uploads |
| Response buffering disabled | Verify streaming behavior; avoid adding full-body buffering inadvertently |
| Read/send timeouts | Configure appropriate Traefik timeout behavior |
| Forwarded headers enabled | Configure trusted proxy handling and check application URL generation |

I confirmed the live NGINX annotations are 610 seconds read and 600 seconds send. The converter’s 6,100-second request timeout is not a faithful numerical copy. Do not retain it without understanding why it was generated.

Why: NGINX inactivity timeouts and a whole-request timeout measure different things. A successful homepage request says little about a slow video upload.

Test large uploads, slow uploads, downloads, playback and any WebSocket functionality. Confirm the chosen Traefik version actually supports each HTTPRoute field you use; accepting YAML is not proof that every optional behavior is implemented.

9. Switch the public hostnames individually

What to do: Change only Tracker’s tunnel origin first, from the NGINX Service to:

http://traefik.kube-system.svc.cluster.local:80

Preserve the original hostname reaching Traefik. Validate public HTTPS, login, redirects and application behavior. Then repeat for Immich.

Why: This tests the complete path, including forwarded scheme/client headers. DNS and the tunnel identity can remain unchanged.

Rollback: Restore that hostname’s original NGINX origin. Leave the old Ingress and controller available during the observation period.

10. Migrate LAN access separately

What to do: Create Pi-hole and Jellyfin routes in their existing namespaces. Decide how LAN clients will reach Traefik:

- A NodePort during testing.
- Eventually a LoadBalancer using the node’s ports after NGINX releases them.
- Another deliberate LAN exposure method.

If clients currently resolve those hostnames to 192.168.68.78 and use normal ports 80/443, plan that handover explicitly. Configure a certificate and HTTPS listener if direct LAN HTTPS is required.

Why: Cloudflare can reach ClusterIP internally; ordinary LAN clients generally cannot. Public tunnel migration does not automatically migrate LAN entry points.

Pi-hole DNS on port 53 is independent of its web route.

11. Remove NGINX through its source configuration

What to do: After every required access path works:

- Disable Pi-hole/Jellyfin’s generated Ingress resources in Helm values.
- Replace Tracker/Immich Ingress definitions in their Argo CD sources.
- Remove the K3s-managed ingress-nginx HelmChart through its provisioning source.
- Check that no tunnel origin or LAN client still depends on NGINX.
- Review the existing Argo CD Ingress-health override.
- Verify the setup survives reconciliation and a planned restart.

Why: Completion means the system can recreate the new configuration reliably, including after an upgrade or reboot.

One cluster-specific detail: your K3s version predates a fix concerning removal of Gateway API CRDs when packaged Traefik is disabled. Keep traefik-crd in place during this migration, and treat any later Traefik removal as a separate operation. K3s version-specific guidance.