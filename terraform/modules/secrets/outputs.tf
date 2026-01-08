output "scope_names" {
  description = "Map of scope keys to names"
  value       = { for k, v in databricks_secret_scope.scopes : k => v.name }
}
