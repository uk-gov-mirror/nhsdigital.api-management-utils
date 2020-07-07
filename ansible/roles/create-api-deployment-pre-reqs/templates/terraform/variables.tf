
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

variable "service_id" {
  type        = string
}

variable "apigee_environment" {
  type = string
}

variable "apigee_shortenv" {
  type = string
}