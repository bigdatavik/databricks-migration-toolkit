output "job_ids" {
  description = "Map of job names to IDs"
  value       = { for k, v in databricks_job.jobs : k => v.id }
}

output "job_urls" {
  description = "Map of job names to URLs"
  value       = { for k, v in databricks_job.jobs : k => v.url }
}
