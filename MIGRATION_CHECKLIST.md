# Pre-Migration Checklist

## ☑️ Before You Start

### Prerequisites
- [ ] Python 3.8+ installed
- [ ] pip package manager available
- [ ] Git installed (optional, for version control)
- [ ] Access to both source and target Databricks workspaces
- [ ] Admin or appropriate permissions in both workspaces

### Access Preparation
- [ ] Source workspace API token generated
- [ ] Target workspace API token generated
- [ ] Tokens have appropriate permissions:
  - [ ] Workspace access
  - [ ] Cluster management
  - [ ] Job management
  - [ ] Secret scope access
  - [ ] User/group management (SCIM)
  - [ ] Repos management

### Environment Setup
- [ ] Migration scripts downloaded/cloned
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `config.json` created from example
- [ ] Source workspace details added to config
- [ ] Target workspace details added to config
- [ ] Validation script run: `python validate_migration.py`

### Communication
- [ ] Migration date/time scheduled
- [ ] Users notified of upcoming migration
- [ ] Downtime window communicated (if needed)
- [ ] Rollback plan documented
- [ ] Support team briefed

### Backup
- [ ] External backup of source workspace created (optional but recommended)
- [ ] Critical notebooks exported separately
- [ ] Important job definitions documented
- [ ] Secret values documented securely

---

## ☑️ During Migration

### Phase 1: Enablement Objects
- [ ] Run `migrate_users_groups.py`
  - [ ] Verify users created in target
  - [ ] Verify groups created in target
  - [ ] Verify group memberships
  
- [ ] Run `migrate_cluster_policies.py`
  - [ ] Verify policies created
  - [ ] Check policy definitions
  
- [ ] Run `migrate_sql_warehouses.py`
  - [ ] Verify warehouses created
  - [ ] Check warehouse configurations
  
- [ ] Run `migrate_secret_scopes.py`
  - [ ] Verify scopes created
  - [ ] Verify secret keys created (placeholders)
  
- [ ] Run `migrate_workspace_folders.py`
  - [ ] Verify folder structure matches source
  - [ ] Check nested directories

### Phase 2: Content Objects
- [ ] Run `migrate_clusters.py`
  - [ ] Verify clusters created
  - [ ] Check cluster configurations
  
- [ ] Run `migrate_notebooks.py`
  - [ ] Verify notebooks imported
  - [ ] Spot-check notebook contents
  
- [ ] Run `migrate_git_repos.py`
  - [ ] Verify repos created
  - [ ] Check repo URLs and branches

### Phase 3: Orchestration
- [ ] Run `migrate_jobs.py`
  - [ ] Verify jobs created
  - [ ] Check job schedules
  - [ ] Verify multi-task workflows

### Verification
- [ ] Review migration logs for errors
- [ ] Check backup files created
- [ ] Verify object counts match expectations
- [ ] Document any failures or issues

---

## ☑️ After Migration

### Critical: Secret Values
- [ ] List all secret scopes migrated
- [ ] Update each secret with actual values
- [ ] Test secret access from notebooks
- [ ] Verify secret permissions
- [ ] Document which secrets were updated

### Critical: Git Repository Access
- [ ] Re-authenticate each Git repo
- [ ] Test pull operations
- [ ] Test push operations (if applicable)
- [ ] Verify branch/tag is correct
- [ ] Check file synchronization

### Critical: Job Updates
- [ ] Create spreadsheet of all jobs
- [ ] For each job:
  - [ ] Update cluster ID references
  - [ ] Verify notebook paths
  - [ ] Check file/wheel/jar paths
  - [ ] Validate job parameters
  - [ ] Test job dependencies
  - [ ] Verify notification emails
  - [ ] Check webhook URLs
  - [ ] Test run the job
- [ ] Enable job schedules

### Cluster Verification
- [ ] Start one test cluster
- [ ] Verify init scripts run successfully
- [ ] Check library installations
- [ ] Test Spark configurations
- [ ] Verify cluster permissions
- [ ] Start production clusters as needed

### SQL Warehouse Verification
- [ ] Start one test warehouse
- [ ] Run sample SQL queries
- [ ] Check query performance
- [ ] Verify warehouse permissions
- [ ] Start production warehouses as needed

### Notebook Testing
- [ ] Open sample notebooks
- [ ] Attach to test cluster
- [ ] Run cells to verify functionality
- [ ] Check widget parameters work
- [ ] Verify any imported libraries
- [ ] Test notebooks with secrets
- [ ] Test notebooks accessing data

### User Access Testing
- [ ] Invite test users to log in
- [ ] Verify user can access workspace
- [ ] Check user can see their folders
- [ ] Verify user can create/edit notebooks
- [ ] Test user can run jobs
- [ ] Verify proper permissions applied

### Data Access (if applicable)
- [ ] Verify Unity Catalog connections
- [ ] Test table access
- [ ] Check external locations
- [ ] Verify storage credentials
- [ ] Test data queries

### Integration Testing
- [ ] Run end-to-end test workflow
- [ ] Verify job → notebook → data pipeline
- [ ] Test scheduled job execution
- [ ] Check job notifications
- [ ] Verify monitoring/alerting

---

## ☑️ Final Validation

### Functionality Checks
- [ ] Users can log in successfully
- [ ] Notebooks open without errors
- [ ] Clusters start successfully
- [ ] SQL warehouses accept queries
- [ ] Jobs run to completion
- [ ] Git repos pull successfully
- [ ] Secrets work in notebooks/jobs
- [ ] Scheduled jobs trigger correctly

### Performance Checks
- [ ] Cluster start times acceptable
- [ ] Job execution times comparable
- [ ] SQL query performance similar
- [ ] Notebook execution not degraded

### Security Checks
- [ ] User permissions match source
- [ ] Secret access properly restricted
- [ ] Cluster policies enforced
- [ ] ACLs applied correctly
- [ ] Network security maintained

### Documentation
- [ ] Migration report completed
- [ ] Issues encountered documented
- [ ] Manual changes recorded
- [ ] Object ID mappings documented
- [ ] Post-migration configuration saved

---

## ☑️ Go-Live

### Final Steps
- [ ] Notify users migration is complete
- [ ] Provide updated workspace URL
- [ ] Share documentation on changes
- [ ] Point to new job locations
- [ ] Update any hardcoded references
- [ ] Update CI/CD pipelines if applicable

### Monitoring
- [ ] Monitor job execution for 24-48 hours
- [ ] Watch for error alerts
- [ ] Check user feedback
- [ ] Track system performance
- [ ] Review logs regularly

### Cleanup
- [ ] Archive backup files
- [ ] Remove migration scripts from production
- [ ] Rotate API tokens used for migration
- [ ] Update documentation repositories
- [ ] Document lessons learned

---

## ☑️ Rollback Plan (If Needed)

### Decision Points
- [ ] Define success criteria
- [ ] Set rollback decision deadline
- [ ] Identify rollback triggers
- [ ] Document rollback procedure

### Rollback Steps (if required)
- [ ] Notify stakeholders of rollback
- [ ] Redirect users to source workspace
- [ ] Document rollback reasons
- [ ] Plan re-migration approach
- [ ] Address issues identified

---

## ☑️ Post-Migration Review

### 1 Week After
- [ ] Review job success rates
- [ ] Check for recurring errors
- [ ] Gather user feedback
- [ ] Optimize configurations
- [ ] Address any issues

### 1 Month After
- [ ] Conduct post-mortem meeting
- [ ] Document best practices
- [ ] Update migration procedures
- [ ] Archive migration project
- [ ] Celebrate success! 🎉

---

## Emergency Contacts

| Role | Name | Contact |
|------|------|---------|
| Migration Lead | __________ | __________ |
| Databricks Admin | __________ | __________ |
| Platform Team | __________ | __________ |
| Business Team Lead | __________ | __________ |
| Databricks Support | __________ | support@databricks.com |

---

## Notes Section

Use this space to document specific decisions, issues, or important information:

```
Date: _______________
Notes:




```

---

**Remember**: Test thoroughly in non-production before migrating production! 
**Tip**: Take breaks during long migrations. It's a marathon, not a sprint! 
**Success Factor**: Communication is key - keep stakeholders informed throughout!
