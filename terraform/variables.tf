variable "source_workspace" {
  description = "Source Databricks workspace configuration"
  type = object({
    host  = string
    token = string
  })
  sensitive = true
}

variable "target_workspace" {
  description = "Target Databricks workspace configuration"
  type = object({
    host  = string
    token = string
  })
  sensitive = true
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  default     = "production"
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "resource_prefix" {
  description = "Prefix for resource names"
  type        = string
  default     = ""
}
