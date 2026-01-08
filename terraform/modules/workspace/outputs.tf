output "directory_paths" {
  description = "Map of directory keys to paths"
  value       = { for k, v in databricks_directory.directories : k => v.path }
}

output "notebook_paths" {
  description = "Map of notebook keys to paths"
  value       = { for k, v in databricks_notebook.notebooks : k => v.path }
}

output "dbfs_file_paths" {
  description = "Map of DBFS file keys to paths"
  value       = { for k, v in databricks_dbfs_file.files : k => v.path }
}
