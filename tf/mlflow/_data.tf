data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
data "aws_availability_zones" "available" {}

data "aws_vpc" "this" {
  filter {
    name   = "tag:Name"
    values = ["${local.prefix}-vpc"]
  }
}

data "aws_subnets" "public" {
  filter {
    name   = "tag:Name"
    values = ["${local.prefix}-public-us-east-1*"]
  }
}

data "aws_subnet" "public" {
  for_each = toset(data.aws_subnets.public.ids)
  id       = each.value
}

data "aws_subnets" "private" {
  filter {
    name   = "tag:Name"
    values = ["${local.prefix}-private-us-east-1*"]
  }
}

data "aws_subnet" "private" {
  for_each = toset(data.aws_subnets.private.ids)
  id       = each.value
}

data "aws_subnets" "public_1b" {
  filter {
    name   = "tag:Name"
    values = ["${local.prefix}-public-us-east-1b*"]
  }
}

data "aws_subnet" "public_1b" {
  for_each = toset(data.aws_subnets.public.ids)
  id       = each.value
}

data "aws_security_group" "mlflow_rds" {
  name = "${local.prefix}-mlflow-rds-sg"
}

data "aws_security_group" "kubernetes" {
  tags = {
    "kubernetes.io/cluster/${local.prefix}-eks-cluster" = "owned"
  }
}

data "aws_sns_topic" "email" {
  name = "${local.prefix}-email-sns"
}

data "aws_db_subnet_group" "rds" {
  name = "${local.prefix}-db-subnet-group"
}