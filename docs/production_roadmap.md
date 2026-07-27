# Production-Style Homelab Roadmap (SLOP GUARANTEED)

This repo already models a useful production-like platform: k3s, Argo CD, self-hosted GitHub Actions runners, Cloudflare Tunnel, Terraform-managed Cloudflare resources, Prometheus/Grafana, persistent workloads, and custom services.

The next improvements should focus on making the cluster more repeatable, observable, secure, and resilient. These are also the areas that translate best into resume and interview material.

## Highest Priority

### 1. GitOps Application Model

Move from mostly app-level manifests and manual notes toward first-class Argo CD resources stored in Git.

Ideas:
- Add Argo CD `Application` manifests for each app.
- Consider `ApplicationSet` if environments or app patterns grow.
- Use sync policies such as auto-sync, prune, and self-heal where appropriate.
- Add sync waves for dependencies like databases, Redis, ingress, and applications.
- Keep each app's namespace, manifests, values, and Argo config together.

Resume framing:
- Managed Kubernetes workloads through declarative GitOps using Argo CD.
- Designed repeatable deployment flows for stateful and stateless services.

### 2. Secrets Management

The repo references Kubernetes Secrets, but secrets are not yet managed through a repeatable Git-friendly workflow.

Options:
- External Secrets Operator with a backend such as 1Password, Vault, Bitwarden, or another secret store.
- SOPS with age-encrypted secret files committed to Git.
- Sealed Secrets for encrypted Kubernetes Secret manifests.

Good target outcome:
- No manual secret creation required after rebuilding the cluster.
- Secret ownership and rotation are documented.
- Argo CD can reconcile secret-backed workloads without ad hoc setup.

Resume framing:
- Implemented GitOps-compatible secrets management for Kubernetes workloads.

### 3. CI Validation Before Deploy

The current deploy flow syncs Argo CD from GitHub Actions. Add validation jobs before allowing deploys.

Checks to add:
- `yamllint` for YAML quality.
- `kubeconform` for Kubernetes schema validation.
- `terraform fmt`, `terraform validate`, and eventually `terraform plan`.
- `trivy config` for Kubernetes and Terraform misconfiguration scanning.
- Docker image vulnerability scanning for custom services.
- Helm chart linting where Helm is used.

Good target outcome:
- Bad manifests fail in CI before Argo CD tries to sync them.
- Infrastructure changes are validated before they reach the cluster.

Resume framing:
- Built CI quality gates for Kubernetes and Terraform using schema validation and security scanning.

### 4. Baseline Kubernetes Hardening

Standardize production basics across workloads.

Add where practical:
- `resources.requests` and `resources.limits`
- `readinessProbe`
- `livenessProbe`
- `securityContext`
- `runAsNonRoot`
- `readOnlyRootFilesystem`
- dropped Linux capabilities
- `PodDisruptionBudget` for important services

Current candidates:
- `applications/switches/deployments/deployment.yaml`
- `applications/tracker/tracker.yaml`
- `applications/tracker/pgStatefulSet.yaml`
- `applications/cloudflared/deployment.yaml`
- `applications/plex/deployment.yaml`

Resume framing:
- Hardened Kubernetes workloads with health checks, resource controls, and restricted container security contexts.

## Security and Policy

### 5. Policy-as-Code

Add Kyverno or OPA Gatekeeper to enforce platform rules.

Useful policies:
- Block `latest` image tags.
- Require resource requests and limits.
- Require liveness/readiness probes.
- Require non-root containers.
- Block privileged containers.
- Require explicit namespaces.
- Restrict hostPath usage.

Good target outcome:
- The cluster rejects manifests that do not meet baseline production standards.
- CI can run the same policies before merge.

Resume framing:
- Implemented Kubernetes policy-as-code guardrails with Kyverno/OPA.

### 6. Network Policies

Add Kubernetes `NetworkPolicy` resources to reduce lateral movement.

Policy model:
- Default deny per namespace.
- Allow ingress only from the ingress controller where needed.
- Allow apps to talk only to their required databases and Redis.
- Allow Prometheus to scrape metrics endpoints.
- Keep LAN-only services isolated from public Cloudflare-exposed services.

Resume framing:
- Designed namespace-level Kubernetes network segmentation for internal and externally exposed services.

### 7. Image and Dependency Hygiene

Avoid mutable image tags and add automated update workflows.

Ideas:
- Replace `latest` tags with pinned versions.
- Consider digest pinning for critical infrastructure.
- Add Renovate or Dependabot for Helm charts, Docker images, Terraform providers, and Python dependencies.
- Track update PRs rather than making unreviewed changes directly.

Current candidates:
- `cloudflare/cloudflared:latest`
- `plexinc/pms-docker:latest`
- `ghcr.io/actions/actions-runner:latest`

Resume framing:
- Automated dependency and container image update workflows with controlled review gates.

## Reliability and Recovery

### 8. Backups and Disaster Recovery

Stateful workloads should have tested backup and restore flows.

Add:
- Velero for Kubernetes resource backups.
- Scheduled Postgres backups for Tracker and Immich/CNPG.
- Volume snapshots if supported by the storage layer.
- Restore runbooks in `docs/`.
- A periodic restore test checklist.

Good target outcome:
- Rebuild the cluster from Git plus backups.
- Prove at least one database can be restored into a clean environment.

Resume framing:
- Implemented backup and disaster recovery strategy for stateful Kubernetes workloads.

### 9. High Availability Path

The cluster is currently single-node, which is reasonable for a homelab. A future production-style milestone would be a multi-node setup.

Ideas:
- Add one or two worker nodes.
- Move local storage toward a replicated storage option if feasible.
- Add topology spread constraints.
- Add PodDisruptionBudgets.
- Document expected behavior during node failure.

Resume framing:
- Evolved a single-node k3s homelab into a multi-node Kubernetes platform with workload availability controls.

## Observability

### 10. Alerting

Prometheus and Grafana are already present. Add alerting so the system can page or notify on real failures.

Ideas:
- Configure Alertmanager routes to Discord, Slack, email, or another notification channel.
- Alert on pod crash loops, persistent volume pressure, node pressure, and failed Prometheus scrapes.
- Add service-specific alerts for Immich, Tracker, Pi-hole, and Cloudflare Tunnel.

Resume framing:
- Built Prometheus alerting for Kubernetes infrastructure and application health.

### 11. Logs

Add a central logging stack.

Options:
- Loki with Promtail or Grafana Alloy.
- Retain logs for a short but useful window.
- Add dashboards linking metrics and logs.

Resume framing:
- Added centralized log aggregation for Kubernetes workloads using Loki and Grafana.

### 12. Synthetic Monitoring and SLOs

Add blackbox-style checks for user-visible endpoints.

Ideas:
- Use blackbox-exporter to check public Cloudflare-routed services.
- Track uptime, latency, and HTTP status.
- Create simple SLO dashboards for exposed services.

Resume framing:
- Created SLO-style dashboards for externally exposed services using Prometheus and Grafana.

## Networking

### 13. Gateway API Migration

The README already notes that NGINX ingress may eventually be replaced. Gateway API would be a strong production-style upgrade.

Ideas:
- Introduce Gateway API resources.
- Replace selected `Ingress` resources with `HTTPRoute`.
- Keep Cloudflare Tunnel as the public entrypoint.
- Document the migration path and behavior changes.

Resume framing:
- Migrated Kubernetes ingress routing from legacy Ingress resources to Gateway API.

### 14. Cloudflare Zero Trust Enhancements

Cloudflare Tunnel is already in use. Add more Zero Trust controls around public apps.

Ideas:
- Cloudflare Access policies for admin-only services.
- mTLS or identity-aware access for sensitive routes.
- Terraform-managed access applications and policies.
- Separate public, private, and admin hostnames.

Resume framing:
- Secured externally exposed homelab services with Cloudflare Zero Trust and Terraform-managed access policies.

## Suggested First Sprint

Start with changes that are low-risk but high-signal:

1. Add CI validation with `yamllint`, `kubeconform`, `terraform validate`, and `trivy config`.
2. Add probes, resource requests/limits, and security contexts to custom app workloads.
3. Replace mutable `latest` image tags with pinned versions.
4. Add SOPS or External Secrets Operator for repeatable secret management.
5. Add Kyverno policies for resource limits, probes, non-root containers, and blocked `latest` tags.
6. Add Alertmanager routing and a small set of real alerts.
7. Document and test one Postgres restore flow.

## Project Themes for Resume

These are the strongest ways to describe the work after implementation:

- Production-style GitOps platform on Kubernetes with Argo CD and GitHub Actions.
- Secure Kubernetes baseline with policy-as-code, network segmentation, and secret management.
- Stateful workload reliability with PostgreSQL backups, restore testing, and persistent storage.
- Observability platform with metrics, logs, alerts, and synthetic uptime checks.
- Private CI/CD platform using self-hosted ephemeral GitHub Actions runners inside Kubernetes.

