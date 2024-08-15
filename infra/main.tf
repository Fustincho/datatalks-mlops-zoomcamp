provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "example_bucket" {
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

terraform {
  backend "s3" {
    bucket         = "fustincho-infra"
    key            = "bucket_test/terraform.tfstate"  # Path to the state file in the bucket
    region         = "us-east-1"                  
    encrypt        = true                             # Optional: Encrypt the state file at rest
  }
}