# Databricks Unity Catalog Migration - Terraform Approach

This directory contains Terraform configurations for migrating Databricks Unity Catalog workspaces using Infrastructure as Code (IaC).

## Overview

Instead of using Python scripts with REST APIs, this approach uses:
- **Terraform** for declarative infrastructure management
- **Databricks Provider** for resource management
- **State files** for tracking resources
- **Modules** for reusable components

## Structure

```
terraform/
├── modules/              # Reusable Terraform modules
│   ├── users-groups/     # User and group management
│   ├── workspace/        # Workspace folders and notebooks
│   ├── clusters/         # Cluster configurations
│   ├── jobs/             # Job definitions
│   ├── sql-warehouses/   # SQL warehouse configs
│   ├── secrets/          # Secret scope management
│   └── repos/            # Git repo integrations
├── environments/         # Environment-specific configs
│   ├── source/           # Source workspace
│   └── target/           # Target workspace
├── scripts/              # Helper scripts
│   ├── export.py         # Export from source to Terraform
│   └── import.sh         # Import existing resources
└── examples/             # Example configurations
```

## Quick Start

### 1. Prerequisites
```bash
# Install Terraform
brew install terraform

# Install Databricks CLI
pip install databricks-cli

# Verify installation
terraform version
databricks --version
```

### 2. Configure Provider
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your workspace details
```

### 3. Export Existing Resources
```bash
# Export source workspace to Terraform configs
python scripts/export_to_terraform.py --workspace source

# This generates .tf files in environments/source/
```

### 4. Plan Migration
```bash
cd environments/target
terraform init
terraform plan
```

### 5. Apply Changes
```bash
terraform apply
```

## Advantages of Terraform Approach

### ✅ Benefits
- **Declarative**: Define desired state, Terraform handles the rest
- **State Management**: Track what's deployed and detect drift
- **Version Control**: All configs in Git
- **Preview Changes**: `terraform plan` shows what will change
- **Rollback**: Easy to revert using Git + Terraform
- **Idempotent**: Safe to run multiple times
- **Dependencies**: Automatic dependency resolution

### ⚠️ Considerations
- Requires Terraform knowledge
- State file management needed
- Some resources may need manual import
- Initial setup takes longer than Python scripts

## Comparison with Python Scripts

| Aspect | Python Scripts | Terraform |
|--------|---------------|-----------|
| **Learning Curve** | Lower | Higher |
| **State Management** | Manual | Automatic |
| **Idempotency** | Manual | Built-in |
| **Drift Detection** | No | Yes |
| **Rollback** | Manual | Git + Terraform |
| **Dependencies** | Manual | Automatic |
| **Preview Changes** | No | Yes (plan) |
| **Best For** | One-time migrations | Ongoing management |

## Migration Workflow

```
Source Workspace
       ↓
   [Export Script]
       ↓
   Terraform Configs (.tf files)
       ↓
   [terraform plan]
       ↓
   Review Changes
       ↓
   [terraform apply]
       ↓
   Target Workspace
```

## Next Steps

1. Review the modules in `modules/` directory
2. Check examples in `examples/` directory  
3. Run export script to generate configs
4. Review generated Terraform files
5. Customize as needed
6. Apply to target workspace

## Documentation

- [Terraform Databricks Provider](https://registry.terraform.io/providers/databricks/databricks/latest/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [Databricks Terraform Examples](https://github.com/databricks/terraform-provider-databricks/tree/main/examples)
