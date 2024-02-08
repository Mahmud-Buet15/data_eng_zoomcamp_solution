

variable "credentials" {
    description = "Credential file"
    default = "./keys/my-creds.json"
}

variable "project_name" {
    description = "Name of the project"
    default = "terraform-demo-project-412717"
    
}

variable "region" {
    description = "Name of the Region"
    default = "us-central1"
    
}

variable "location_name" {
    description = "Name of location"
    default = "US"
    
}

variable "gcs_bucket_name" {
    description = "Name of GCS bucket"
    default = "terraform-demo-project-412717-terra-bucket"
    
}

variable "bq_dataset_name" {
    description = "My BigQuery Dataset Name"
    default = "example_dataset"
    
}