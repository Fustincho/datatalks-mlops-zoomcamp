resource "aws_secretsmanager_secret" "project_secrets" {
  name = "${var.project_prefix}-secrets"
}

resource "aws_secretsmanager_secret_version" "project_secrets_value" {
  secret_id     = aws_secretsmanager_secret.project_secrets.id
    secret_string = jsonencode({
    "MAGEDB_HOST"                 = var.magedb_host
    "MAGE_DATABASE_CONNECTION_URL" = var.mage_database_connection_url
    "MLFLOW_HOST"                 = var.mlflow_host
    "API_HOST"                    = var.api_host
    "OPENAQ_API_KEY"              = var.openaq_api_key
    "MAGEDB_PORT"                 = var.magedb_port
    "MAGEDB_NAME"                 = var.magedb_name
    "MAGEDB_USER"                 = var.magedb_user
    "MAGEDB_PASSWORD"             = var.magedb_password
    "S3_BUCKET_NAME"              = var.s3_bucket_name
  })
}
