
variable "account" {
  type        = string
  description = "account (env) ptl/prod"
}

variable "profile" {
  type = string
  description = "aws profile for remote state"
}

variable "workspace" {
  type = string
  description = "terraform workspace required for management remote state"
}

variable "state_bucket" {
  type = string
  description = "terraform state bucket"
}

variable "service_name" {
  type = string
  description = "The name of the apigee environment to deploy to"
}

variable "apigee_environment" {
  type = string
}

variable "namespace" {
  type = string
  description = "String appended to the end of proxy and product names to allow namespaced deploys, for PRs and such"
}
