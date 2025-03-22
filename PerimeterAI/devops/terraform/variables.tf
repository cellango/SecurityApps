variable "environment" {
  type        = string
  description = "Environment (dev/prod)"
}

variable "region" {
  type        = string
  description = "Default region for resources"
}

variable "cloud_provider" {
  type        = string
  description = "Cloud provider (aws/azure)"
}

variable "cluster_name" {
  type        = string
  description = "Name of the Kubernetes cluster"
}
