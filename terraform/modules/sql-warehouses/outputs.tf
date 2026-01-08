output "warehouse_ids" {
  description = "Map of warehouse keys to IDs"
  value       = { for k, v in databricks_sql_endpoint.warehouses : k => v.id }
}

output "warehouse_jdbc_urls" {
  description = "Map of warehouse keys to JDBC URLs"
  value       = { for k, v in databricks_sql_endpoint.warehouses : k => v.jdbc_url }
}
