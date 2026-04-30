### Deployed using helm chart 
https://github.com/MoJo2600/pihole-kubernetes

#### Install
`helm install pihole mojo2600/pihole -f applications/pihole/values.yaml -n default`

#### Upgrade
`helm upgrade pihole mojo2600/pihole -f applications/pihole/values.yaml`
