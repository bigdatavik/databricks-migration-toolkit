# SQL Warehouses Module

terraform {
  required_providers {
    databricks = {
      source = "databricks/databricks"
    }
  }
}

# SQL Warehouses (Endpoints)
resource "databricks_sql_endpoint" "warehouses" {
  for_each = var.sql_warehouses

  name             = each.value.name
  cluster_size     = each.value.cluster_size # 2X-Small, X-Small, Small, Medium, Large, X-Large, 2X-Large, 3X-Large, 4X-Large
  max_num_clusters = lookup(each.value, "max_num_clusters", 1)
  min_num_clusters = lookup(each.value, "min_num_clusters", 1)
  
  auto_stop_mins      = lookup(each.value, "auto_stop_mins", 120)
  enable_photon       = lookup(each.value, "enable_photon", true)
  enable_serverless_compute = lookup(each.value, "enable_serverless_compute", false)
  
  warehouse_type = lookup(each.value, "warehouse_type", "PRO") # PRO or CLASSIC
  
  # Spot instance policy
  spot_instance_policy = lookup(each.value, "spot_instance_policy", "COST_OPTIMIZED") # COST_OPTIMIZED, RELIABILITY_OPTIMIZED

  # Tags
  tags {
    custom_tags = merge(
      var.common_tags,
      lookup(each.value, "tags", {})
    )
  }

  # Channel (version)
  dynamic "channel" {
    for_each = lookup(each.value, "channel", null) != null ? [each.value.channel] : []
    content {
      name = channel.value.name # CHANNEL_NAME_CURRENT or CHANNEL_NAME_PREVIEW
    }
  }
}
