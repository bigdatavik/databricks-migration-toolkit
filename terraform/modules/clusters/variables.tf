variable "cluster_policies" {
  description = "Map of cluster policies"
  type = map(object({
    name       = string
    definition = any
  }))
  default = {}
}

variable "clusters" {
  description = "Map of clusters to create"
  type = map(object({
    cluster_name            = string
    spark_version           = string
    node_type_id            = string
    autotermination_minutes = optional(number)
    num_workers             = optional(number)
    autoscale = optional(object({
      min_workers = number
      max_workers = number
    }))
    spark_conf      = optional(map(string))
    spark_env_vars  = optional(map(string))
    custom_tags     = optional(map(string))
    policy_key      = optional(string)
    init_scripts    = optional(list(string))
    libraries       = optional(list(any))
  }))
  default = {}
}

variable "instance_pools" {
  description = "Map of instance pools"
  type = map(object({
    instance_pool_name                    = string
    node_type_id                          = string
    min_idle_instances                    = optional(number)
    max_capacity                          = optional(number)
    idle_instance_autotermination_minutes = optional(number)
    preloaded_spark_versions              = optional(list(string))
  }))
  default = {}
}

variable "common_tags" {
  description = "Common tags to apply"
  type        = map(string)
  default     = {}
}
