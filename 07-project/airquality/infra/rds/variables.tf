variable "private_subnet_ids" {}

variable "project_prefix" {
  description = "Project prefix used to define several resource names"
  type        = string
}

variable "mlflow_rds_username" {}

variable "mlflow_rds_password" {}

variable "mage_rds_username" {}

variable "mage_rds_password" {}

variable "mlflow_rds_sg_id" {
  description = "Security group ID for MLflow RDS instance"
  type        = string
}

variable "mage_ai_rds_sg_id" {
  description = "Security group ID for Mage AI RDS instance"
  type        = string
}
