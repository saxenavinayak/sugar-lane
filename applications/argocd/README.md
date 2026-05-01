- ArgoCD running in argocd ns (quickstart guide: https://argo-cd.readthedocs.io/en/stable/getting_started/)
### Access
- Copy kubeconfig file from Node, located on `/etc/rancher/k3s/k3s.yaml`
- Paste contents to jumpbox in ~/.kube/k3s.yaml (making sure to update IP to IP assigned to node on LAN)
- Set `export KUBECONFIG=~/.kube/k3s.yaml`
- PF to interface with argoCD
- Default username is admin, default password: `kubectl get secret  argocd-initial-admin-secret --template='{{.data.password | base64d
ecode}}'` (it is stored as a secret in argo-cd namespace)

```
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
- UI available on http://localhost:8080
- To access via CLI, login:  `argocd login 127.0.0.1:8080`


### Revision (Updated 2026-04-30)
- Switched to helm chart
`helm repo add argo https://argoproj.github.io/argo-helm`
`helm install argocd argo/argo-cd --namespace argocd --create-namespace`
`helm upgrade argocd argo/argo-cd -f applications/argocd/values.yaml`
