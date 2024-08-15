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
