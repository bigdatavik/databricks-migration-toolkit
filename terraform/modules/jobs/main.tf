# Jobs Module

terraform {
  required_providers {
    databricks = {
      source = "databricks/databricks"
    }
  }
}

# Jobs
resource "databricks_job" "jobs" {
  for_each = var.jobs

  name                = each.value.name
  max_concurrent_runs = lookup(each.value, "max_concurrent_runs", 1)
  timeout_seconds     = lookup(each.value, "timeout_seconds", 0)
  
  # Email notifications
  dynamic "email_notifications" {
    for_each = lookup(each.value, "email_notifications", null) != null ? [each.value.email_notifications] : []
    content {
      on_start                 = lookup(email_notifications.value, "on_start", [])
      on_success               = lookup(email_notifications.value, "on_success", [])
      on_failure               = lookup(email_notifications.value, "on_failure", [])
      no_alert_for_skipped_runs = lookup(email_notifications.value, "no_alert_for_skipped_runs", false)
    }
  }

  # Schedule
  dynamic "schedule" {
    for_each = lookup(each.value, "schedule", null) != null ? [each.value.schedule] : []
    content {
      quartz_cron_expression = schedule.value.quartz_cron_expression
      timezone_id            = schedule.value.timezone_id
      pause_status           = lookup(schedule.value, "pause_status", "UNPAUSED")
    }
  }

  # Tasks (for multi-task jobs)
  dynamic "task" {
    for_each = lookup(each.value, "tasks", [])
    content {
      task_key = task.value.task_key

      # Notebook task
      dynamic "notebook_task" {
        for_each = lookup(task.value, "notebook_task", null) != null ? [task.value.notebook_task] : []
        content {
          notebook_path   = notebook_task.value.notebook_path
          base_parameters = lookup(notebook_task.value, "base_parameters", {})
        }
      }

      # Spark Python task
      dynamic "spark_python_task" {
        for_each = lookup(task.value, "spark_python_task", null) != null ? [task.value.spark_python_task] : []
        content {
          python_file = spark_python_task.value.python_file
          parameters  = lookup(spark_python_task.value, "parameters", [])
        }
      }

      # New cluster config for job cluster
      dynamic "new_cluster" {
        for_each = lookup(task.value, "new_cluster", null) != null ? [task.value.new_cluster] : []
        content {
          spark_version = new_cluster.value.spark_version
          node_type_id  = new_cluster.value.node_type_id
          num_workers   = lookup(new_cluster.value, "num_workers", 1)
          
          dynamic "autoscale" {
            for_each = lookup(new_cluster.value, "autoscale", null) != null ? [new_cluster.value.autoscale] : []
            content {
              min_workers = autoscale.value.min_workers
              max_workers = autoscale.value.max_workers
            }
          }
        }
      }

      # Existing cluster
      existing_cluster_id = lookup(task.value, "existing_cluster_id", null)

      # Dependencies
      dynamic "depends_on" {
        for_each = lookup(task.value, "depends_on", [])
        content {
          task_key = depends_on.value
        }
      }

      # Libraries
      dynamic "library" {
        for_each = lookup(task.value, "libraries", [])
        content {
          dynamic "pypi" {
            for_each = lookup(library.value, "pypi", null) != null ? [library.value.pypi] : []
            content {
              package = pypi.value.package
            }
          }
        }
      }
    }
  }

  # Legacy: Single task job (for backwards compatibility)
  dynamic "notebook_task" {
    for_each = lookup(each.value, "notebook_task", null) != null && lookup(each.value, "tasks", null) == null ? [each.value.notebook_task] : []
    content {
      notebook_path   = notebook_task.value.notebook_path
      base_parameters = lookup(notebook_task.value, "base_parameters", {})
    }
  }

  # Legacy: Cluster configuration
  dynamic "new_cluster" {
    for_each = lookup(each.value, "new_cluster", null) != null && lookup(each.value, "tasks", null) == null ? [each.value.new_cluster] : []
    content {
      spark_version = new_cluster.value.spark_version
      node_type_id  = new_cluster.value.node_type_id
      num_workers   = lookup(new_cluster.value, "num_workers", 1)
    }
  }

  # Tags
  tags = merge(
    var.common_tags,
    lookup(each.value, "tags", {})
  )
}
