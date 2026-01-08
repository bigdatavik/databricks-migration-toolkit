# Terraform Databricks Migration - Quick Start Guide

## Prerequisites

1. **Install Terraform**
```bash
brew install terraform
terraform version  # Should be >= 1.0
```

2. **Configure Databricks Access**
```bash
# Option 1: Using config file
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your workspace details

# Option 2: Using environment variables
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi_your_token_here"
```

## Quick Start

### Step 1: Export from Source Workspace

```bash
# From terraform directory
python scripts/export_to_terraform.py --workspace source --output ./environments/source

# This generates:
# - users_groups.auto.tfvars.json
# - clusters.auto.tfvars.json
# - jobs.auto.tfvars.json
# - secrets.auto.tfvars.json
# - sql_warehouses.auto.tfvars.json
# - repos.auto.tfvars.json
```

### Step 2: Review Generated Configs

```bash
cd environments/source
ls -la *.json

# Review and customize as needed
```

### Step 3: Create main.tf

Use the example as a starting point:

```bash
cp ../../examples/complete/main.tf ./main.tf
```

Or create manually:

```hcl
terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.40"
    }
  }
}

provider "databricks" {
  host  = var.target_workspace.host
  token = var.target_workspace.token
}

module "users_groups" {
  source = "../../modules/users-groups"
  groups = var.groups
  users  = var.users
}

# Add other modules as needed
```

### Step 4: Initialize Terraform

```bash
terraform init

# This will:
# - Download Databricks provider
# - Initialize modules
# - Set up backend
```

### Step 5: Plan the Migration

```bash
terraform plan

# Review what will be created:
# - Number of resources
# - Resource names and configurations
# - Any errors or warnings
```

### Step 6: Apply Changes

```bash
terraform apply

# Review the plan
# Type 'yes' to confirm
```

## Directory Structure After Setup

```
terraform/
├── environments/
│   ├── source/
│   │   ├── main.tf
│   │   ├── terraform.tfvars
│   │   ├── users_groups.auto.tfvars.json
│   │   ├── clusters.auto.tfvars.json
│   │   └── ...
│   └── target/
│       └── (similar structure)
├── modules/
│   ├── users-groups/
│   ├── clusters/
│   └── ...
└── scripts/
    ├── export_to_terraform.py
    └── import.sh
```

## Common Commands

```bash
# Format Terraform files
terraform fmt -recursive

# Validate configuration
terraform validate

# Show current state
terraform show

# List resources in state
terraform state list

# Show specific resource
terraform state show 'module.clusters.databricks_cluster.clusters["cluster_0"]'

# Plan with specific var file
terraform plan -var-file="custom.tfvars"

# Apply specific module
terraform apply -target=module.users_groups

# Destroy everything (careful!)
terraform destroy
```

## Import Existing Resources

If resources already exist in target workspace:

```bash
# Find resource ID in Databricks UI or API
# Import into Terraform state
terraform import 'module.users_groups.databricks_group.groups["admins"]' 'Admins'

# Verify import
terraform plan  # Should show no changes for imported resource
```

## Troubleshooting

### Issue: Provider authentication failed
```bash
# Check credentials
echo $DATABRICKS_HOST
echo $DATABRICKS_TOKEN

# Or verify terraform.tfvars
cat terraform.tfvars
```

### Issue: Module not found
```bash
# Re-initialize
terraform init -upgrade
```

### Issue: State lock error
```bash
# If using remote state and lock is stuck
# (Be careful with this!)
terraform force-unlock <lock-id>
```

### Issue: Resource already exists
```bash
# Option 1: Import existing resource
terraform import '<resource_address>' '<resource_id>'

# Option 2: Remove from state and recreate
terraform state rm '<resource_address>'
```

## Best Practices

1. **Use Remote State** (for team collaboration)
```hcl
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "databricks/terraform.tfstate"
    region = "us-east-1"
  }
}
```

2. **Use Workspaces** (for multiple environments)
```bash
terraform workspace new production
terraform workspace new staging
terraform workspace select production
```

3. **Version Pin Providers**
```hcl
terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "= 1.40.0"  # Pin exact version
    }
  }
}
```

4. **Sensitive Variables**
```hcl
variable "databricks_token" {
  type      = string
  sensitive = true
}
```

5. **Use Data Sources** (reference existing resources)
```hcl
data "databricks_current_user" "me" {}

output "current_user" {
  value = data.databricks_current_user.me.user_name
}
```

## Next Steps

1. Review example in `examples/complete/`
2. Customize for your environment
3. Test in dev workspace first
4. Set up CI/CD pipeline
5. Document custom configurations

## Resources

- [Terraform Databricks Provider Docs](https://registry.terraform.io/providers/databricks/databricks/latest/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [Databricks Terraform Examples](https://github.com/databricks/terraform-provider-databricks/tree/main/examples)
