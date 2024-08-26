variable "project_prefix" {
    type = string
    description = "Project prefix used to define several resources names"
}

variable "mlflow_rds_username" {}

variable "mlflow_rds_password" {}

variable "mage_rds_username" {}

variable "mage_rds_password" {}

# ECS

variable "magedb_host" {
  description = "Host for the MageDB"
  type        = string
}

variable "mage_database_connection_url" {
  description = "Database connection URL for Mage"
  type        = string
}

variable "mlflow_host" {
  description = "Host for MLFlow"
  type        = string
}

variable "mlflowdb_dbname" {
  description = "Database Name for MLflow"
  type        = string
}

variable "api_host" {
  description = "Host for the API"
  type        = string
}

variable "openaq_api_key" {
  description = "API key for OpenAQ"
  type        = string
}

variable "magedb_port" {
  description = "Port for MageDB"
  type        = number
}

variable "magedb_name" {
  description = "Name of the MageDB database"
  type        = string
}

variable "magedb_user" {
  description = "Username for MageDB"
  type        = string
}

variable "magedb_password" {
  description = "Password for MageDB"
  type        = string
}

variable "mlflow_tracking_uri" {
  type        = string
}

