resource "aws_db_instance" "this" {
  allocated_storage      = 10
  db_name                = "mlflow"
  identifier             = "${local.prefix}-mlflow-db"
  engine                 = "postgres"
  engine_version         = "16.2"
  instance_class         = "db.t3.micro"
  username               = "postgres"
  password               = random_password.this.result
  vpc_security_group_ids = [data.aws_security_group.mlflow_rds.id]
  db_subnet_group_name   = data.aws_db_subnet_group.rds.name
  skip_final_snapshot    = true
  storage_encrypted      = true
  enabled_cloudwatch_logs_exports = ["postgresql"]
  iam_database_authentication_enabled = true

  tags = local.tags
}


## PASSWORD ##
resource "random_password" "this" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}


## SECRURITY GROUP RULES ##

resource "aws_security_group_rule" "mlflow_ingress" {
  security_group_id = data.aws_security_group.mlflow_rds.id
  description       = "Allow inbound traffic on port 5432 from EKS Cluster"
  type              = "ingress"
  protocol          = "tcp"
  from_port         = 5432
  to_port           = 5432
  source_security_group_id = data.aws_security_group.kubernetes.id
}


## IAM ACCESS ##

resource "aws_iam_policy" "rds_access" {
  name        = "${local.prefix}-mlflow-rds-access-policy"
  path        = "/"
  description = "This Policy give access to the Mlflow RDS Database"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "RDS"
        Effect = "Allow"
        Action = [
          "rds-db:connect"
        ]
        Resource = "arn:aws:rds-db:us-east-1:${data.aws_caller_identity.current.account_id}:dbuser:*/postgres"
      }
    ]
  })

  tags = local.tags
}