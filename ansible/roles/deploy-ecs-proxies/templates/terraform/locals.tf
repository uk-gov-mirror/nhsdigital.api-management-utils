data "aws_caller_identity" "current" {}
data "aws_region" "current" {}



locals {
  account_id = data.aws_caller_identity.current.account_id
  region = data.aws_region.current.name
  namespaced_name = "${var.service_name}${var.namespace == "" ? "" : "-"}${var.namespace}"
  env_namespaced_name = "${var.apigee_environment}-${local.namespaced_name}"

  common_tags = {
    source = "terraform"
    api-service = var.service_name
    api-environment = var.apigee_environment
    api-namespaced-name = local.namespaced_name
    api-is-namespaced = var.namespace == "" ? false : true
  }

  logConfig = {
  for container in local.docker_services:
  container.name => {
    logDriver = "splunk"
    options = {
      splunk-format = "json"
      splunk-index = "requests_apm_${var.account}"
      splunk-sourcetype = "apm-json-docker"
      splunk-source = "apm:ecs:${var.workspace}:${container.name}"
    },
    secretOptions= [
      {
        name = "splunk-url"
        valueFrom = "/${var.account}/platform-common/splunk/hec_url"
      },
      {
        name = "splunk-token"
        valueFrom = "/${var.account}/platform-common/splunk/hec_token"
      }
    ]
  }

  }

  docker_services = [
  {% for service in docker_containers %}
    {{
        (
          (container_defaults | combine(service))
          | combine(
            {'image': '${local.account_id}.dkr.ecr.eu-west-2.amazonaws.com/' + service.name + ':' + build_label }
          )
        ) | to_json
    }},
  {% endfor %}
  ]

  exposed_service = element(matchkeys(local.docker_services, local.docker_services.*.expose, list(true)), 0)

}