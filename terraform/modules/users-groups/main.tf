# Users and Groups Module

terraform {
  required_providers {
    databricks = {
      source = "databricks/databricks"
    }
  }
}

# Data source to read users from source (if needed)
# This would be populated by the export script

# Create Groups
resource "databricks_group" "groups" {
  for_each = var.groups

  display_name               = each.value.display_name
  allow_cluster_create       = lookup(each.value, "allow_cluster_create", false)
  allow_instance_pool_create = lookup(each.value, "allow_instance_pool_create", false)
}

# Create Users
resource "databricks_user" "users" {
  for_each = var.users

  user_name    = each.value.user_name
  display_name = lookup(each.value, "display_name", each.value.user_name)
  active       = lookup(each.value, "active", true)
  
  # Optional: Set user as workspace admin
  workspace_access = lookup(each.value, "workspace_access", true)
}

# Group Memberships
resource "databricks_group_member" "members" {
  for_each = var.group_members

  group_id  = databricks_group.groups[each.value.group_key].id
  member_id = databricks_user.users[each.value.user_key].id
}

# Service Principals (if needed)
resource "databricks_service_principal" "service_principals" {
  for_each = var.service_principals

  application_id = each.value.application_id
  display_name   = each.value.display_name
  active         = lookup(each.value, "active", true)
}
