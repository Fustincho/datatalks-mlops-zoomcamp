output "mlflow_repository_url" {
  value = aws_ecr_repository.mlflow_repository.repository_url
}

output "mage_repository_url" {
  value = aws_ecr_repository.mage_repository.repository_url
}