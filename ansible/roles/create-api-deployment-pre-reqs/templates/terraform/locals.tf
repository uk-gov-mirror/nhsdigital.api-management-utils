data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
  account_id     = data.aws_caller_identity.current.account_id
  region         = data.aws_region.current.name
  aws_ecr_bucket = "prod-eu-west-2-starport-layer-bucket"

  env_service_id       = "${var.apigee_environment}-${var.service_id}"
  service_namespaces     = var.apigee_environment == "internal-dev" ? [var.service_id, "${var.service_id}-*"] : [var.service_id]
  env_service_namespaces = [for ns in local.service_namespaces : "${var.apigee_environment}-${ns}"]
  short_env_service_namespaces = [for ns in local.service_namespaces : "${var.apigee_shortenv}-${ns}"]
  workspaces             = var.apigee_environment == "internal-dev" ? [var.workspace, "${var.workspace}:*"] : [var.workspace]


  public_alb_listener = data.terraform_remote_state.account.outputs.apis.alb-listener.public[var.apigee_environment]
  public_alb          = data.terraform_remote_state.account.outputs.apis.alb.public[var.apigee_environment]
  ecs_cluster         = data.terraform_remote_state.account.outputs.apis.ecs_clusters[var.apigee_environment]
  apis_subdomain      = data.terraform_remote_state.account.outputs.apis.apis_subdomain


}
