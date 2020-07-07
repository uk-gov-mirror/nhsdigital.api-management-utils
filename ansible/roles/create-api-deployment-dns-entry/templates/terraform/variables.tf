
variable "account" {
  type        = string
  description = "account (env) ptl/prod"
}

variable "profile" {
  type        = string
  description = "aws profile for remote state"
}

variable "workspace" {
  type        = string
  description = "terraform workspace required for management remote state"
}

variable "state_bucket" {
  type        = string
  description = "terraform state bucket"
}

variable "namespaced_name" {
  type        = string
}

variable "apigee_environment" {
  type = string
}

variable "namespace" {
  type        = string
  description = "String appended to the end of proxy and product names to allow namespaced deploys, for PRs and such"
}