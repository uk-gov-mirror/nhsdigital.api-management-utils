
locals {
  apis_subdomain  = data.terraform_remote_state.account.outputs.apis.apis_subdomain
  namespaced_name = "${var.service_name}${var.namespace == "" ? "" : "-"}${var.namespace}"
  public_alb      = data.terraform_remote_state.account.outputs.apis.alb.public[var.apigee_environment]

}