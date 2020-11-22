//resource "aws_route53_record" "service" {
//  name    = "${var.namespaced_name}.${var.apigee_environment}.${local.apis_subdomain}"
//  zone_id = data.terraform_remote_state.account.outputs.dns.public.zone_id
//
//  type = "A"
//
//  alias {
//    evaluate_target_health = true
//    name                   = local.public_alb.dns_name
//    zone_id                = local.public_alb.zone_id
//  }
//
//}