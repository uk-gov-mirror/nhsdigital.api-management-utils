
data "aws_iam_role" "ecs-execution-role" {
  name = "apis-ecs-x-role-${local.env_service_name}"
}

resource "aws_ecs_task_definition" "service" {
  family                   = local.env_namespaced_name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = {{ service_cpu }}
  memory                   = {{ service_memory }}
  execution_role_arn       = data.aws_iam_role.ecs-execution-role.arn

  container_definitions = jsonencode(
  [
  for container in local.docker_services:
  {
    cpu              = container.cpu
    essential        = container.essential
    image            = container.image
    name             = container.name
    logConfiguration = local.logConfig[container.name]
    portMappings = [
      {
        containerPort = container.port
        hostPort      = container.port
        protocol      = lower(container.protocol)
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

  deployment_maximum_percent         = 200
  deployment_minimum_healthy_percent = 100
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

}

resource "aws_appautoscaling_target" "ecs_target" {
  max_capacity       = 2
  min_capacity       = 0
  resource_id        = "service/apis-${var.apigee_environment}/${aws_ecs_service.service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}
