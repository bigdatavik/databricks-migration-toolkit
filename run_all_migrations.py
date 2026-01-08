#!/usr/bin/env python3
"""
Run all migration scripts in the correct order
"""
import logging
import sys
from datetime import datetime

# Import all migration modules
from migrate_users_groups import migrate_users_and_groups
from migrate_cluster_policies import migrate_cluster_policies
from migrate_sql_warehouses import migrate_sql_warehouses
from migrate_secret_scopes import migrate_secret_scopes
from migrate_workspace_folders import migrate_workspace_folders
from migrate_clusters import migrate_clusters
from migrate_notebooks import migrate_notebooks
from migrate_git_repos import migrate_git_repos
from migrate_jobs import migrate_jobs

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_all_migrations():
    """Run all migrations in the correct order"""
    start_time = datetime.now()
    logger.info("="*80)
    logger.info("Starting complete workspace migration")
    logger.info("="*80)
    
    migrations = [
        ("Users & Groups", migrate_users_and_groups),
        ("Cluster Policies", migrate_cluster_policies),
        ("SQL Warehouses", migrate_sql_warehouses),
        ("Secret Scopes", migrate_secret_scopes),
        ("Workspace Folders", migrate_workspace_folders),
        ("Clusters", migrate_clusters),
        ("Notebooks", migrate_notebooks),
        ("Git Repos", migrate_git_repos),
        ("Jobs", migrate_jobs)
    ]
    
    results = []
    
    for name, migration_func in migrations:
        logger.info(f"\n{'='*80}")
        logger.info(f"Starting migration: {name}")
        logger.info(f"{'='*80}")
        
        try:
            migration_func()
            results.append((name, "SUCCESS"))
            logger.info(f"✓ Completed migration: {name}")
        except Exception as e:
            logger.error(f"✗ Failed migration: {name}")
            logger.error(f"Error: {e}")
            results.append((name, f"FAILED: {e}"))
            
            # Ask if user wants to continue
            response = input(f"\nMigration '{name}' failed. Continue with next migration? (y/n): ")
            if response.lower() != 'y':
                logger.info("Migration process stopped by user")
                break
    
    # Print summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    logger.info(f"\n{'='*80}")
    logger.info("Migration Summary")
    logger.info(f"{'='*80}")
    logger.info(f"Start time: {start_time}")
    logger.info(f"End time: {end_time}")
    logger.info(f"Duration: {duration}")
    logger.info(f"\nResults:")
    
    for name, status in results:
        logger.info(f"  {name}: {status}")
    
    logger.info(f"\n{'='*80}")
    logger.info("IMPORTANT POST-MIGRATION STEPS:")
    logger.info("1. Update secret values in secret scopes (placeholders were created)")
    logger.info("2. Review and update cluster IDs in jobs")
    logger.info("3. Verify notebook paths in jobs are correct")
    logger.info("4. Test SQL warehouses and start them if needed")
    logger.info("5. Test all-purpose clusters and start them if needed")
    logger.info("6. Verify Git repo credentials are configured")
    logger.info("7. Run test jobs to ensure everything works")
    logger.info(f"{'='*80}")

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   Databricks Unity Catalog Workspace Migration Tool         ║
    ╚══════════════════════════════════════════════════════════════╝
    
    This will migrate all workspace objects from source to target.
    
    Please ensure:
    - config.json is properly configured
    - You have appropriate permissions in both workspaces
    - You have backed up important data
    
    """)
    
    response = input("Continue with migration? (yes/no): ")
    if response.lower() == 'yes':
        run_all_migrations()
    else:
        logger.info("Migration cancelled by user")
        sys.exit(0)
