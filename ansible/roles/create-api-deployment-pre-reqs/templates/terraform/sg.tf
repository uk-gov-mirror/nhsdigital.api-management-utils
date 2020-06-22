
resource "aws_security_group" "api-deployment" {

  vpc_id      = data.terraform_remote_state.account.outputs.account_vpc.id
  name        = "api-${local.env_service_name}"
  description = "api-${local.env_service_name} specific rules"

  tags = {
    Name   = "api-${local.env_service_name}"
    source = "terraform"
  }
}
