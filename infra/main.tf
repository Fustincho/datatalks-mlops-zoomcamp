provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "example_bucket" {
  bucket = "fustincho-tf-gha-test"  
}

terraform {
  backend "s3" {
    bucket         = "fustincho-infra"
    key            = "bucket_test/terraform.tfstate"  # Path to the state file in the bucket
    region         = "us-east-1"                  
    encrypt        = true                             # Optional: Encrypt the state file at rest
  }
}