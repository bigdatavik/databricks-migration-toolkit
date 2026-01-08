#!/usr/bin/env python3
"""
Pre-migration validation script to check prerequisites before running migration
"""
import json
import logging
import sys
from utils import load_config, get_headers, make_api_request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_config_exists():
    """Check if config.json exists and is valid"""
    try:
        config = load_config()
        logger.info("✓ Configuration file loaded successfully")
        return True, config
    except FileNotFoundError:
        logger.error("✗ config.json not found")
        return False, None
    except json.JSONDecodeError:
        logger.error("✗ config.json is not valid JSON")
        return False, None

def validate_workspace_connection(host: str, token: str, workspace_name: str):
    """Validate connection to workspace"""
    url = f"{host}/api/2.0/clusters/list"
    headers = get_headers(token)
    
    try:
        response = make_api_request("GET", url, headers)
        logger.info(f"✓ Successfully connected to {workspace_name} workspace")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to connect to {workspace_name} workspace: {e}")
        return False

def check_workspace_permissions(host: str, token: str, workspace_name: str):
    """Check if user has necessary permissions"""
    checks = {
        "Workspace": f"{host}/api/2.0/workspace/list",
        "Clusters": f"{host}/api/2.0/clusters/list",
        "Jobs": f"{host}/api/2.1/jobs/list",
        "Groups": f"{host}/api/2.0/groups/list",
        "Secret Scopes": f"{host}/api/2.0/secrets/scopes/list",
    }
    
    headers = get_headers(token)
    all_passed = True
    
    logger.info(f"\nChecking permissions in {workspace_name} workspace:")
    for check_name, url in checks.items():
        try:
            response = make_api_request("GET", url, headers)
            logger.info(f"  ✓ {check_name} access")
        except Exception as e:
            logger.error(f"  ✗ {check_name} access - {e}")
            all_passed = False
    
    return all_passed

def check_python_packages():
    """Check if required Python packages are installed"""
    required_packages = [
        'requests',
        'databricks'
    ]
    
    all_installed = True
    logger.info("\nChecking Python packages:")
    
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"  ✓ {package} installed")
        except ImportError:
            logger.error(f"  ✗ {package} not installed")
            all_installed = False
    
    return all_installed

def get_workspace_stats(host: str, token: str, workspace_name: str):
    """Get statistics about objects in workspace"""
    logger.info(f"\n{workspace_name} Workspace Statistics:")
    
    stats = {}
    
    # Count groups
    try:
        url = f"{host}/api/2.0/groups/list"
        headers = get_headers(token)
        response = make_api_request("GET", url, headers)
        groups = response.json().get('group_names', [])
        stats['groups'] = len(groups)
        logger.info(f"  Groups: {len(groups)}")
    except:
        logger.warning("  Groups: Unable to retrieve")
    
    # Count clusters
    try:
        url = f"{host}/api/2.0/clusters/list"
        headers = get_headers(token)
        response = make_api_request("GET", url, headers)
        clusters = response.json().get('clusters', [])
        all_purpose = [c for c in clusters if c.get('cluster_source') != 'JOB']
        stats['clusters'] = len(all_purpose)
        logger.info(f"  All-Purpose Clusters: {len(all_purpose)}")
    except:
        logger.warning("  Clusters: Unable to retrieve")
    
    # Count jobs
    try:
        url = f"{host}/api/2.1/jobs/list"
        headers = get_headers(token)
        response = make_api_request("GET", url, headers)
        jobs = response.json().get('jobs', [])
        stats['jobs'] = len(jobs)
        logger.info(f"  Jobs: {len(jobs)}")
    except:
        logger.warning("  Jobs: Unable to retrieve")
    
    # Count secret scopes
    try:
        url = f"{host}/api/2.0/secrets/scopes/list"
        headers = get_headers(token)
        response = make_api_request("GET", url, headers)
        scopes = response.json().get('scopes', [])
        stats['secret_scopes'] = len(scopes)
        logger.info(f"  Secret Scopes: {len(scopes)}")
    except:
        logger.warning("  Secret Scopes: Unable to retrieve")
    
    # Count SQL warehouses
    try:
        url = f"{host}/api/2.0/sql/warehouses"
        headers = get_headers(token)
        response = make_api_request("GET", url, headers)
        warehouses = response.json().get('warehouses', [])
        stats['sql_warehouses'] = len(warehouses)
        logger.info(f"  SQL Warehouses: {len(warehouses)}")
    except:
        logger.warning("  SQL Warehouses: Unable to retrieve")
    
    # Count repos
    try:
        url = f"{host}/api/2.0/repos"
        headers = get_headers(token)
        response = make_api_request("GET", url, headers)
        repos = response.json().get('repos', [])
        stats['git_repos'] = len(repos)
        logger.info(f"  Git Repos: {len(repos)}")
    except:
        logger.warning("  Git Repos: Unable to retrieve")
    
    return stats

def validate_pre_migration():
    """Main validation function"""
    logger.info("="*80)
    logger.info("Pre-Migration Validation Check")
    logger.info("="*80)
    
    all_checks_passed = True
    
    # Check 1: Configuration file
    logger.info("\n[1/6] Checking configuration file...")
    config_valid, config = validate_config_exists()
    if not config_valid:
        logger.error("Please create and configure config.json")
        return False
    all_checks_passed = all_checks_passed and config_valid
    
    # Check 2: Python packages
    logger.info("\n[2/6] Checking Python packages...")
    packages_ok = check_python_packages()
    if not packages_ok:
        logger.error("Please install required packages: pip install -r requirements.txt")
    all_checks_passed = all_checks_passed and packages_ok
    
    # Check 3: Source workspace connection
    logger.info("\n[3/6] Validating source workspace connection...")
    source_connected = validate_workspace_connection(
        config['source']['host'],
        config['source']['token'],
        "source"
    )
    all_checks_passed = all_checks_passed and source_connected
    
    # Check 4: Target workspace connection
    logger.info("\n[4/6] Validating target workspace connection...")
    target_connected = validate_workspace_connection(
        config['target']['host'],
        config['target']['token'],
        "target"
    )
    all_checks_passed = all_checks_passed and target_connected
    
    # Check 5: Source permissions
    if source_connected:
        logger.info("\n[5/6] Checking source workspace permissions...")
        source_perms = check_workspace_permissions(
            config['source']['host'],
            config['source']['token'],
            "source"
        )
        all_checks_passed = all_checks_passed and source_perms
    
    # Check 6: Target permissions
    if target_connected:
        logger.info("\n[6/6] Checking target workspace permissions...")
        target_perms = check_workspace_permissions(
            config['target']['host'],
            config['target']['token'],
            "target"
        )
        all_checks_passed = all_checks_passed and target_perms
    
    # Get statistics
    if source_connected:
        logger.info("\n" + "="*80)
        source_stats = get_workspace_stats(
            config['source']['host'],
            config['source']['token'],
            "Source"
        )
    
    if target_connected:
        logger.info("")
        target_stats = get_workspace_stats(
            config['target']['host'],
            config['target']['token'],
            "Target"
        )
    
    # Final summary
    logger.info("\n" + "="*80)
    logger.info("Validation Summary")
    logger.info("="*80)
    
    if all_checks_passed:
        logger.info("✓ All validation checks passed!")
        logger.info("\nYou can proceed with migration by running:")
        logger.info("  python run_all_migrations.py")
        logger.info("\nOr run individual scripts as needed.")
        return True
    else:
        logger.error("✗ Some validation checks failed")
        logger.error("Please fix the issues above before proceeding with migration")
        return False

if __name__ == "__main__":
    success = validate_pre_migration()
    sys.exit(0 if success else 1)
