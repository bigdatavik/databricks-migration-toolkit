variable "secret_scopes" {
  description = "Map of secret scopes to create"
  type = map(object({
    name = string
    keyvault_metadata = optional(object({
      resource_id = string
      dns_name    = string
    }))
  }))
  default = {}
}

variable "secrets" {
  description = "Map of secrets to create"
  type = map(object({
    scope_key    = string
    key          = string
    string_value = string
  }))
  default   = {}
  sensitive = true
}

variable "secret_acls" {
  description = "Map of secret ACLs"
  type = map(object({
    scope_key  = string
    principal  = string
    permission = string
  }))
  default = {}
}
