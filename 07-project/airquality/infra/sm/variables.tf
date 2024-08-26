variable "project_prefix" {
    type = string
    description = "Project prefix used to define several resources names"
}

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

variable "mlflow_tracking_uri" {
  description = "Host for MLFlow"
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

variable "s3_bucket_name" {
  description = "S3 bucket name for MLFlow"
  type        = string
}

variable "mlflowdb_user" {
  type        = string
}

variable "mlflowdb_password" {
  type        = string
}

variable "mlflowdb_endpoint" {
  type        = string
}

variable "mlflowdb_dbname" {
  type        = string
}