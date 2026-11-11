### Deployed using helm chart 
https://github.com/MoJo2600/pihole-kubernetes

#### Install
`helm install pihole mojo2600/pihole -f applications/pihole/values.yaml -n default`

#### Upgrade
`helm upgrade pihole mojo2600/pihole -f applications/pihole/values.yaml`


#### Pihole upgrade incident 2026-11-11
- Doing a helm rollout of pihole fucked with the node being able to pull images
- The node was set to be using 127.0.0.53 as the DNS to pull images from
- but k3s had set a rule such that traffic sent to 127.0.0.53 was sent to the pihole.
- But when helm rollout happened, k3s could not pull the new image as pihole pod is shut down
- This created a circular dependency: pihole needed itself to be up to pull an image
-  pointed /etc/resolv.conf to /run/systemd/resolve/resolv.conf, with external DNS servers configured. This bypassed the local port-53 redirection, allowing image pulls and services to recover

For future, we need ot make the hosts DNS independent of pihole
