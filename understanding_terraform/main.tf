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
  credentials = var.credentials
  project = var.project_name
  region  = var.region
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id                  = var.bq_dataset_name
}


resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name   #must be unique for all over GCP
  location      = var.location_name
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