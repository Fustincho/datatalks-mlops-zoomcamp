resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "${var.project_prefix}-vpc"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${var.project_prefix}-igw"
  }
}

resource "aws_eip" "nat_eip" {
  domain = "vpc"
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.project_prefix}-public-subnet-${var.availability_zones[count.index]}"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]
  tags = {
    Name = "${var.project_prefix}-private-subnet-${var.availability_zones[count.index]}"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${var.project_prefix}-public-route-table"
  }
}

resource "aws_route_table_association" "public" {
  count        = length(var.public_subnet_cidrs)
  subnet_id    = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route" "public_route" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public[0].id  # Use the first public subnet
  tags = {
    Name = "${var.project_prefix}-nat-gateway"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${var.project_prefix}-private-route-table"
  }
}

resource "aws_route_table_association" "private" {
  count        = length(var.private_subnet_cidrs)
  subnet_id    = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

resource "aws_route" "private_route" {
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat.id
}
