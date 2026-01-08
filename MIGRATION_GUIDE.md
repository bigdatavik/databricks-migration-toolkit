# Databricks Unity Catalog Workspace Migration Guide

## Overview

This guide provides detailed instructions for migrating Databricks Unity Catalog workspace objects from one workspace to another using the provided migration scripts.

## Migration Objects

### Enablement Team Objects
These are foundational objects typically provisioned by the enablement/platform team:

1. **AD Group & User Onboarding** - User identities and group memberships
2. **Workspace Folder** - Directory structure for organizing workspace objects
3. **Secret Scopes** - Secure storage for credentials (note: values must be re-entered)
4. **SQL Warehouses** - Compute resources for SQL queries
5. **Cluster Policies** - Governance policies for cluster creation

### Business/App Team Objects
These are objects created and managed by application/business teams:

1. **Clusters** (All-Purpose: 2) - Interactive compute clusters
2. **Job Clusters** (N/A) - Clusters defined within job configurations
3. **Notebooks** (1+) - Jupyter-style notebooks
4. **Secrets in Secret Scope** (1) - Application-specific secrets
5. **Jobs** (600/business: 2) - Scheduled workflows and pipelines
6. **Git Repos Integration** (3) - Connected Git repositories

## Prerequisites

### Access Requirements
- Admin or appropriate permissions in both source and target workspaces
- API tokens for both workspaces
- Network access to both Databricks workspaces

### Software Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)

## Installation

1. **Clone or download this repository**
```bash
cd Migration
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure workspace connections**
Edit `config.json` with your workspace details:
```json
{
  "source": {
    "host": "https://adb-123456789.azuredatabricks.net",
    "token": "dapi_abc123..."
  },
  "target": {
    "host": "https://adb-987654321.azuredatabricks.net",
    "token": "dapi_xyz789..."
  }
}
```

## Migration Order

**IMPORTANT**: Follow this exact order to maintain dependencies:

### Phase 1: Foundation (Enablement Team)
1. **Users & Groups** - Run first as other objects depend on user identities
2. **Cluster Policies** - Required before creating clusters
3. **SQL Warehouses** - Can run in parallel with other Phase 1 items
4. **Secret Scopes** - Structure created (values need manual update)
5. **Workspace Folders** - Required before importing notebooks

### Phase 2: Content & Compute (Business Team)
6. **Clusters** - All-purpose clusters (created in TERMINATED state)
7. **Notebooks** - Workspace notebooks
8. **Git Repos** - Repository integrations

### Phase 3: Orchestration
9. **Jobs** - Must be last as they reference other objects

## Running Migrations

### Option 1: Run All Migrations Sequentially
```bash
python run_all_migrations.py
```

This will run all migrations in the correct order with progress tracking.

### Option 2: Run Individual Migrations
```bash
# Phase 1
python migrate_users_groups.py
python migrate_cluster_policies.py
python migrate_sql_warehouses.py
python migrate_secret_scopes.py
python migrate_workspace_folders.py

# Phase 2
python migrate_clusters.py
python migrate_notebooks.py
python migrate_git_repos.py

# Phase 3
python migrate_jobs.py
```

## Script Descriptions

### migrate_users_groups.py
- Migrates AD groups and their members
- Creates users in target workspace via SCIM API
- Preserves group membership relationships
- **Note**: Password-based users may need to reset passwords

### migrate_workspace_folders.py
- Recreates folder hierarchy from source to target
- Recursively traverses directory structure
- Creates parent folders before children

### migrate_secret_scopes.py
- Creates secret scope structure
- Creates placeholder secrets (values cannot be read via API)
- **ACTION REQUIRED**: Manually update secret values after migration

### migrate_sql_warehouses.py
- Migrates SQL warehouse configurations
- Preserves sizing, auto-stop, and Photon settings
- Warehouses created in STOPPED state

### migrate_cluster_policies.py
- Migrates custom cluster policies
- Skips built-in/default policies
- Preserves policy definitions and constraints

### migrate_clusters.py
- Migrates all-purpose clusters only (not job clusters)
- Clusters created in TERMINATED state
- Preserves Spark configs, init scripts, and libraries
- **Note**: Instance pools and policy IDs may need updating

### migrate_notebooks.py
- Exports notebooks in SOURCE format
- Preserves all languages (Python, SQL, Scala, R)
- Maintains folder structure (requires workspace folders to exist first)

### migrate_git_repos.py
- Migrates Git repository configurations
- Preserves repo URLs, providers, and branch/tag info
- **ACTION REQUIRED**: Re-authenticate Git credentials

### migrate_jobs.py
- Migrates job definitions and schedules
- **ACTION REQUIRED**: Update cluster IDs and notebook paths
- Job clusters are migrated within job definitions
- Review dependencies and parameters

## Post-Migration Steps

### 1. Update Secret Values
```bash
# Secrets are created with placeholder values
# Update them manually via UI or CLI
databricks secrets put --scope <scope-name> --key <secret-key>
```

### 2. Verify and Update Jobs
- Review cluster references (cluster IDs change in migration)
- Verify notebook paths are correct
- Check library dependencies
- Validate job parameters and schedules
- Update any hardcoded workspace URLs

### 3. Test Clusters and Warehouses
```bash
# Start a test cluster
databricks clusters start --cluster-id <cluster-id>

# Start a SQL warehouse
databricks sql warehouses start --id <warehouse-id>
```

### 4. Configure Git Repository Access
- Re-authenticate Git providers (GitHub, GitLab, Azure DevOps)
- Verify repository credentials
- Test pull operations

### 5. Run Test Jobs
- Start with simple test jobs
- Gradually test more complex workflows
- Monitor for errors in job runs

### 6. Update Instance Pools (if used)
- Recreate or map instance pool IDs
- Update cluster configurations accordingly

## Backup and Recovery

All scripts automatically create backups before migration:
- Format: `backup_<object_type>_<timestamp>.json`
- Location: Current directory
- Use these for rollback or reference

### Manual Backup
```bash
# Backup is automatic but you can also use Databricks CLI
databricks workspace export_dir /path/to/backup ./backup/
```

## Troubleshooting

### Common Issues

#### 1. Authentication Errors
```
Error: 403 Forbidden
```
**Solution**: Verify API tokens have correct permissions

#### 2. Object Already Exists
```
Error: Resource already exists
```
**Solution**: Delete or rename existing object in target workspace

#### 3. Policy ID Not Found
```
Error: Cluster policy not found
```
**Solution**: Run `migrate_cluster_policies.py` before `migrate_clusters.py`

#### 4. Notebook Import Fails
```
Error: Path does not exist
```
**Solution**: Run `migrate_workspace_folders.py` first

#### 5. Job Creation Fails
```
Error: Invalid cluster specification
```
**Solution**: Update cluster IDs in job configuration

### Debug Mode
Enable detailed logging:
```python
# In config.json
{
  "migration_settings": {
    "log_level": "DEBUG"
  }
}
```

## Best Practices

1. **Test in Non-Production First**: Always test migration in dev/staging environment
2. **Run During Low-Traffic Period**: Minimize user impact
3. **Communicate with Teams**: Notify users of migration schedule
4. **Verify Permissions**: Ensure all necessary permissions before starting
5. **Document Custom Changes**: Keep notes on any manual updates needed
6. **Incremental Migration**: Consider migrating objects in batches
7. **Keep Backups**: Maintain backups until migration is fully verified

## Limitations

### Cannot Be Migrated Automatically
- Secret values (security restriction)
- Cluster ACLs (requires manual setup)
- SQL endpoint ACLs
- Legacy Hive metastore tables (requires separate Unity Catalog migration)
- Experiment runs (MLflow)
- Global Init Scripts (admin-level)

### Requires Manual Updates After Migration
- Job cluster IDs
- Notebook paths in jobs
- Git repository credentials
- Secret values
- Instance pool IDs
- Service principal credentials

## Security Considerations

1. **Protect API Tokens**: Never commit tokens to version control
2. **Use Service Principals**: Prefer service principals over user tokens
3. **Rotate Tokens**: Change tokens after migration
4. **Audit Access**: Review who has access to migration scripts
5. **Secure Backups**: Encrypt backup files containing sensitive configs

## Support and Resources

- [Databricks API Documentation](https://docs.databricks.com/dev-tools/api/latest/)
- [Unity Catalog Documentation](https://docs.databricks.com/data-governance/unity-catalog/)
- [Migration Best Practices](https://docs.databricks.com/migration/)

## Version History

- v1.0 (Jan 2026) - Initial release with all migration scripts

## Contact

For issues or questions, please contact your Databricks administrator or platform team.
