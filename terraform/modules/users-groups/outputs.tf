output "group_ids" {
  description = "Map of group names to IDs"
  value       = { for k, v in databricks_group.groups : k => v.id }
}

output "user_ids" {
  description = "Map of user names to IDs"
  value       = { for k, v in databricks_user.users : k => v.id }
}

output "service_principal_ids" {
  description = "Map of service principal names to IDs"
  value       = { for k, v in databricks_service_principal.service_principals : k => v.id }
}
