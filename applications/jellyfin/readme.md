helm install jellyfin jellyfin/jellyfin \
  --namespace jellyfin \
  --create-namespace \
  --values applciations.jellyfin.values.yam




v6saxena@DESKTOP-K20NK91:~/sugar-lane$ helm install jellyfin jellyfin/jellyfin --namespace jellyfin --create-namespace --values applications/jellyfin/values.yaml 
NAME: jellyfin
LAST DEPLOYED: Tue Oct 20 16:57:39 2026
NAMESPACE: jellyfin
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Thank you for installing jellyfin!

Your release is named jellyfin.

To learn more about the release, try:

  $ helm status jellyfin --namespace jellyfin
  $ helm get all jellyfin --namespace jellyfin

Get the Jellyfin URL by running:

  export NODE_PORT=$(kubectl get --namespace jellyfin -o jsonpath="{.spec.ports[0].nodePort}" services jellyfin)
  export NODE_IP=$(kubectl get nodes --namespace jellyfin -o jsonpath="{.items[0].status.addresses[0].address}")
  echo "Jellyfin URL: http://$NODE_IP:$NODE_PORT"

Configuration is persisted to:
  PVC: jellyfin-config

Media is persisted to PVC:
  PVC: jellyfin-media

For more information and documentation:
  Repository: https://github.com/jellyfin/jellyfin-helm
  Jellyfin Docs: https://jellyfin.org/docs/
  $ helm status jellyfin
  $ helm get all jellyfin

To access Jellyfin, you can use port-forwarding:

  $ kubectl port-forward --namespace jellyfin svc/jellyfin 8096:8096

Then visit http://localhost:8096 in your browser.

Network Policy is DISABLED (default).
To enable network isolation, set networkPolicy.enabled=true in your values.
For troubleshooting common issues, see the README:
- inotify instance limit errors
- Hardware acceleration setup
- Network configuration

Useful resources:
  Documentation: https://jellyfin.org/docs/
  Troubleshooting: See README.md in the chart repository

Startup Configuration:
  Startup Probe: Enabled
  Max Startup Time: 300s (5 minutes)

  The startup probe gives Jellyfin enough time to initialize, especially
  with large media libraries. After startup succeeds, liveness and
  readiness probes take over for health monitoring.

Persistence Configuration:
  Config: pvc
  Media: pvc
  Cache: emptyDir
Deployment Configuration:
  Revision History Limit: 3
  You can rollback to any of the last 3 revisions using:
    kubectl rollout undo deployment/jellyfin --namespace jellyfin
v6saxena@DESKTOP-K20NK91:~/sugar-lane$ 