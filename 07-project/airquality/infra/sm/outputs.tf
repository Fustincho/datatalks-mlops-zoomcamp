output "secret_arn" {
  description = "The ARN of the created secret in Secrets Manager"
  value       = aws_secretsmanager_secret.project_secrets.arn
}

output "secret_id" {
  value = aws_secretsmanager_secret.project_secrets.id
}