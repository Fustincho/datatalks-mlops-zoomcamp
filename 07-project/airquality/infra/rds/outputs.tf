output "mage_db_host" {
  value = aws_db_instance.mage_db.address
}

output "mlflow_db_host" {
  value = aws_db_instance.mlflow_db.address
}
