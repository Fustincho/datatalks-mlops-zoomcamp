resource "aws_security_group" "default_vpc" {
  vpc_id      = module.vpc.vpc_id
  name        = "${var.project_prefix}-vpc-sg"
  description = "Default security group to allow inbound/outbound within the VPC and outbound to the internet"

  # Allow inbound traffic from instances associated with this security group (self)
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    self        = true
  }

  # Allow outbound traffic to instances associated with this security group (self)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    self        = true
  }

  # Allow all outbound traffic to the internet
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "mlflow_sg" {
  vpc_id      = module.vpc.vpc_id
  name        = "${var.project_prefix}-mlflow-sg"
  description = "Security group for MLflow EC2 instance to allow connections on port 5000 and PostgreSQL access from RDS"

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "mlflow_rds_sg" {
  vpc_id      = module.vpc.vpc_id
  name        = "${var.project_prefix}-mlflow-rds-sg"
  description = "MLflow Backend Store"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group_rule" "mlflow_ec2_ingress_rds" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.mlflow_sg.id
  source_security_group_id = aws_security_group.mlflow_rds_sg.id
}

resource "aws_security_group_rule" "mlflow_rds_ingress_ec2" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.mlflow_rds_sg.id
  source_security_group_id = aws_security_group.mlflow_sg.id
}


resource "aws_security_group" "mage_ai_sg" {
  vpc_id      = module.vpc.vpc_id
  name        = "${var.project_prefix}-mage-ai-sg"
  description = "Security group for Mage AI EC2 instance to allow connections on port 6789 and PostgreSQL access from RDS"

  ingress {
    from_port   = 6789
    to_port     = 6789
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "mage_ai_rds_sg" {
  vpc_id      = module.vpc.vpc_id
  name        = "${var.project_prefix}-mage-ai-rds-sg"
  description = "Mage AI Backend Store"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group_rule" "mage_ai_ec2_ingress_rds" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.mage_ai_sg.id
  source_security_group_id = aws_security_group.mage_ai_rds_sg.id
}

resource "aws_security_group_rule" "mage_ai_rds_ingress_ec2" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.mage_ai_rds_sg.id
  source_security_group_id = aws_security_group.mage_ai_sg.id
}

resource "aws_security_group" "api_sg" {
  vpc_id      = module.vpc.vpc_id
  name        = "${var.project_prefix}-api-sg"
  description = "Security group for the inference API"

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}