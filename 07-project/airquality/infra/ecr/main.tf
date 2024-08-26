resource "aws_ecr_repository" "mlflow_repository" {
  name = "${var.project_prefix}-mlflow"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "mage_repository" {
  name = "${var.project_prefix}-mage"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "api_repository" {
  name = "${var.project_prefix}-api"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}