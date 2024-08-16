resource "aws_ecs_cluster" "cluster" {
  name = "${var.project_prefix}-ecs-cluster"
}

resource "aws_ecs_task_definition" "mage_ecs_task" {
  family                = "${var.project_prefix}-mage-task"
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  network_mode = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  container_definitions = jsonencode([
    {
      "name"      = "app-container"
      "image"     = "${join("", [var.mage_repository_url, ":latest"])}"
      "cpu"       = 1024
      "memory"    = 2048
      "essential" = true
      "portMappings" = [
        {
          "containerPort" = 6789
          "hostPort"      = 6789
        }
      ]
    }
  ])
}

resource "aws_ecs_task_definition" "mlflow_ecs_task" {
  family                = "${var.project_prefix}-mlflow-task"
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  network_mode = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  container_definitions = jsonencode([
    {
      "name"      = "app-container"
      "image"     = "${join("", [var.mlflow_repository_url, ":latest"])}"
      "cpu"       = 1024
      "memory"    = 2048
      "essential" = true
      "portMappings" = [
        {
          "containerPort" = 5000
          "hostPort"      = 5000
        }
      ]
    }
  ])
}

# Define the ECS Service
resource "aws_ecs_service" "mage_service" {
  name            = "${var.project_prefix}-mage-service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.mage_ecs_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  platform_version = "LATEST"

  network_configuration {
    subnets         = var.public_subnet_ids
    security_groups = [var.mage_ai_sg_id]
    assign_public_ip = true
  }

  lifecycle {
    ignore_changes = [task_definition]
  }
}

resource "aws_ecs_service" "mlflow_service" {
  name            = "${var.project_prefix}-mlflow-service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.mlflow_ecs_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  platform_version = "LATEST"

  network_configuration {
    subnets         = var.public_subnet_ids
    security_groups = [var.mlflow_sg_id]
    assign_public_ip = true
  }

  lifecycle {
    ignore_changes = [task_definition]
  }
}