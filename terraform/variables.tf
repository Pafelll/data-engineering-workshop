variable "project" {
  description = "Project"
  default     = "terraform-demo-485019"
}

variable "region" {
  description = "Region name"
  default     = "europe-central2"
}

variable "location" {
  description = "Project location"
  default     = "EU"
}


variable "bq_dataset_name" {
  description = "super description"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "Bucket storage Name"
  default     = "terraform-demo-485019-terra-bucket"
}
