terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  # Configuration options
  project = "terraform-demo-project-412717"
  region  = "us-central1"
}


resource "google_storage_bucket" "demo-bucket" {
  name          = "terraform-demo-project-412717-terra-bucket"   #must be unique for all over GCP
  location      = "US"
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}