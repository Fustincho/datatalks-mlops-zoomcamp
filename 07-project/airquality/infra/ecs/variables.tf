variable "project_prefix" {
  description = "Project prefix used to define several resource names"
  type        = string
}

variable "mage_repository_url" {
  type        = string
}

variable "mlflow_repository_url" {
  type        = string
}

variable "mlflow_bucket_arn" {}

variable "public_subnet_ids" {}

variable "mage_ai_sg_id" {}

variable "mlflow_sg_id" {}

variable "secret_arn" {
  description = "ARN of the Secrets Manager secret"
  type        = string
}