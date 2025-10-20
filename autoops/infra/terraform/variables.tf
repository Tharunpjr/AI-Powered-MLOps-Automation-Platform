# AutoOps Infrastructure Variables

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "autoops-cluster"
}

variable "kubernetes_version" {
  description = "Kubernetes version for EKS cluster"
  type        = string
  default     = "1.28"
}

variable "create_eks_cluster" {
  description = "Whether to create EKS cluster"
  type        = bool
  default     = false
}

variable "subnet_ids" {
  description = "List of subnet IDs for EKS cluster"
  type        = list(string)
  default     = []
}

variable "kubernetes_host" {
  description = "Kubernetes API server host"
  type        = string
  default     = ""
}

variable "kubernetes_cluster_ca_certificate" {
  description = "Kubernetes cluster CA certificate"
  type        = string
  default     = ""
}

variable "kubernetes_token" {
  description = "Kubernetes API token"
  type        = string
  default     = ""
  sensitive   = true
}

variable "model_artifacts_bucket_name" {
  description = "S3 bucket name for model artifacts"
  type        = string
  default     = "autoops-model-artifacts"
}

variable "namespace" {
  description = "Kubernetes namespace for AutoOps"
  type        = string
  default     = "autoops"
}

variable "replica_count" {
  description = "Number of replicas for model service"
  type        = number
  default     = 2
}

variable "resource_requests_cpu" {
  description = "CPU resource requests"
  type        = string
  default     = "100m"
}

variable "resource_requests_memory" {
  description = "Memory resource requests"
  type        = string
  default     = "256Mi"
}

variable "resource_limits_cpu" {
  description = "CPU resource limits"
  type        = string
  default     = "500m"
}

variable "resource_limits_memory" {
  description = "Memory resource limits"
  type        = string
  default     = "512Mi"
}
