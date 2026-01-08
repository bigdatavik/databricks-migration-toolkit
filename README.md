# 🚀 Unity Catalog Workspace Migration Toolkit

> **Complete solution for migrating Databricks Unity Catalog workspaces from one environment to another**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Terraform](https://img.shields.io/badge/terraform-1.0+-purple.svg)](https://www.terraform.io/)
[![Databricks](https://img.shields.io/badge/Databricks-Unity%20Catalog-orange.svg)](https://www.databricks.com/)

## 🎯 Two Approaches Available

This toolkit provides **TWO migration approaches**:

1. **🐍 Python Scripts** (Root directory) - Fast, imperative, script-based migration
   - ✅ Best for: One-time migrations, quick setup
   - ✅ Easier to learn and customize

2. **🏗️ Terraform** (`/terraform` directory) - Declarative Infrastructure as Code
   - ✅ Best for: Ongoing management, multi-environment
   - ✅ State management and drift detection

**Not sure which to use?** See [PYTHON_VS_TERRAFORM.md](PYTHON_VS_TERRAFORM.md) for detailed comparison.

## 📋 What This Does

Migrate all workspace objects between Databricks Unity Catalog workspaces:
- ✅ Users & Groups
- ✅ Notebooks (all languages)
- ✅ Jobs & Workflows (600+ supported)
- ✅ Clusters & Policies
- ✅ SQL Warehouses
- ✅ Secret Scopes
- ✅ Git Repository Integrations
- ✅ Workspace Folder Structure

## 🎯 Quick Start

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Configure
```bash
# Copy example config
cp config.example.json config.json

# Edit with your workspace details
nano config.json
```

Required configuration:
```json
{
  "source": {
    "host": "https://your-source-workspace.cloud.databricks.com",
    "token": "dapi_your_source_token"
  },
  "target": {
    "host": "https://your-target-workspace.cloud.databricks.com",
    "token": "dapi_your_target_token"
  }
}
```

### 3. Validate
```bash
python validate_migration.py
```

### 4. Migrate
```bash
# Option A: Run all migrations
python run_all_migrations.py

# Option B: Run individually
python migrate_users_groups.py
python migrate_notebooks.py
# ... etc
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[INDEX.md](INDEX.md)** | 📑 Documentation navigator |
| **[SUMMARY.md](SUMMARY.md)** | 📊 Overview & architecture |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | ⚡ Command cheat sheet |
| **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** | 📖 Complete detailed guide |
| **[MIGRATION_CHECKLIST.md](MIGRATION_CHECKLIST.md)** | ☑️ Step-by-step checklist |
| **[SCRIPTS_REFERENCE.md](SCRIPTS_REFERENCE.md)** | 🔧 Technical script docs |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | 🏗️ Visual diagrams |

**New to migration?** Start with [SUMMARY.md](SUMMARY.md) → [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)

**Quick commands needed?** Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**Complete navigation?** See [INDEX.md](INDEX.md)

## 🔄 Migration Process

```
Phase 1: Foundation          Phase 2: Content           Phase 3: Orchestration
─────────────────────       ─────────────────          ──────────────────────
1. Users & Groups      →    6. Clusters           →    9. Jobs/Workflows
2. Cluster Policies    →    7. Notebooks          →       (depends on all)
3. SQL Warehouses      →    8. Git Repos          →
4. Secret Scopes       →
5. Workspace Folders   →
```

**Total Time**: ~6-7 hours for typical workspace (adjust based on object count)

## 📦 What's Included

### Migration Scripts (9)
- `migrate_users_groups.py` - Users and AD groups
- `migrate_cluster_policies.py` - Governance policies
- `migrate_sql_warehouses.py` - SQL compute resources
- `migrate_secret_scopes.py` - Secret management
- `migrate_workspace_folders.py` - Directory structure
- `migrate_clusters.py` - All-purpose clusters
- `migrate_notebooks.py` - Jupyter notebooks
- `migrate_git_repos.py` - Git integrations
- `migrate_jobs.py` - Workflows and schedules

### Utilities
- `validate_migration.py` - Pre-flight checks
- `run_all_migrations.py` - Orchestrate all migrations
- `utils.py` - Shared helper functions

### Configuration
- `config.json` - Your workspace settings
- `config.example.json` - Configuration template
- `requirements.txt` - Python dependencies

## ⚠️ Critical Post-Migration Actions

After migration completes, you MUST:

1. **Update Secret Values** 🔴 REQUIRED
   - Placeholders created, need real values
   - Cannot be read from source (API limitation)

2. **Re-authenticate Git Repos** 🔴 REQUIRED
   - Credentials don't migrate (security)
   - Re-enter personal access tokens

3. **Update Job Cluster IDs** 🔴 REQUIRED
   - Cluster IDs change during migration
   - Update references in all jobs

4. **Test Workflows** 🟡 RECOMMENDED
   - Run sample jobs to verify
   - Check notebook execution

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md#post-migration-steps) for details.

## 🛡️ Safety Features

- ✅ Automatic backups before migration (`backup_*.json` files)
- ✅ Pre-migration validation tool
- ✅ Detailed logging with error tracking
- ✅ Continue on error option (optional)
- ✅ Dry-run mode available

## 📊 Scale

Handles enterprise workspaces:
- 600+ jobs per business team
- 100+ notebooks
- Multiple clusters and warehouses
- Complex folder hierarchies
- Large user/group structures

## 🔒 Security

- API tokens never logged
- Secret values handled securely (placeholders only)
- Git credentials require re-authentication
- Follows Databricks best practices
- Backup files can be encrypted

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection fails | Run `python validate_migration.py` |
| Permission denied | Verify API token has admin permissions |
| Object already exists | Delete from target or enable overwrite |
| Job fails after migration | Update cluster IDs in job settings |

Full troubleshooting guide: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md#troubleshooting)

## 📋 Prerequisites

**Access Requirements:**
- Admin or appropriate permissions in both workspaces
- API tokens for both source and target workspaces
- Network access to both Databricks workspaces

**Software Requirements:**
- Python 3.8 or higher
- pip package manager
- Git (optional, for version control)

**Permissions Needed:**
- Workspace access
- Cluster management
- Job management
- Secret scope access
- User/group management (SCIM API)
- Repos management

## 💻 System Requirements

- **OS**: macOS, Linux, or Windows with Python
- **Memory**: 1GB+ recommended
- **Disk**: 500MB+ free space (for backups)
- **Network**: Stable internet connection

## 🎓 Example Usage

### Complete Migration
```bash
# Validate setup
python validate_migration.py

# Run all migrations
python run_all_migrations.py

# Review logs and backups
ls backup_*.json
```

### Individual Migration
```bash
# Migrate only notebooks
python migrate_notebooks.py

# Migrate only jobs
python migrate_jobs.py
```

### Check Progress
All scripts provide progress output:
```
2026-01-08 10:30:00 - migrate_notebooks - INFO - Starting notebook migration...
2026-01-08 10:30:05 - migrate_notebooks - INFO - Found 123 notebooks
2026-01-08 10:30:10 - migrate_notebooks - INFO - Exporting notebook: /Users/john/analysis.py
...
2026-01-08 10:35:00 - migrate_notebooks - INFO - Migration completed
2026-01-08 10:35:00 - migrate_notebooks - INFO -   Success: 123
2026-01-08 10:35:00 - migrate_notebooks - INFO -   Failed: 0
```

## 🤝 Support

1. Check documentation (see [INDEX.md](INDEX.md))
2. Review troubleshooting guide ([MIGRATION_GUIDE.md](MIGRATION_GUIDE.md))
3. Examine backup files created during migration
4. Check detailed logs in console output

## 📄 License

This toolkit is designed for Databricks Unity Catalog workspace migrations.

## ⚡ Quick Links

- [Full Migration Guide](MIGRATION_GUIDE.md) - Comprehensive instructions
- [Command Reference](QUICK_REFERENCE.md) - Quick command lookups
- [Migration Checklist](MIGRATION_CHECKLIST.md) - Track your progress
- [Architecture Diagrams](ARCHITECTURE.md) - Visual workflow
- [Script Details](SCRIPTS_REFERENCE.md) - Technical documentation

## 🎯 Success Criteria

Your migration is successful when:
- ✅ All 9 migration scripts complete without errors
- ✅ Users can log into target workspace
- ✅ Notebooks open and run correctly
- ✅ Test jobs execute successfully
- ✅ SQL warehouses process queries
- ✅ Git repos can pull/push
- ✅ Secrets are working in notebooks/jobs

## ⚠️ Important Notes

- **Always test in non-production first!**
- Secret values must be re-entered manually (API security limitation)
- Git credentials must be re-authenticated (security)
- Job cluster IDs need updating after migration (IDs change)
- Review [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for limitations

## 🚀 Ready to Migrate?

```bash
# 1. Review the summary
cat SUMMARY.md

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure workspaces
cp config.example.json config.json
nano config.json

# 4. Validate setup
python validate_migration.py

# 5. Start migration
python run_all_migrations.py

# 6. Follow checklist
cat MIGRATION_CHECKLIST.md
```

---

**Questions?** See [INDEX.md](INDEX.md) for complete documentation navigation.

**Need help?** Check [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) troubleshooting section.

**Want quick commands?** See [QUICK_REFERENCE.md](QUICK_REFERENCE.md).

*Happy Migrating! 🎉*
