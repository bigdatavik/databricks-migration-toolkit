output "repo_ids" {
  description = "Map of repo keys to IDs"
  value       = { for k, v in databricks_repo.repos : k => v.id }
}

output "repo_paths" {
  description = "Map of repo keys to paths"
  value       = { for k, v in databricks_repo.repos : k => v.path }
}
