variable "groups" {
  description = "Map of groups to create"
  type = map(object({
    display_name               = string
    allow_cluster_create       = optional(bool)
    allow_instance_pool_create = optional(bool)
  }))
  default = {}
}

variable "users" {
  description = "Map of users to create"
  type = map(object({
    user_name        = string
    display_name     = optional(string)
    active           = optional(bool)
    workspace_access = optional(bool)
  }))
  default = {}
}

variable "group_members" {
  description = "Map of group memberships"
  type = map(object({
    group_key = string
    user_key  = string
  }))
  default = {}
}

variable "service_principals" {
  description = "Map of service principals"
  type = map(object({
    application_id = string
    display_name   = string
    active         = optional(bool)
  }))
  default = {}
}
