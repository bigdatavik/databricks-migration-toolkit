#!/bin/bash
# Import existing Databricks resources into Terraform state

set -e

echo "========================================="
echo "Import Existing Resources to Terraform"
echo "========================================="
echo ""

# Check if terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform not found. Please install: brew install terraform"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "versions.tf" ]; then
    echo "❌ Please run this script from the terraform directory"
    exit 1
fi

echo "This script will import existing resources into Terraform state"
echo "This is useful if resources already exist in the target workspace"
echo ""
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cancelled"
    exit 0
fi

# Initialize terraform
echo ""
echo "Initializing Terraform..."
terraform init

# Example imports (customize based on your resources)
echo ""
echo "Import examples (uncomment and customize):"
echo ""

# Import users
# terraform import 'module.users_groups.databricks_user.users["user_0"]' <user_id>

# Import groups
# terraform import 'module.users_groups.databricks_group.groups["group_0"]' <group_id>

# Import clusters
# terraform import 'module.clusters.databricks_cluster.clusters["cluster_0"]' <cluster_id>

# Import jobs
# terraform import 'module.jobs.databricks_job.jobs["job_0"]' <job_id>

# Import secret scopes
# terraform import 'module.secrets.databricks_secret_scope.scopes["scope_0"]' <scope_name>

# Import SQL warehouses
# terraform import 'module.sql_warehouses.databricks_sql_endpoint.warehouses["warehouse_0"]' <warehouse_id>

# Import repos
# terraform import 'module.repos.databricks_repo.repos["repo_0"]' <repo_id>

echo ""
echo "To import resources:"
echo "1. Find resource IDs from your workspace"
echo "2. Uncomment and customize import commands above"
echo "3. Run: terraform import '<resource_address>' '<resource_id>'"
echo ""
echo "Example:"
echo "  terraform import 'module.users_groups.databricks_group.groups[\"admins\"]' 'Admins'"
echo ""
