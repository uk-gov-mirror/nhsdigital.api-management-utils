
variable "profile" {
  type = string
}

terraform {
  backend "s3" {
    key     = "route53/terraform.tfstate"
    region  = "eu-west-2"
    encrypt = true
    dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region  = "eu-west-2"
  version = "~> 2.33"
  profile = var.profile
}


