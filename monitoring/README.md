## Deployment
`helm install kube-prom-stack  oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack -f monitoring/prometheus.yaml -n monitoring --create-namespace`