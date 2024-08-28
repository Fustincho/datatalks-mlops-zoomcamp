resource "aws_ecs_cluster" "cluster" {
  name = "${var.project_prefix}-ecs-cluster"
}

resource "aws_ecs_task_definition" "mage_ecs_task" {
  family                = "${var.project_prefix}-mage-task"
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  network_mode = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "2048"
  memory                   = "8192"
  container_definitions = jsonencode([
    {
      "name"      = "app-container"
      "image"     = "${join("", [var.mage_repository_url, ":latest"])}"
      "cpu"       = 2048
      "memory"    = 8192
      "essential" = true
      "portMappings" = [
        {
          "containerPort" = 6789
          "hostPort"      = 6789
        }
      ]
      secrets = [
        {
          name      = "API_HOST"
          valueFrom = "${var.secret_arn}:API_HOST::"
        },
        {
          name      = "MAGEDB_HOST"
          valueFrom = "${var.secret_arn}:MAGEDB_HOST::"
        },
        {
          name      = "MAGEDB_NAME"
          valueFrom = "${var.secret_arn}:MAGEDB_NAME::"
        },
        {
          name      = "MAGEDB_PASSWORD"
          valueFrom = "${var.secret_arn}:MAGEDB_PASSWORD::"
        },
        {
          name      = "MAGEDB_PORT"
          valueFrom = "${var.secret_arn}:MAGEDB_PORT::"
        },
        {
          name      = "MAGEDB_USER"
          valueFrom = "${var.secret_arn}:MAGEDB_USER::"
        },
        {
          name      = "MAGE_DATABASE_CONNECTION_URL"
          valueFrom = "${var.secret_arn}:MAGE_DATABASE_CONNECTION_URL::"
        },
        {
          name      = "MLFLOW_HOST"
          valueFrom = "${var.secret_arn}:MLFLOW_HOST::"
        },
        {
          name      = "OPENAQ_API_KEY"
          valueFrom = "${var.secret_arn}:OPENAQ_API_KEY::"
        },
        {
          name      = "S3_BUCKET_NAME"
          valueFrom = "${var.secret_arn}:S3_BUCKET_NAME::"
        },
        {
          name      = "MLFLOW_TRACKING_URI"
          valueFrom = "${var.secret_arn}:MLFLOW_TRACKING_URI::"
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
      secrets = [
        {
          name      = "MLFLOWDB_USER"
          valueFrom = "${var.secret_arn}:MLFLOWDB_USER::"
        },
        {
          name      = "MLFLOWDB_PASSWORD"
          valueFrom = "${var.secret_arn}:MLFLOWDB_PASSWORD::"
        },
        {
          name      = "MLFLOWDB_ENDPOINT"
          valueFrom = "${var.secret_arn}:MLFLOWDB_ENDPOINT::"
        },
        {
          name      = "MLFLOWDB_DBNAME"
          valueFrom = "${var.secret_arn}:MLFLOWDB_DBNAME::"
        },
        {
          name      = "MLFLOW_ARTIFACT_ROOT"
          valueFrom = "${var.secret_arn}:MLFLOW_ARTIFACT_ROOT::"
        }
      ]
    }
  ])
}

resource "aws_ecs_task_definition" "api_ecs_task" {
  family                = "${var.project_prefix}-api-task"
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  network_mode = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  container_definitions = jsonencode([
    {
      "name"      = "app-container"
      "image"     = "${join("", [var.api_repository_url, ":latest"])}"
      "cpu"       = 1024
      "memory"    = 2048
      "essential" = true
      "portMappings" = [
        {
          "containerPort" = 8000
          "hostPort"      = 8000
        }
      ]
      secrets = [
        {
          name      = "MLFLOW_TRACKING_URI"
          valueFrom = "${var.secret_arn}:MLFLOW_TRACKING_URI::"
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

resource "aws_ecs_service" "api_service" {
  name            = "${var.project_prefix}-api-service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.api_ecs_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  platform_version = "LATEST"

  network_configuration {
    subnets         = var.public_subnet_ids
    security_groups = [var.api_sg_id]
    assign_public_ip = true
  }

  lifecycle {
    ignore_changes = [task_definition]
  }
}