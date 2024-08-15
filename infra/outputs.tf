output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnet_ids" {
  value = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  value = module.vpc.private_subnet_ids
}

output "default_vpc_sg_id" {
  description = "The ID of the default VPC security group."
  value       = aws_security_group.default_vpc.id
}

output "default_vpc_sg_name" {
  description = "The name of the default VPC security group."
  value       = aws_security_group.default_vpc.name
}

output "mlflow_repository_url" {
  value = module.ecr.mlflow_repository_url
}

output "mage_repository_url" {
  value = module.ecr.mage_repository_url
}