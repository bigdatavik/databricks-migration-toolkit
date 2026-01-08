# Quick Reference: Unity Catalog Workspace Migration

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure workspaces
cp config.json.example config.json
# Edit config.json with your workspace details

# 3. Validate setup
python validate_migration.py

# 4. Run migration
python run_all_migrations.py
```

## Migration Scripts Reference

| Script | Purpose | Dependencies | Manual Actions Required |
|--------|---------|--------------|------------------------|
| `migrate_users_groups.py` | Migrate users and groups | None | None |
| `migrate_cluster_policies.py` | Migrate cluster policies | Users & Groups | None |
| `migrate_sql_warehouses.py` | Migrate SQL warehouses | Users & Groups | Start warehouses |
| `migrate_secret_scopes.py` | Migrate secret scopes | None | **Update all secret values** |
| `migrate_workspace_folders.py` | Migrate folder structure | None | None |
| `migrate_clusters.py` | Migrate all-purpose clusters | Cluster Policies | Start clusters, verify instance pools |
| `migrate_notebooks.py` | Migrate notebooks | Workspace Folders | None |
| `migrate_git_repos.py` | Migrate Git repos | Workspace Folders | **Re-authenticate Git credentials** |
| `migrate_jobs.py` | Migrate jobs/workflows | All above | **Update cluster IDs & paths** |

## Execution Order

```
Phase 1 (Enablement Team):
1. Users & Groups          →  2. Cluster Policies
                              3. SQL Warehouses
                              4. Secret Scopes
                              5. Workspace Folders
                                      ↓
Phase 2 (Business Team):            ↓
6. Clusters  ←──────────────────────┘
7. Notebooks
8. Git Repos
    ↓
Phase 3 (Orchestration):
9. Jobs (depends on everything above)
```

## Command Cheat Sheet

### Individual Migrations
```bash
# Enablement objects
python migrate_users_groups.py
python migrate_cluster_policies.py
python migrate_sql_warehouses.py
python migrate_secret_scopes.py
python migrate_workspace_folders.py

# Business objects
python migrate_clusters.py
python migrate_notebooks.py
python migrate_git_repos.py

# Orchestration
python migrate_jobs.py
```

### All-in-One
```bash
python run_all_migrations.py
```

### Validation
```bash
python validate_migration.py
```

## Critical Post-Migration Tasks

### 1. Secret Scopes (REQUIRED)
```bash
# Via UI: Go to Secrets → Select Scope → Update each secret
# Or via CLI:
databricks secrets put --scope <scope> --key <key>
```

### 2. Git Repos (REQUIRED)
- Go to Repos in target workspace
- Click on each repo
- Re-authenticate with Git provider
- Pull latest changes

### 3. Jobs (REQUIRED)
- Review each job in target workspace
- Update cluster IDs (they change during migration)
- Verify notebook/file paths
- Test run each job

### 4. Clusters (OPTIONAL)
- Start clusters as needed
- Verify init scripts work
- Check installed libraries

### 5. SQL Warehouses (OPTIONAL)
- Start warehouses as needed
- Test queries
- Verify permissions

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `403 Forbidden` | Check API token permissions |
| `Resource already exists` | Delete or rename in target workspace |
| `Policy not found` | Run `migrate_cluster_policies.py` first |
| `Path does not exist` | Run `migrate_workspace_folders.py` first |
| `Invalid cluster specification` | Update cluster IDs in job configs |
| Job fails with "Cluster not found" | Update cluster_id in job settings |
| Notebook not found in job | Update notebook path in job settings |

## File Locations

```
Migration/
├── config.json              # Your workspace configurations (DO NOT COMMIT)
├── requirements.txt         # Python dependencies
├── utils.py                # Shared utility functions
├── validate_migration.py   # Pre-migration validation
├── run_all_migrations.py   # Run all migrations in order
├── migrate_*.py            # Individual migration scripts
├── backup_*.json           # Auto-generated backups (created during migration)
├── README.md               # Project overview
├── MIGRATION_GUIDE.md      # Detailed migration guide
└── QUICK_REFERENCE.md      # This file
```

## Environment Variables (Alternative to config.json)

```bash
# .env file
SOURCE_HOST=https://source-workspace.cloud.databricks.com
SOURCE_TOKEN=dapi_source_token_here
TARGET_HOST=https://target-workspace.cloud.databricks.com
TARGET_TOKEN=dapi_target_token_here
```

## Backup Files

All migrations create automatic backups:
- Format: `backup_<object_type>_YYYYMMDD_HHMMSS.json`
- Location: Current directory
- Use for rollback or reference

## Testing Strategy

```bash
# 1. Test in Dev/Staging first
# Configure dev workspaces in config.json
python run_all_migrations.py

# 2. Verify key objects
# - Check users can log in
# - Test a sample notebook
# - Run a test job
# - Query a SQL warehouse

# 3. Then run in Production
# Update config.json for production workspaces
python run_all_migrations.py
```

## Support

- Detailed Guide: `MIGRATION_GUIDE.md`
- Databricks Docs: https://docs.databricks.com/
- API Reference: https://docs.databricks.com/dev-tools/api/

## Migration Checklist

- [ ] Install requirements (`pip install -r requirements.txt`)
- [ ] Configure `config.json` with workspace details
- [ ] Run validation (`python validate_migration.py`)
- [ ] Backup source workspace (manual/external backup recommended)
- [ ] Run migration (`python run_all_migrations.py`)
- [ ] Update secret values in all secret scopes
- [ ] Re-authenticate Git repositories
- [ ] Update cluster IDs in all jobs
- [ ] Verify and update notebook paths in jobs
- [ ] Test sample notebooks
- [ ] Test sample jobs
- [ ] Start and test SQL warehouses
- [ ] Verify user access and permissions
- [ ] Document any manual changes made
- [ ] Notify users of completion

---

**Remember**: Always test in non-production first! 🚀
