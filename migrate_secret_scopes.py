#!/usr/bin/env python3
"""
Migrate Secret Scopes from source to target Databricks workspace
NOTE: Secret values cannot be read from API, only secret names are migrated
"""
import logging
from utils import load_config, get_headers, make_api_request, save_backup, log_migration_result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_secret_scopes(host: str, token: str):
    """List all secret scopes"""
    url = f"{host}/api/2.0/secrets/scopes/list"
    headers = get_headers(token)
    try:
        response = make_api_request("GET", url, headers)
        return response.json().get('scopes', [])
    except Exception as e:
        logger.error(f"Failed to list secret scopes: {e}")
        return []

def list_secrets(host: str, token: str, scope_name: str):
    """List all secrets in a scope"""
    url = f"{host}/api/2.0/secrets/list"
    headers = get_headers(token)
    data = {"scope": scope_name}
    try:
        response = make_api_request("GET", url, headers)
        return response.json().get('secrets', [])
    except Exception as e:
        logger.error(f"Failed to list secrets in scope {scope_name}: {e}")
        return []

def create_secret_scope(host: str, token: str, scope_name: str, backend_type: str = "DATABRICKS"):
    """Create a secret scope"""
    url = f"{host}/api/2.0/secrets/scopes/create"
    headers = get_headers(token)
    data = {
        "scope": scope_name,
        "initial_manage_principal": "users",
        "backend_type": backend_type
    }
    try:
        response = make_api_request("POST", url, headers, data)
        logger.info(f"Created secret scope: {scope_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to create secret scope {scope_name}: {e}")
        return False

def create_secret_placeholder(host: str, token: str, scope_name: str, secret_key: str):
    """Create a placeholder for secret (value needs to be set manually)"""
    url = f"{host}/api/2.0/secrets/put"
    headers = get_headers(token)
    data = {
        "scope": scope_name,
        "key": secret_key,
        "string_value": "PLACEHOLDER_PLEASE_UPDATE"
    }
    try:
        response = make_api_request("POST", url, headers, data)
        logger.warning(f"Created secret placeholder: {scope_name}/{secret_key} - PLEASE UPDATE VALUE")
        return True
    except Exception as e:
        logger.error(f"Failed to create secret {scope_name}/{secret_key}: {e}")
        return False

def migrate_secret_scopes():
    """Main migration function for secret scopes"""
    config = load_config()
    source = config['source']
    target = config['target']
    
    logger.info("Starting secret scope migration...")
    logger.warning("NOTE: Secret values cannot be read via API - placeholders will be created")
    
    # Get secret scopes from source
    logger.info("Fetching secret scopes from source workspace...")
    scopes = list_secret_scopes(source['host'], source['token'])
    logger.info(f"Found {len(scopes)} secret scopes")
    
    # Get secrets for each scope
    scope_details = []
    for scope in scopes:
        scope_name = scope['name']
        secrets = list_secrets(source['host'], source['token'], scope_name)
        scope_details.append({
            'scope': scope,
            'secrets': secrets
        })
    
    # Save backup
    save_backup(scope_details, "secret_scopes")
    
    success_count = 0
    failed_count = 0
    secrets_migrated = 0
    
    # Create scopes and secrets in target
    for detail in scope_details:
        scope_name = detail['scope']['name']
        backend_type = detail['scope'].get('backend_type', 'DATABRICKS')
        
        logger.info(f"Creating secret scope: {scope_name}")
        
        if create_secret_scope(target['host'], target['token'], scope_name, backend_type):
            success_count += 1
            
            # Create placeholder secrets
            for secret in detail['secrets']:
                secret_key = secret['key']
                if create_secret_placeholder(target['host'], target['token'], scope_name, secret_key):
                    secrets_migrated += 1
        else:
            failed_count += 1
    
    log_migration_result("Secret Scopes", success_count, failed_count)
    logger.info(f"Created {secrets_migrated} secret placeholders - PLEASE UPDATE VALUES MANUALLY")

if __name__ == "__main__":
    migrate_secret_scopes()
