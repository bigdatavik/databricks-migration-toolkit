#!/usr/bin/env python3
"""
Migrate Notebooks from source to target Databricks workspace
"""
import logging
import base64
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

def get_all_notebooks(host: str, token: str, path: str = "/", notebooks: list = None):
    """Recursively get all notebooks"""
    if notebooks is None:
        notebooks = []
    
    objects = list_workspace_objects(host, token, path)
    
    for obj in objects:
        if obj['object_type'] == 'NOTEBOOK':
            notebooks.append(obj)
        elif obj['object_type'] == 'DIRECTORY':
            # Recursively get notebooks from subdirectories
            get_all_notebooks(host, token, obj['path'], notebooks)
    
    return notebooks

def export_notebook(host: str, token: str, notebook_path: str, format: str = "SOURCE"):
    """Export a notebook"""
    url = f"{host}/api/2.0/workspace/export"
    headers = get_headers(token)
    data = {
        "path": notebook_path,
        "format": format
    }
    try:
        response = make_api_request("GET", url, headers)
        return response.json()
    except Exception as e:
        logger.error(f"Failed to export notebook {notebook_path}: {e}")
        return None

def import_notebook(host: str, token: str, notebook_path: str, content: str, language: str, format: str = "SOURCE"):
    """Import a notebook"""
    url = f"{host}/api/2.0/workspace/import"
    headers = get_headers(token)
    data = {
        "path": notebook_path,
        "content": content,
        "language": language,
        "format": format,
        "overwrite": False
    }
    try:
        response = make_api_request("POST", url, headers, data)
        logger.info(f"Imported notebook: {notebook_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to import notebook {notebook_path}: {e}")
        return False

def migrate_notebooks():
    """Main migration function for notebooks"""
    config = load_config()
    source = config['source']
    target = config['target']
    
    logger.info("Starting notebook migration...")
    
    # Get all notebooks from source
    logger.info("Fetching notebooks from source workspace...")
    notebooks = get_all_notebooks(source['host'], source['token'])
    logger.info(f"Found {len(notebooks)} notebooks")
    
    # Export all notebooks
    notebook_exports = []
    for notebook in notebooks:
        path = notebook['path']
        language = notebook.get('language', 'PYTHON')
        
        logger.info(f"Exporting notebook: {path}")
        exported = export_notebook(source['host'], source['token'], path)
        
        if exported:
            notebook_exports.append({
                'path': path,
                'language': language,
                'content': exported.get('content')
            })
    
    # Save backup
    save_backup(notebook_exports, "notebooks")
    
    success_count = 0
    failed_count = 0
    
    # Import notebooks to target
    for notebook_export in notebook_exports:
        path = notebook_export['path']
        language = notebook_export['language']
        content = notebook_export['content']
        
        logger.info(f"Importing notebook: {path}")
        
        if import_notebook(target['host'], target['token'], path, content, language):
            success_count += 1
        else:
            failed_count += 1
    
    log_migration_result("Notebooks", success_count, failed_count)

if __name__ == "__main__":
    migrate_notebooks()
