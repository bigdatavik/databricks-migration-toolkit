# Cluster Policies Module

terraform {
  required_providers {
    databricks = {
      source = "databricks/databricks"
    }
  }
}

# Cluster Policies
resource "databricks_cluster_policy" "policies" {
  for_each = var.cluster_policies

  name       = each.value.name
  definition = jsonencode(each.value.definition)
}

# All-Purpose Clusters
resource "databricks_cluster" "clusters" {
  for_each = var.clusters

  cluster_name            = each.value.cluster_name
  spark_version           = each.value.spark_version
  node_type_id            = each.value.node_type_id
  autotermination_minutes = lookup(each.value, "autotermination_minutes", 120)
  
  # Autoscaling or fixed workers
  dynamic "autoscale" {
    for_each = lookup(each.value, "autoscale", null) != null ? [each.value.autoscale] : []
    content {
      min_workers = autoscale.value.min_workers
      max_workers = autoscale.value.max_workers
    }
  }

  num_workers = lookup(each.value, "autoscale", null) == null ? lookup(each.value, "num_workers", 1) : null

  # Spark configuration
  spark_conf = lookup(each.value, "spark_conf", {})
  
  # Environment variables
  spark_env_vars = lookup(each.value, "spark_env_vars", {})
  
  # Custom tags
  custom_tags = merge(
    var.common_tags,
    lookup(each.value, "custom_tags", {})
  )

  # Cluster policy
  policy_id = lookup(each.value, "policy_key", null) != null ? databricks_cluster_policy.policies[each.value.policy_key].id : null

  # Init scripts
  dynamic "init_scripts" {
    for_each = lookup(each.value, "init_scripts", [])
    content {
      dbfs {
        destination = init_scripts.value
      }
    }
  }

  # Libraries
  dynamic "library" {
    for_each = lookup(each.value, "libraries", [])
    content {
      dynamic "pypi" {
        for_each = lookup(library.value, "pypi", null) != null ? [library.value.pypi] : []
        content {
          package = pypi.value.package
          repo    = lookup(pypi.value, "repo", null)
        }
      }

      dynamic "maven" {
        for_each = lookup(library.value, "maven", null) != null ? [library.value.maven] : []
        content {
          coordinates = maven.value.coordinates
          repo        = lookup(maven.value, "repo", null)
          exclusions  = lookup(maven.value, "exclusions", null)
        }
      }

      dynamic "jar" {
        for_each = lookup(library.value, "jar", null) != null ? [library.value.jar] : []
        content {
          uri = jar.value
        }
      }
    }
  }
}

# Instance Pools (if used)
resource "databricks_instance_pool" "pools" {
  for_each = var.instance_pools

  instance_pool_name                    = each.value.instance_pool_name
  min_idle_instances                    = lookup(each.value, "min_idle_instances", 0)
  max_capacity                          = lookup(each.value, "max_capacity", null)
  node_type_id                          = each.value.node_type_id
  idle_instance_autotermination_minutes = lookup(each.value, "idle_instance_autotermination_minutes", 10)

  dynamic "preloaded_spark_versions" {
    for_each = lookup(each.value, "preloaded_spark_versions", [])
    content {
      spark_version = preloaded_spark_versions.value
    }
  }
}
