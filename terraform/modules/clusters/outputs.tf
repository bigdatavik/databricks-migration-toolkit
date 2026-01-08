output "cluster_ids" {
  description = "Map of cluster names to IDs"
  value       = { for k, v in databricks_cluster.clusters : k => v.id }
}

output "cluster_policy_ids" {
  description = "Map of policy names to IDs"
  value       = { for k, v in databricks_cluster_policy.policies : k => v.id }
}

output "instance_pool_ids" {
  description = "Map of instance pool names to IDs"
  value       = { for k, v in databricks_instance_pool.pools : k => v.id }
}
