#!/usr/bin/env python3
"""
Migrate Cluster Policies from source to target Databricks workspace
"""
import logging
from utils import load_config, get_headers, make_api_request, save_backup, log_migration_result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_cluster_policies(host: str, token: str):
    """List all cluster policies"""
    url = f"{host}/api/2.0/policies/clusters/list"
    headers = get_headers(token)
    try:
        response = make_api_request("GET", url, headers)
        return response.json().get('policies', [])
    except Exception as e:
        logger.error(f"Failed to list cluster policies: {e}")
        return []

def get_cluster_policy(host: str, token: str, policy_id: str):
    """Get details of a specific cluster policy"""
    url = f"{host}/api/2.0/policies/clusters/get"
    headers = get_headers(token)
    data = {"policy_id": policy_id}
    try:
        response = make_api_request("GET", url, headers)
        return response.json()
    except Exception as e:
        logger.error(f"Failed to get cluster policy {policy_id}: {e}")
        return None

def create_cluster_policy(host: str, token: str, policy_config: dict):
    """Create a cluster policy"""
    url = f"{host}/api/2.0/policies/clusters/create"
    headers = get_headers(token)
    
    data = {
        "name": policy_config.get('name'),
        "definition": policy_config.get('definition'),
        "description": policy_config.get('description', ''),
        "max_clusters_per_user": policy_config.get('max_clusters_per_user', 10)
    }
    
    # Add policy family if exists
    if 'policy_family_definition_overrides' in policy_config:
        data['policy_family_definition_overrides'] = policy_config['policy_family_definition_overrides']
    
    try:
        response = make_api_request("POST", url, headers, data)
        logger.info(f"Created cluster policy: {data['name']}")
        return response.json()
    except Exception as e:
        logger.error(f"Failed to create cluster policy {data['name']}: {e}")
        return None

def migrate_cluster_policies():
    """Main migration function for cluster policies"""
    config = load_config()
    source = config['source']
    target = config['target']
    
    logger.info("Starting cluster policy migration...")
    
    # Get cluster policies from source
    logger.info("Fetching cluster policies from source workspace...")
    policies = list_cluster_policies(source['host'], source['token'])
    logger.info(f"Found {len(policies)} cluster policies")
    
    # Get detailed config for each policy
    policy_configs = []
    for policy in policies:
        # Skip built-in policies
        if policy.get('is_default', False):
            logger.info(f"Skipping built-in policy: {policy['name']}")
            continue
            
        policy_id = policy['policy_id']
        config_detail = get_cluster_policy(source['host'], source['token'], policy_id)
        if config_detail:
            policy_configs.append(config_detail)
    
    # Save backup
    save_backup(policy_configs, "cluster_policies")
    
    success_count = 0
    failed_count = 0
    
    # Create policies in target
    for policy_config in policy_configs:
        logger.info(f"Creating cluster policy: {policy_config['name']}")
        
        if create_cluster_policy(target['host'], target['token'], policy_config):
            success_count += 1
        else:
            failed_count += 1
    
    log_migration_result("Cluster Policies", success_count, failed_count)

if __name__ == "__main__":
    migrate_cluster_policies()
