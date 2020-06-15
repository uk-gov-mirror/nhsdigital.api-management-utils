

resource "aws_alb_target_group" "service" {
  name        = local.env_namespaced_name
  port        = local.exposed_service.port
  protocol    = local.exposed_service.lb_protocol
  vpc_id      = data.terraform_remote_state.pre-reqs.outputs.vpc_id
  target_type = "ip"

  health_check {
    matcher = local.exposed_service.health_check.matcher
    path    = local.exposed_service.health_check.path
  }

  tags = local.common_tags
}

resource "aws_lb_listener_rule" "service" {
  listener_arn = data.terraform_remote_state.pre-reqs.outputs.public_alb_listener_arn

  action {
    order            = 1
    target_group_arn = aws_alb_target_group.service.arn
    type             = "forward"
  }

  condition {
    host_header {
      values = [
        "${local.namespaced_name}.*"
      ]
    }
  }

}