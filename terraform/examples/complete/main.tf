# Example: Complete Databricks Migration Configuration

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.40"
    }
  }
}

# Provider for target workspace
provider "databricks" {
  host  = var.target_workspace.host
  token = var.target_workspace.token
}

# Module: Users and Groups
module "users_groups" {
  source = "../../modules/users-groups"
  
  groups = var.groups
  users  = var.users
  group_members = var.group_members
}

# Module: Cluster Policies and Clusters
module "clusters" {
  source = "../../modules/clusters"
  
  cluster_policies = var.cluster_policies
  clusters         = var.clusters
  instance_pools   = var.instance_pools
  common_tags      = var.common_tags
  
  depends_on = [module.users_groups]
}

# Module: SQL Warehouses
module "sql_warehouses" {
  source = "../../modules/sql-warehouses"
  
  sql_warehouses = var.sql_warehouses
  common_tags    = var.common_tags
  
  depends_on = [module.users_groups]
}

# Module: Secret Scopes
module "secrets" {
  source = "../../modules/secrets"
  
  secret_scopes = var.secret_scopes
  secrets       = var.secrets
  secret_acls   = var.secret_acls
  
  depends_on = [module.users_groups]
}

# Module: Workspace (folders and notebooks)
module "workspace" {
  source = "../../modules/workspace"
  
  directories = var.directories
  notebooks   = var.notebooks
  dbfs_files  = var.dbfs_files
  
  depends_on = [module.users_groups]
}

# Module: Git Repositories
module "repos" {
  source = "../../modules/repos"
  
  repos = var.repos
  
  depends_on = [module.workspace]
}

# Module: Jobs
module "jobs" {
  source = "../../modules/jobs"
  
  jobs        = var.jobs
  common_tags = var.common_tags
  
  # Jobs depend on most other resources
  depends_on = [
    module.clusters,
    module.workspace,
    module.repos,
    module.secrets
  ]
}
