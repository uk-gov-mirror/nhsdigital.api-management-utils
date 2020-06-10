
data "aws_iam_role" "ecs-execution-role" {
  name = "apis-ecs-execution-role-${local.env_namespaced_name}"
}

resource "aws_ecs_task_definition" "service" {
  family                   = local.env_namespaced_name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 512
  memory                   = 2048
  execution_role_arn       = data.aws_iam_role.ecs-execution-role.arn

  container_definitions = jsonencode(
  [
  for container in local.docker_services:
  {
    cpu              = 0
    essential        = true
    image            = container.image
    name             = container.name
    logConfiguration = local.logConfig[container.name]
    portMappings = [
      {
        protocol      = "tcp"
        containerPort = container.port
        hostPort      = container.port
      }
    ]
    mountPoints = []
    volumesFrom = []
    environment = container.environment
    secrets     = container.secrets
  }
  ]
  )

  tags = local.common_tags

}



resource "aws_ecs_service" "service" {
  platform_version = "1.4.0"
  name             = local.namespaced_name
  cluster          = data.terraform_remote_state.pre-reqs.outputs.ecs_cluster_id
  task_definition  = aws_ecs_task_definition.service.arn


  desired_count = 1
  launch_type   = "FARGATE"

  deployment_maximum_percent         = 100
  deployment_minimum_healthy_percent = 0
  force_new_deployment               = true


  network_configuration {
    security_groups = [data.terraform_remote_state.pre-reqs.outputs.ecs_sg_id]
    subnets         = data.terraform_remote_state.pre-reqs.outputs.subnet_ids
  }

  health_check_grace_period_seconds = 45

  load_balancer {
    target_group_arn = aws_alb_target_group.service.arn
    container_name   = local.exposed_service.name
    container_port   = local.exposed_service.port
  }

  depends_on = [
    aws_lb_listener_rule.service
  ]

  tags = local.common_tags
}