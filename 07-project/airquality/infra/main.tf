provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "mlflow_bucket" {
  bucket = "${var.project_prefix}-bucket"  
}

module "sm" {
  source = "./sm"

  project_prefix               = var.project_prefix
  magedb_host                  = var.magedb_host
  mage_database_connection_url = var.mage_database_connection_url
  mlflow_host                  = var.mlflow_host
  api_host                     = var.api_host
  openaq_api_key               = var.openaq_api_key
  magedb_port                  = var.magedb_port
  magedb_name                  = var.magedb_name
  magedb_user                  = var.magedb_user
  magedb_password              = var.magedb_password
  s3_bucket_name               = aws_s3_bucket.mlflow_bucket.bucket
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
  api_repository_url = module.ecr.api_repository_url
  mlflow_repository_url = module.ecr.mlflow_repository_url
  mage_repository_url = module.ecr.mage_repository_url
  mlflow_bucket_arn = aws_s3_bucket.mlflow_bucket.arn

  public_subnet_ids = module.vpc.public_subnet_ids
  mage_ai_sg_id = aws_security_group.mage_ai_sg.id
  mlflow_sg_id = aws_security_group.mlflow_sg.id
  api_sg_id = aws_security_group.api_sg.id

  secret_arn = module.sm.secret_arn
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
    # These values will be overridden by the -backend-config flags
    bucket = "dummy"
    key    = "dummy"  # Path to the state file in the bucket
    region = "dummy"
    encrypt = "dummy" # Optional: Encrypt the state file at rest
  }
}