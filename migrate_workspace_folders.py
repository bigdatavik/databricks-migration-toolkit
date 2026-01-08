#!/usr/bin/env python3
"""
Migrate Workspace Folder structure from source to target Databricks workspace
"""
import logging
from utils import load_config, get_headers, make_api_request, save_backup, log_migration_result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_workspace_objects(host: str, token: str, path: str = "/"):
    """List all objects in a workspace path"""
    url = f"{host}/api/2.0/workspace/list"
    headers = get_headers(token)
    data = {"path": path}
    try:
        response = make_api_request("GET", url, headers)
        return response.json().get('objects', [])
    except Exception as e:
        logger.error(f"Failed to list workspace path {path}: {e}")
        return []

def get_workspace_structure(host: str, token: str, path: str = "/", structure: list = None):
    """Recursively get workspace folder structure"""
    if structure is None:
        structure = []
    
    objects = list_workspace_objects(host, token, path)
    
    for obj in objects:
        if obj['object_type'] == 'DIRECTORY':
            structure.append({
                'path': obj['path'],
                'object_type': 'DIRECTORY'
            })
            # Recursively get subdirectories
            get_workspace_structure(host, token, obj['path'], structure)
    
    return structure

def create_folder(host: str, token: str, path: str):
    """Create a folder in workspace"""
    url = f"{host}/api/2.0/workspace/mkdirs"
    headers = get_headers(token)
    data = {"path": path}
    try:
        response = make_api_request("POST", url, headers, data)
        logger.info(f"Created folder: {path}")
        return True
    except Exception as e:
        logger.error(f"Failed to create folder {path}: {e}")
        return False

def migrate_workspace_folders():
    """Main migration function for workspace folders"""
    config = load_config()
    source = config['source']
    target = config['target']
    
    logger.info("Starting workspace folder migration...")
    
    # Get folder structure from source
    logger.info("Fetching folder structure from source workspace...")
    folders = get_workspace_structure(source['host'], source['token'])
    logger.info(f"Found {len(folders)} folders")
    
    # Save backup
    save_backup(folders, "workspace_folders")
    
    success_count = 0
    failed_count = 0
    
    # Create folders in target
    for folder in folders:
        path = folder['path']
        logger.info(f"Creating folder: {path}")
        
        if create_folder(target['host'], target['token'], path):
            success_count += 1
        else:
            failed_count += 1
    
    log_migration_result("Workspace Folders", success_count, failed_count)

if __name__ == "__main__":
    migrate_workspace_folders()
