provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "devops_artifacts" {
  bucket_prefix = "aws-devops-platform-"

  tags = {
    Project     = "aws-devops-platform"
    Environment = "learning"
    ManagedBy   = "terraform"
    Stage       = "terraform-demo"
  }
}

output "aws_account_id" {
  description = "AWS account ID used by Terraform"
  value       = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  description = "AWS region configured for Terraform"
  value       = var.aws_region
}

output "s3_bucket_name" {
  description = "Name of the Terraform-managed S3 bucket"
  value       = aws_s3_bucket.devops_artifacts.bucket
}
