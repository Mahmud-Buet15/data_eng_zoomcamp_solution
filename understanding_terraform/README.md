

### Refresh service-account's auth-token for this session
gcloud auth application-default login

### Initialize state file (.tfstate)
terraform init

### Formatting
terraform fmt

### Saving credentials as environment variable
export GOOGLE_CREDENTIALS='/home/mahmud/Desktop/personal_tasks/data_eng_zoomcamp_solution/understanding_terraform/keys/my-creds.json'

### Check changes to new infra plan
terraform plan 

### Apply the infra plan (contents of main.tf file)
terraform apply 

### Destroy the infra plan (contents of main.tf file)
terraform destroy 


