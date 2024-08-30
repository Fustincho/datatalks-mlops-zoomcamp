resource "aws_cloudwatch_log_group" "ecs_task_log_group" {
  name              = "/ecs/${var.project_prefix}"
  retention_in_days = 7
}
