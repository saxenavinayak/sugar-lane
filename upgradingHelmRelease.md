### Upgrading a helm release

 Typical `helm upgrade` requires the syntax
 `helm upgrade RELEASE_NAME CHART --FLAGS`
In this scenario, RELEASE_NAME is the name of the release of your application, and CHART = repo/chart_name
Flags such as -f (override value.yaml) and --version (override version)
 
 Find the RELEASE_NAME by getting the list of releases
 `helm list -A`
 The NAME column is your RELEASE_NAME
 
 The CHART is a bit tricky
You need the format repo/chart_name
You can get the list of repos available using `helm repo list` (locally installed repos only)

chart_name you can get from original `helm list -A`, where the `CHART` field is of value `chart_name-version`

For instance, 
```sh
(sugar-lane) v6saxena@DESKTOP-K20NK91:~/sugar-lane$ helm list -A 
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                                   APP VERSION
arc             arc-controller  1               2026-05-02 19:47:19.047772093 -0400 EDT deployed        gha-runner-scale-set-controller-0.14.1  0.14.1     
arc-runner      arc-runners     4               2026-05-03 11:40:56.904422206 -0400 EDT deployed        gha-runner-scale-set-0.14.1             0.14.1     
argocd          argocd          4               2026-05-05 17:57:11.614867996 -0400 EDT deployed        argo-cd-9.5.9                           v3.3.8   
```

and
```sh
(sugar-lane) v6saxena@DESKTOP-K20NK91:~/sugar-lane$ helm repo list
NAME                    URL                                               
jetstack                https://charts.jetstack.io                        
prometheus-community    https://prometheus-community.github.io/helm-charts
mojo2600                https://mojo2600.github.io/pihole-kubernetes/     
argo                    https://argoproj.github.io/argo-helm  
```
Our repo here is `argo`, our RELEASE_NAME is `argocd`, our chart is `argo-cd`, and version is `9.5.9`

As such, you can run the command
```sh
 helm upgrade argocd argo/argo-cd --version 9.5.9 --namespace argocd -f values.yaml 
Release "argocd" has been upgraded. Happy Helming!
```