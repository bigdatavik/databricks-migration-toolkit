variable "jobs" {
  description = "Map of jobs to create"
  type = map(object({
    name                = string
    max_concurrent_runs = optional(number)
    timeout_seconds     = optional(number)
    email_notifications = optional(any)
    schedule            = optional(any)
    tasks               = optional(list(any))
    notebook_task       = optional(any)
    new_cluster         = optional(any)
    existing_cluster_id = optional(string)
    tags                = optional(map(string))
  }))
  default = {}
}

variable "common_tags" {
  description = "Common tags to apply"
  type        = map(string)
  default     = {}
}
