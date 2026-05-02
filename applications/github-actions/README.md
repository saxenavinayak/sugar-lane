

### Github Actions (self hosted runner)
- We need 2 componenets:
    - **Action Runner Controller** : Control plane of setup (kubernetes operator) managing lifecycle of runner pods
    - **Runner Scale Set** : Data plane, creates a long-polling https connection to github (operator runs a "listener" pod whern you deploy it which polls for pending jobs, if found, tells the controller to spin up a job)
Ideally both in separate namesapces



#### Installing Action Runner Controller
- https://docs.github.com/en/actions/tutorials/use-actions-runner-controller/get-started
- Installed in namespace action-runner
```
helm install arc \
    --namespace action-runner \
    --create-namespace \
    oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller
```
- Release name `arc`

- Architecture explanation: https://github.com/actions/actions-runner-controller/blob/master/docs/gha-runner-scale-set-controller/README.md 


#### Installing Runner Scale Set
- Installation_name is: `self_hosted` (used as `runs-on` field on workflows)
- Namesapce: `runner-set`
- Github config url is `https://github.com/saxenavinayak/sugar-lane`
- Github PAT is a token with `repo` and `admin:org` scopes

```
INSTALLATION_NAME="self_hosted"
NAMESPACE="runner-set"
GITHUB_CONFIG_URL="https://github.com/saxenavinayak/sugar-lane"
GITHUB_PAT="XXX"
helm install "${INSTALLATION_NAME}" \
    --namespace "${NAMESPACE}" \
    --create-namespace \
    --set githubConfigUrl="${GITHUB_CONFIG_URL}" \
    --set githubConfigSecret.github_token="${GITHUB_PAT}" \
    oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set

```