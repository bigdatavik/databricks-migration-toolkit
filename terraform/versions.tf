terraform {
  required_version = ">= 1.0"

  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.40"
    }
  }

  # Optional: Configure remote state backend
  # backend "s3" {
  #   bucket = "my-terraform-state"
  #   key    = "databricks-migration/terraform.tfstate"
  #   region = "us-east-1"
  # }
}

provider "databricks" {
  alias = "source"
  host  = var.source_workspace.host
  token = var.source_workspace.token
}

provider "databricks" {
  alias = "target"
  host  = var.target_workspace.host
  token = var.target_workspace.token
}
