# AutoOps Infrastructure - Main Configuration
# This is a skeleton for cloud infrastructure setup

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

# Configure AWS Provider
provider "aws" {
  region = var.aws_region
}

# Configure Kubernetes Provider
provider "kubernetes" {
  host                   = var.kubernetes_host
  cluster_ca_certificate = base64decode(var.kubernetes_cluster_ca_certificate)
  token                  = var.kubernetes_token
}

# ECR Repository for container images
resource "aws_ecr_repository" "autoops_model_service" {
  name                 = "autoops/model-service"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# EKS Cluster (placeholder - configure as needed)
resource "aws_eks_cluster" "autoops_cluster" {
  count    = var.create_eks_cluster ? 1 : 0
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster[0].arn
  version  = var.kubernetes_version

  vpc_config {
    subnet_ids = var.subnet_ids
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy[0],
  ]
}

# IAM Role for EKS Cluster
resource "aws_iam_role" "eks_cluster" {
  count = var.create_eks_cluster ? 1 : 0
  name  = "${var.cluster_name}-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  count      = var.create_eks_cluster ? 1 : 0
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster[0].name
}

# S3 Bucket for model artifacts
resource "aws_s3_bucket" "model_artifacts" {
  bucket = var.model_artifacts_bucket_name

  tags = {
    Name        = "AutoOps Model Artifacts"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "model_artifacts" {
  bucket = aws_s3_bucket.model_artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}

# CloudWatch Log Group for monitoring
resource "aws_cloudwatch_log_group" "autoops_logs" {
  name              = "/aws/eks/autoops"
  retention_in_days = 30

  tags = {
    Environment = var.environment
    Application = "AutoOps"
  }
}
