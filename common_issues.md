### DNS Resolution
After a network change (ie ISP or a DNS), the core-dns deployment is probably stale -> core-dns takes a snapshot of /etc/resolv.conf at the time of the deployment - to refresh it, delete the core-dns pod and have it reschedule it, the core-dns deployment will then pick up the latest /etc/resolv.conf on your host
dns-utils is a good node to test your changes 