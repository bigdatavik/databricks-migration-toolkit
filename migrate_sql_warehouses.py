#!/usr/bin/env python3
"""
Migrate SQL Warehouses from source to target Databricks workspace
"""
import logging
from utils import load_config, get_headers, make_api_request, save_backup, log_migration_result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_sql_warehouses(host: str, token: str):
    """List all SQL warehouses"""
    url = f"{host}/api/2.0/sql/warehouses"
    headers = get_headers(token)
    try:
        response = make_api_request("GET", url, headers)
        return response.json().get('warehouses', [])
    except Exception as e:
        logger.error(f"Failed to list SQL warehouses: {e}")
        return []

def get_sql_warehouse(host: str, token: str, warehouse_id: str):
    """Get details of a specific SQL warehouse"""
    url = f"{host}/api/2.0/sql/warehouses/{warehouse_id}"
    headers = get_headers(token)
    try:
        response = make_api_request("GET", url, headers)
        return response.json()
    except Exception as e:
        logger.error(f"Failed to get SQL warehouse {warehouse_id}: {e}")
        return None

def create_sql_warehouse(host: str, token: str, warehouse_config: dict):
    """Create a SQL warehouse"""
    url = f"{host}/api/2.0/sql/warehouses"
    headers = get_headers(token)
    
    # Extract relevant configuration (remove runtime-specific fields)
    data = {
        "name": warehouse_config.get('name'),
        "cluster_size": warehouse_config.get('cluster_size'),
        "min_num_clusters": warehouse_config.get('min_num_clusters', 1),
        "max_num_clusters": warehouse_config.get('max_num_clusters', 1),
        "auto_stop_mins": warehouse_config.get('auto_stop_mins', 120),
        "tags": warehouse_config.get('tags', {}),
        "spot_instance_policy": warehouse_config.get('spot_instance_policy', 'COST_OPTIMIZED'),
        "enable_photon": warehouse_config.get('enable_photon', True),
        "enable_serverless_compute": warehouse_config.get('enable_serverless_compute', False),
        "warehouse_type": warehouse_config.get('warehouse_type', 'PRO'),
        "channel": warehouse_config.get('channel', {})
    }
    
    try:
        response = make_api_request("POST", url, headers, data)
        logger.info(f"Created SQL warehouse: {data['name']}")
        return response.json()
    except Exception as e:
        logger.error(f"Failed to create SQL warehouse {data['name']}: {e}")
        return None

def migrate_sql_warehouses():
    """Main migration function for SQL warehouses"""
    config = load_config()
    source = config['source']
    target = config['target']
    
    logger.info("Starting SQL warehouse migration...")
    
    # Get SQL warehouses from source
    logger.info("Fetching SQL warehouses from source workspace...")
    warehouses = list_sql_warehouses(source['host'], source['token'])
    logger.info(f"Found {len(warehouses)} SQL warehouses")
    
    # Get detailed config for each warehouse
    warehouse_configs = []
    for warehouse in warehouses:
        warehouse_id = warehouse['id']
        config_detail = get_sql_warehouse(source['host'], source['token'], warehouse_id)
        if config_detail:
            warehouse_configs.append(config_detail)
    
    # Save backup
    save_backup(warehouse_configs, "sql_warehouses")
    
    success_count = 0
    failed_count = 0
    
    # Create warehouses in target
    for warehouse_config in warehouse_configs:
        logger.info(f"Creating SQL warehouse: {warehouse_config['name']}")
        
        if create_sql_warehouse(target['host'], target['token'], warehouse_config):
            success_count += 1
        else:
            failed_count += 1
    
    log_migration_result("SQL Warehouses", success_count, failed_count)

if __name__ == "__main__":
    migrate_sql_warehouses()
