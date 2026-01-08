#!/usr/bin/env python3
"""
Migrate Clusters (All-Purpose) from source to target Databricks workspace
Note: Job clusters are migrated as part of job definitions
"""
import logging
from utils import load_config, get_headers, make_api_request, save_backup, log_migration_result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_clusters(host: str, token: str):
    """List all clusters"""
    url = f"{host}/api/2.0/clusters/list"
    headers = get_headers(token)
    try:
        response = make_api_request("GET", url, headers)
        return response.json().get('clusters', [])
    except Exception as e:
        logger.error(f"Failed to list clusters: {e}")
        return []

def get_cluster(host: str, token: str, cluster_id: str):
    """Get details of a specific cluster"""
    url = f"{host}/api/2.0/clusters/get"
    headers = get_headers(token)
    data = {"cluster_id": cluster_id}
    try:
        response = make_api_request("GET", url, headers)
        return response.json()
    except Exception as e:
        logger.error(f"Failed to get cluster {cluster_id}: {e}")
        return None

def create_cluster(host: str, token: str, cluster_config: dict):
    """Create a cluster"""
    url = f"{host}/api/2.0/clusters/create"
    headers = get_headers(token)
    
    # Extract relevant configuration (remove runtime-specific fields)
    data = {
        "cluster_name": cluster_config.get('cluster_name'),
        "spark_version": cluster_config.get('spark_version'),
        "node_type_id": cluster_config.get('node_type_id'),
        "driver_node_type_id": cluster_config.get('driver_node_type_id'),
        "autoscale": cluster_config.get('autoscale'),
        "num_workers": cluster_config.get('num_workers'),
        "autotermination_minutes": cluster_config.get('autotermination_minutes', 120),
        "spark_conf": cluster_config.get('spark_conf', {}),
        "spark_env_vars": cluster_config.get('spark_env_vars', {}),
        "custom_tags": cluster_config.get('custom_tags', {}),
        "cluster_log_conf": cluster_config.get('cluster_log_conf'),
        "init_scripts": cluster_config.get('init_scripts', []),
        "ssh_public_keys": cluster_config.get('ssh_public_keys', []),
        "enable_elastic_disk": cluster_config.get('enable_elastic_disk', True),
        "enable_local_disk_encryption": cluster_config.get('enable_local_disk_encryption', False),
        "runtime_engine": cluster_config.get('runtime_engine', 'STANDARD')
    }
    
    # Add policy if exists
    if 'policy_id' in cluster_config:
        data['policy_id'] = cluster_config['policy_id']
    
    # Add instance pool if exists
    if 'instance_pool_id' in cluster_config:
        data['instance_pool_id'] = cluster_config['instance_pool_id']
    
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}
    
    try:
        response = make_api_request("POST", url, headers, data)
        logger.info(f"Created cluster: {data['cluster_name']}")
        return response.json()
    except Exception as e:
        logger.error(f"Failed to create cluster {data['cluster_name']}: {e}")
        return None

def migrate_clusters():
    """Main migration function for clusters"""
    config = load_config()
    source = config['source']
    target = config['target']
    
    logger.info("Starting cluster migration...")
    
    # Get clusters from source
    logger.info("Fetching clusters from source workspace...")
    clusters = list_clusters(source['host'], source['token'])
    logger.info(f"Found {len(clusters)} clusters")
    
    # Filter only all-purpose clusters (exclude job clusters)
    all_purpose_clusters = [c for c in clusters if c.get('cluster_source') != 'JOB']
    logger.info(f"Found {len(all_purpose_clusters)} all-purpose clusters")
    
    # Get detailed config for each cluster
    cluster_configs = []
    for cluster in all_purpose_clusters:
        cluster_id = cluster['cluster_id']
        config_detail = get_cluster(source['host'], source['token'], cluster_id)
        if config_detail:
            cluster_configs.append(config_detail)
    
    # Save backup
    save_backup(cluster_configs, "clusters")
    
    success_count = 0
    failed_count = 0
    
    # Create clusters in target (they will be in TERMINATED state)
    for cluster_config in cluster_configs:
        logger.info(f"Creating cluster: {cluster_config['cluster_name']}")
        
        if create_cluster(target['host'], target['token'], cluster_config):
            success_count += 1
        else:
            failed_count += 1
    
    log_migration_result("Clusters", success_count, failed_count)
    logger.info("Note: Clusters created in TERMINATED state. Start them manually as needed.")

if __name__ == "__main__":
    migrate_clusters()
