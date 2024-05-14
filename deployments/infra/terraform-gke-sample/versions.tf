

terraform {
  required_version = ">= 1.0.11"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 3.39.0, <5.0.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 3.43, < 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}