provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "mlflow_bucket" {
  bucket = "${var.project_prefix}-bucket"  
}

module "vpc" {
  source = "./vpc"

  project_prefix = var.project_prefix  # Pass the variable to the sub-module
}

module "ecr" {
  source = "./ecr"

  project_prefix = var.project_prefix
}

module "ecs" {
  source = "./ecs"

  project_prefix = var.project_prefix
  mlflow_repository_url = module.ecr.mlflow_repository_url
  mage_repository_url = module.ecr.mage_repository_url
  mlflow_bucket_arn = aws_s3_bucket.mlflow_bucket.arn

  public_subnet_ids = module.vpc.public_subnet_ids
  mage_ai_sg_id = aws_security_group.mage_ai_sg.id
  mlflow_sg_id = aws_security_group.mlflow_sg.id
}

module "rds" {
  source = "./rds"
  
  project_prefix = var.project_prefix
  private_subnet_ids = module.vpc.private_subnet_ids

  mlflow_rds_sg_id = aws_security_group.mlflow_rds_sg.id
  mage_ai_rds_sg_id = aws_security_group.mage_ai_rds_sg.id
  
  mlflow_rds_username = var.mlflow_rds_username
  mlflow_rds_password = var.mlflow_rds_password
  mage_rds_username = var.mage_rds_username
  mage_rds_password = var.mage_rds_password
}

terraform {
  backend "s3" {
    bucket         = "fustincho-infra"
    key            = "bucket_test/terraform.tfstate"  # Path to the state file in the bucket
    region         = "us-east-1"                  
    encrypt        = true                             # Optional: Encrypt the state file at rest
  }
}