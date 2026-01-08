# Migration Scripts Detailed Reference

## Individual Migration Scripts

### 1. migrate_users_groups.py
**Purpose**: Migrate Active Directory groups and user accounts

**What it does**:
- Retrieves all groups from source workspace
- Creates groups in target workspace
- Fetches group membership information
- Adds users to target workspace using SCIM API
- Assigns users to appropriate groups
- Preserves group hierarchy and relationships

**API Endpoints Used**:
- `/api/2.0/groups/list` - List groups
- `/api/2.0/groups/create` - Create groups
- `/api/2.0/groups/list-members` - Get group members
- `/api/2.0/groups/add-member` - Add members to groups
- `/api/2.0/preview/scim/v2/Users` - Create users

**Dependencies**: None (should run first)

**Manual Actions After**: None

**Important Notes**:
- Password-based users may need to reset passwords
- External identity providers (AAD, Okta) need separate configuration
- Service principals require separate migration

---

### 2. migrate_workspace_folders.py
**Purpose**: Recreate workspace folder hierarchy

**What it does**:
- Recursively scans source workspace directory structure
- Identifies all folders (excludes files)
- Creates matching folder structure in target workspace
- Preserves parent-child relationships

**API Endpoints Used**:
- `/api/2.0/workspace/list` - List workspace objects
- `/api/2.0/workspace/mkdirs` - Create directories

**Dependencies**: None

**Manual Actions After**: None

**Important Notes**:
- Only creates folders, not contents
- Run before notebook migration
- Does not migrate folder permissions/ACLs

---

### 3. migrate_secret_scopes.py
**Purpose**: Migrate secret scope structure and secret keys

**What it does**:
- Lists all secret scopes from source
- Identifies secrets within each scope (keys only, not values)
- Creates scopes in target workspace
- Creates placeholder secrets with dummy values
- Preserves scope backend type (Databricks-backed or Azure Key Vault-backed)

**API Endpoints Used**:
- `/api/2.0/secrets/scopes/list` - List secret scopes
- `/api/2.0/secrets/list` - List secrets in scope
- `/api/2.0/secrets/scopes/create` - Create secret scope
- `/api/2.0/secrets/put` - Create secret

**Dependencies**: None

**Manual Actions After**: 
- ⚠️ **CRITICAL**: Update all secret values manually
- Secret values cannot be read via API (security restriction)
- Placeholder value: "PLACEHOLDER_PLEASE_UPDATE"

**Important Notes**:
- Azure Key Vault-backed scopes need vault configuration
- ACLs on scopes are not migrated

---

### 4. migrate_sql_warehouses.py
**Purpose**: Migrate SQL Warehouse (formerly SQL Endpoints) configurations

**What it does**:
- Lists all SQL warehouses from source
- Retrieves detailed configuration for each warehouse
- Extracts settings: size, scaling, auto-stop, Photon, serverless
- Creates warehouses in target workspace
- Preserves tags and custom configurations

**API Endpoints Used**:
- `/api/2.0/sql/warehouses` - List warehouses
- `/api/2.0/sql/warehouses/{id}` - Get warehouse details
- `/api/2.0/sql/warehouses` (POST) - Create warehouse

**Dependencies**: Users & Groups (for ownership)

**Manual Actions After**: 
- Start warehouses (created in STOPPED state)
- Verify query performance
- Configure access permissions

**Important Notes**:
- Warehouses are created but not started (cost control)
- Photon and serverless settings preserved
- Channel/version settings migrated

---

### 5. migrate_cluster_policies.py
**Purpose**: Migrate cluster governance policies

**What it does**:
- Lists all cluster policies from source
- Filters out built-in/default policies
- Extracts policy definitions (JSON constraints)
- Creates policies in target workspace
- Preserves policy limits and restrictions

**API Endpoints Used**:
- `/api/2.0/policies/clusters/list` - List policies
- `/api/2.0/policies/clusters/get` - Get policy details
- `/api/2.0/policies/clusters/create` - Create policy

**Dependencies**: None (but should run before cluster migration)

**Manual Actions After**: None

**Important Notes**:
- Built-in policies are skipped (recreated automatically by Databricks)
- Policy IDs will change (mapping may be needed for clusters)
- Policy family definitions are preserved

---

### 6. migrate_clusters.py
**Purpose**: Migrate all-purpose (interactive) clusters

**What it does**:
- Lists all clusters from source workspace
- Filters to only all-purpose clusters (excludes job clusters)
- Retrieves detailed configuration for each cluster
- Extracts: instance types, scaling, Spark configs, init scripts, libraries
- Creates clusters in target workspace
- Preserves custom tags and configurations

**API Endpoints Used**:
- `/api/2.0/clusters/list` - List clusters
- `/api/2.0/clusters/get` - Get cluster details
- `/api/2.0/clusters/create` - Create cluster

**Dependencies**: 
- Cluster Policies (if clusters use policies)
- Instance Pools (if clusters use pools - requires mapping)

**Manual Actions After**: 
- Start clusters as needed (created in TERMINATED state)
- Verify init scripts execute correctly
- Check library installations
- Update instance pool IDs if used

**Important Notes**:
- Clusters created but not started (cost control)
- Job clusters migrate with job definitions
- Instance pool IDs may need manual mapping
- Libraries on clusters are preserved in config

---

### 7. migrate_notebooks.py
**Purpose**: Migrate Jupyter-style notebooks with all code

**What it does**:
- Recursively scans workspace for notebooks
- Exports notebooks in SOURCE format (preserves all code)
- Supports all languages: Python, SQL, Scala, R
- Imports notebooks to target workspace
- Preserves notebook metadata and cell outputs

**API Endpoints Used**:
- `/api/2.0/workspace/list` - List workspace objects
- `/api/2.0/workspace/export` - Export notebook
- `/api/2.0/workspace/import` - Import notebook

**Dependencies**: Workspace Folders (folders must exist first)

**Manual Actions After**: 
- Test notebooks run correctly
- Verify attached clusters work
- Check any hardcoded paths/URLs

**Important Notes**:
- Notebook revisions/history not migrated
- Widget parameters preserved
- Comments and markdown cells included
- Binary content (images) is preserved

---

### 8. migrate_git_repos.py
**Purpose**: Migrate Git repository integrations

**What it does**:
- Lists all connected Git repos from source
- Retrieves repo configuration: URL, provider, branch/tag
- Creates repo connections in target workspace
- Preserves repo paths and branch information
- Supports: GitHub, GitLab, Azure DevOps, Bitbucket

**API Endpoints Used**:
- `/api/2.0/repos` - List repos
- `/api/2.0/repos/{id}` - Get repo details
- `/api/2.0/repos` (POST) - Create repo

**Dependencies**: Workspace Folders

**Manual Actions After**: 
- ⚠️ **CRITICAL**: Re-authenticate with Git provider
- Test pull operations
- Verify branch/tag is correct
- Check read/write permissions

**Important Notes**:
- Git credentials do NOT migrate (security)
- Personal access tokens must be re-entered
- SSH keys need to be reconfigured
- Repo is cloned fresh in target workspace

---

### 9. migrate_jobs.py
**Purpose**: Migrate workflows, scheduled jobs, and pipelines

**What it does**:
- Lists all jobs from source workspace (paginated)
- Retrieves complete job definitions
- Extracts: tasks, schedules, dependencies, parameters
- Migrates job cluster definitions (embedded)
- Creates jobs in target workspace
- Preserves: schedules, notifications, timeouts, retries

**API Endpoints Used**:
- `/api/2.1/jobs/list` - List jobs
- `/api/2.1/jobs/get` - Get job details
- `/api/2.1/jobs/create` - Create job

**Dependencies**: ALL previous migrations
- Requires notebooks to exist
- Requires clusters/policies for cluster references
- Requires Git repos if jobs use repo files

**Manual Actions After**: 
- ⚠️ **CRITICAL**: Update all cluster IDs (IDs change in migration)
- Verify notebook paths are correct
- Check file paths for wheel/jar tasks
- Test run each job
- Verify job parameters
- Check email notification addresses
- Validate webhook URLs

**Important Notes**:
- Jobs created in PAUSED state
- Job runs history is NOT migrated
- Job cluster definitions are embedded in job config
- Multi-task workflows fully supported
- Parameters and widgets preserved
- Schedules preserved but may need time zone adjustment

---

## Utility Scripts

### validate_migration.py
**Purpose**: Pre-migration validation and readiness check

**What it does**:
- Validates config.json exists and is valid JSON
- Tests connectivity to source workspace
- Tests connectivity to target workspace
- Checks API token permissions in both workspaces
- Verifies Python dependencies are installed
- Generates statistics on objects to migrate
- Provides go/no-go decision

**Usage**: Run BEFORE starting migration

---

### run_all_migrations.py
**Purpose**: Orchestrate complete migration in correct order

**What it does**:
- Runs all 9 migration scripts in dependency order
- Provides progress tracking
- Handles errors gracefully with continue/abort option
- Generates comprehensive summary report
- Tracks migration duration
- Lists post-migration action items

**Usage**: Run for complete workspace migration

---

### utils.py
**Purpose**: Shared utility functions for all migration scripts

**What it provides**:
- Configuration loading
- HTTP request handling with retries
- Error logging and formatting
- Backup file creation
- API header generation
- Common helper functions

**Usage**: Imported by all migration scripts (not run directly)

---

## API Versions Used

| Object Type | API Version | Notes |
|-------------|-------------|-------|
| Groups & Users | 2.0 | Stable API |
| SCIM Users | 2.0 (preview) | For user creation |
| Workspace | 2.0 | Stable API |
| Secrets | 2.0 | Stable API |
| Clusters | 2.0 | Stable API |
| Cluster Policies | 2.0 | Stable API |
| SQL Warehouses | 2.0 | Stable API |
| Repos | 2.0 | Stable API |
| Jobs | 2.1 | Latest job API version |

---

## Common Parameters

All scripts use:
- `config.json` for workspace configuration
- Automatic backup with timestamp
- Consistent logging format
- Error handling with detailed messages
- Success/failure counters

---

## Error Handling

Each script includes:
- Try-catch blocks for API calls
- Detailed error logging with request/response
- Continues processing remaining objects on single failures
- Final summary with success/failure counts
- Backup files created before any changes

---

## Performance Considerations

| Script | Time Complexity | Notes |
|--------|----------------|-------|
| Users & Groups | O(n*m) | n=groups, m=members per group |
| Workspace Folders | O(d) | d=directory depth (recursive) |
| Secret Scopes | O(s*k) | s=scopes, k=keys per scope |
| SQL Warehouses | O(w) | w=number of warehouses |
| Cluster Policies | O(p) | p=number of policies |
| Clusters | O(c) | c=number of clusters |
| Notebooks | O(n*d) | n=notebooks, d=depth (recursive) |
| Git Repos | O(r) | r=number of repos |
| Jobs | O(j) | j=number of jobs (paginated) |

**Optimization tip**: For large workspaces (1000+ objects), consider running scripts during off-peak hours.

---

## Logging

All scripts log to console with format:
```
TIMESTAMP - SCRIPT_NAME - LEVEL - MESSAGE
```

Levels:
- **INFO**: Normal operation progress
- **WARNING**: Non-critical issues (e.g., secret placeholders)
- **ERROR**: Failures that don't stop execution
- **CRITICAL**: Failures that stop execution

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success - all objects migrated |
| 1 | Partial failure - some objects failed |
| 2 | Configuration error |
| 3 | Authentication error |

---

**For detailed usage of any script, run**: `python <script_name>.py --help`
