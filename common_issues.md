### DNS Resolution
After a network change (ie ISP or a DNS), the core-dns deployment is probably stale -> core-dns takes a snapshot of /etc/resolv.conf at the time of the deployment - to refresh it, delete the core-dns pod and have it reschedule it, the core-dns deployment will then pick up the latest /etc/resolv.conf on your host
dns-utils is a good service to test your changes 

###
By default, the local path provisioner can only assign PVCs on the node to a specific path, by default `/var/lib/rancher/k3s/storage`. You can add an additional entry to the CM for local-storage, by default located in `/var/lib/rancher/k3s/server/manifests/local-storage` -> For example, add an entry to `data.config.json.nodePathMap`
```
"node": "homelab"
"paths": ["/media/chungus/"]
```
Then, if you have a `storageClass` object defined in your cluster with the path `/media/chungus`, the provisioner will be able to assign PVCs to this path.
(Make sure to apply the above manifest and do a rollout start `kubectl rollout restart deployment local-path-provisioner -n kube-system`)