resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "${var.project_prefix}_rds_subnet_group"
  subnet_ids = var.private_subnet_ids

  tags = {
    Name = "MLflow DB subnet group"
  }
}

resource "aws_db_instance" "mlflow_db" {
  identifier              = "${var.project_prefix}-mlflow"
  allocated_storage       = 20
  engine                  = "postgres"
  instance_class          = "db.t3.micro"
  db_name                 = "mlflow_db"
  username                = var.mlflow_rds_username
  password                = var.mlflow_rds_password
  parameter_group_name    = "default.postgres16"
  port                    = 5432
  skip_final_snapshot     = true
  publicly_accessible     = false
  vpc_security_group_ids  = [var.mlflow_rds_sg_id]
  db_subnet_group_name    = aws_db_subnet_group.rds_subnet_group.name
}

resource "aws_db_instance" "mage_db" {
  identifier              = "${var.project_prefix}-mage"
  allocated_storage       = 20
  engine                  = "postgres"
  instance_class          = "db.t3.micro"
  db_name                 = "mage_database"
  username                = var.mage_rds_username
  password                = var.mage_rds_password
  parameter_group_name    = "default.postgres16"
  port                    = 5432
  skip_final_snapshot     = true
  publicly_accessible     = false
  vpc_security_group_ids  = [var.mage_ai_rds_sg_id]
  db_subnet_group_name    = aws_db_subnet_group.rds_subnet_group.name
}
