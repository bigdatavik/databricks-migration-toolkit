# Unity Catalog Workspace Migration - Complete Toolkit

## 📦 What's Included

This repository contains **9 individual migration scripts** plus supporting utilities to migrate all workspace objects from one Databricks Unity Catalog workspace to another.

## 📂 Project Structure

```
Migration/
│
├── 📋 Documentation
│   ├── README.md                    # Project overview and setup
│   ├── MIGRATION_GUIDE.md           # Detailed migration guide (comprehensive)
│   ├── QUICK_REFERENCE.md           # Quick commands and cheat sheet
│   └── SUMMARY.md                   # This file
│
├── ⚙️ Configuration
│   ├── config.json                  # Workspace connection settings
│   └── requirements.txt             # Python dependencies
│
├── 🔧 Utilities
│   ├── utils.py                     # Shared helper functions
│   ├── validate_migration.py        # Pre-migration validation tool
│   └── run_all_migrations.py        # Execute all migrations in order
│
└── 🔄 Migration Scripts (Individual)
    ├── migrate_users_groups.py      # Users & AD Groups
    ├── migrate_cluster_policies.py  # Cluster Policies
    ├── migrate_sql_warehouses.py    # SQL Warehouses
    ├── migrate_secret_scopes.py     # Secret Scopes
    ├── migrate_workspace_folders.py # Folder Structure
    ├── migrate_clusters.py          # All-Purpose Clusters
    ├── migrate_notebooks.py         # Notebooks
    ├── migrate_git_repos.py         # Git Repository Integrations
    └── migrate_jobs.py              # Jobs/Workflows
```

## 🎯 Migration Coverage

### ✅ Enablement Team Objects
| Object Type | Script | Auto-Complete | Manual Action |
|------------|--------|---------------|---------------|
| AD Groups & Users | `migrate_users_groups.py` | ✅ Yes | None |
| Workspace Folders | `migrate_workspace_folders.py` | ✅ Yes | None |
| Secret Scopes | `migrate_secret_scopes.py` | ⚠️ Structure Only | Update secret values |
| SQL Warehouses | `migrate_sql_warehouses.py` | ✅ Yes | Start warehouses |
| Cluster Policies | `migrate_cluster_policies.py` | ✅ Yes | None |

### ✅ Business/App Team Objects
| Object Type | Quantity (Example) | Script | Auto-Complete | Manual Action |
|------------|----------|--------|---------------|---------------|
| All-Purpose Clusters | 2 | `migrate_clusters.py` | ✅ Yes | Start clusters |
| Job Clusters | N/A* | Included in jobs | ✅ Yes | Via job migration |
| Notebooks | 1+ | `migrate_notebooks.py` | ✅ Yes | None |
| Secrets in Scopes | 1 | `migrate_secret_scopes.py` | ⚠️ Placeholder | Update values |
| Jobs/Workflows | 600/business (2) | `migrate_jobs.py` | ⚠️ Structure | Update cluster IDs |
| Git Repos | 3 | `migrate_git_repos.py` | ✅ Structure | Re-auth credentials |

*Job clusters are part of job definitions and migrate with jobs.

## 🚀 Quick Start (3 Steps)

### Step 1: Setup
```bash
pip install -r requirements.txt
```

### Step 2: Configure
Edit `config.json`:
```json
{
  "source": {
    "host": "https://your-source.cloud.databricks.com",
    "token": "dapi_your_source_token"
  },
  "target": {
    "host": "https://your-target.cloud.databricks.com",
    "token": "dapi_your_target_token"
  }
}
```

### Step 3: Migrate
```bash
# Validate first
python validate_migration.py

# Run all migrations
python run_all_migrations.py
```

## 🔄 Migration Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 1: FOUNDATION                      │
│                  (Enablement Team Objects)                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌──────────────────────────────────────┐
        │  1. Users & Groups                   │ ← Run First
        └──────────────────────────────────────┘
                              ↓
        ┌──────────────────────────────────────┐
        │  2. Cluster Policies                 │
        │  3. SQL Warehouses                   │ ← Can run in parallel
        │  4. Secret Scopes                    │
        │  5. Workspace Folders                │
        └──────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   PHASE 2: CONTENT                          │
│                  (Business Team Objects)                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌──────────────────────────────────────┐
        │  6. All-Purpose Clusters             │
        │  7. Notebooks                        │ ← Can run in parallel
        │  8. Git Repos                        │
        └──────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  PHASE 3: ORCHESTRATION                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌──────────────────────────────────────┐
        │  9. Jobs/Workflows                   │ ← Run Last
        └──────────────────────────────────────┘
```

## ⚠️ Critical Post-Migration Actions

### 🔴 REQUIRED (Must Do)
1. **Update Secret Values** - Placeholders created, need real values
2. **Re-authenticate Git Repos** - Credentials don't migrate
3. **Update Job Cluster IDs** - Cluster IDs change in migration
4. **Verify Job Paths** - Check all notebook/file paths in jobs

### 🟡 RECOMMENDED (Should Do)
5. **Test Sample Jobs** - Run test workflows to verify
6. **Start SQL Warehouses** - They migrate in STOPPED state
7. **Start Clusters** - They migrate in TERMINATED state
8. **Verify User Access** - Ensure users can log in and access resources

## 📊 Features

### ✅ What Works Automatically
- Complete workspace structure recreation
- All configurations preserved
- Automatic backups before migration
- Progress logging and error handling
- Dependency order management
- Support for 1000+ objects

### ⚠️ What Needs Manual Intervention
- Secret values (API limitation - can't read secrets)
- Git credentials (security - can't migrate)
- Job cluster references (IDs change)
- Testing and verification

## 🛡️ Safety Features

1. **Automatic Backups**: Every migration creates `backup_*.json` files
2. **Validation Tool**: Check prerequisites before migrating
3. **Dry Run Support**: Test without making changes (in config)
4. **Detailed Logging**: Track every operation
5. **Error Handling**: Graceful failures with clear messages

## 📈 Scale

These scripts handle:
- ✅ 600+ jobs per business team
- ✅ Multiple notebooks and repos
- ✅ Complex cluster configurations
- ✅ Large workspace structures
- ✅ Numerous users and groups

## 🔒 Security

- API tokens never logged
- Secrets handled securely (placeholders only)
- Backup files can be encrypted
- Git credentials require re-authentication
- Follows Databricks security best practices

## 📚 Documentation Hierarchy

1. **SUMMARY.md** (this file) - Overview and visual guide
2. **QUICK_REFERENCE.md** - Commands and cheat sheet
3. **README.md** - Setup and basic usage
4. **MIGRATION_GUIDE.md** - Comprehensive detailed guide

## 🆘 Getting Help

**Issue**: Connection fails
→ **Solution**: Run `python validate_migration.py`

**Issue**: Object already exists
→ **Solution**: Delete from target or rename

**Issue**: Job fails after migration
→ **Solution**: Update cluster IDs in job settings

**Issue**: Permission denied
→ **Solution**: Verify API token has admin permissions

For detailed troubleshooting, see `MIGRATION_GUIDE.md` section "Troubleshooting"

## 📝 License & Usage

These scripts are designed for Databricks Unity Catalog workspace migrations.
Always test in non-production environments first!

## 🎉 Success Criteria

Your migration is complete when:
- ✅ All scripts run without errors
- ✅ Users can log into target workspace
- ✅ Notebooks open and run successfully
- ✅ Test jobs execute without issues
- ✅ SQL warehouses query correctly
- ✅ Git repos can pull/push
- ✅ Secrets are updated and working

---

**Ready to migrate?** Start with `python validate_migration.py` 🚀
