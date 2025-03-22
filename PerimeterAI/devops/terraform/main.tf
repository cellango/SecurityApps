terraform {
  required_version = ">= 1.0.0"
  backend "s3" {
    # Will be configured per environment
  }
}
