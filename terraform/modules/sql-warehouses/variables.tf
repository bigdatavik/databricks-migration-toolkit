variable "sql_warehouses" {
  description = "Map of SQL warehouses to create"
  type = map(object({
    name                      = string
    cluster_size              = string
    max_num_clusters          = optional(number)
    min_num_clusters          = optional(number)
    auto_stop_mins            = optional(number)
    enable_photon             = optional(bool)
    enable_serverless_compute = optional(bool)
    warehouse_type            = optional(string)
    spot_instance_policy      = optional(string)
    tags                      = optional(map(string))
    channel                   = optional(any)
  }))
  default = {}
}

variable "common_tags" {
  description = "Common tags to apply"
  type        = map(string)
  default     = {}
}
