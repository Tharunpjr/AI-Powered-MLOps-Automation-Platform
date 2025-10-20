# AutoOps Infrastructure Outputs

output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.autoops_model_service.repository_url
}

output "ecr_repository_arn" {
  description = "ARN of the ECR repository"
  value       = aws_ecr_repository.autoops_model_service.arn
}

output "eks_cluster_id" {
  description = "EKS cluster ID"
  value       = var.create_eks_cluster ? aws_eks_cluster.autoops_cluster[0].id : null
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = var.create_eks_cluster ? aws_eks_cluster.autoops_cluster[0].endpoint : null
}

output "eks_cluster_security_group_id" {
  description = "EKS cluster security group ID"
  value       = var.create_eks_cluster ? aws_eks_cluster.autoops_cluster[0].vpc_config[0].cluster_security_group_id : null
}

output "model_artifacts_bucket_name" {
  description = "S3 bucket name for model artifacts"
  value       = aws_s3_bucket.model_artifacts.bucket
}

output "model_artifacts_bucket_arn" {
  description = "S3 bucket ARN for model artifacts"
  value       = aws_s3_bucket.model_artifacts.arn
}

output "cloudwatch_log_group_name" {
  description = "CloudWatch log group name"
  value       = aws_cloudwatch_log_group.autoops_logs.name
}

output "cloudwatch_log_group_arn" {
  description = "CloudWatch log group ARN"
  value       = aws_cloudwatch_log_group.autoops_logs.arn
}
