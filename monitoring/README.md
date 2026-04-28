## Deployment
`helm install kube-prom-stack  oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack -f monitoring/prometheus.yaml -n monitoring --create-namespace`

## Upgrade
`helm upgrade kube-prom-stack prometheus-community/kube-prometheus-stack -f monitoring/prometheus.yaml`

### To PF Grafana locally
`export POD_NAME=$(kubectl --namespace monitoring get pod -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=kube-prom-stack" -oname)`

`kubectl --namespace monitoring port-forward $POD_NAME 3000`

Default username is `admin`, password you can grab by `kubectl --namespace monitoring get secrets kube-prom-stack-grafana -o jsonpath="{.data.admin-password}" | base64 -d ; echo`
