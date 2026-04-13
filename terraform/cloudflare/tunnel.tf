
resource "cloudflare_zero_trust_tunnel_cloudflared" "home_lab" {
  account_id = var.cloudflare_account_id
  name       = "sugar-home-lab"
  secret     = "some-secret"
  lifecycle {
    ignore_changes = [secret]
  }
}

resource "cloudflare_record" "example" {
  zone_id = var.cloudflare_zone_id # This comes from your domain, vinayaksaxena.uk
  name    = "vinayaksaxena.uk" # @ is used for root domain vinayaksaxena.uk
  value   = "${cloudflare_zero_trust_tunnel_cloudflared.home_lab.id}.cfargotunnel.com"
  type    = "CNAME"
  proxied = true
}

resource "cloudflare_zero_trust_tunnel_cloudflared_config" "homelab_config" {
  account_id = var.cloudflare_account_id
  tunnel_id  = cloudflare_zero_trust_tunnel_cloudflared.home_lab.id
  

  config {
    ingress_rule {
      hostname = "vinayaksaxena.uk"
      service  = "http://ingress-nginx-controller.ingress-nginx.svc.cluster.local"
    }
    # Catch-all rule (Required)
    ingress_rule {
      service  = "http_status:404"
    }
  }
}