#!/usr/bin/env python3
"""
Migrate Git Repos integration from source to target Databricks workspace
"""
import logging
from utils import load_config, get_headers, make_api_request, save_backup, log_migration_result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_repos(host: str, token: str):
    """List all Git repos"""
    url = f"{host}/api/2.0/repos"
    headers = get_headers(token)
    try:
        response = make_api_request("GET", url, headers)
        return response.json().get('repos', [])
    except Exception as e:
        logger.error(f"Failed to list repos: {e}")
        return []

def get_repo(host: str, token: str, repo_id: str):
    """Get details of a specific repo"""
    url = f"{host}/api/2.0/repos/{repo_id}"
    headers = get_headers(token)
    try:
        response = make_api_request("GET", url, headers)
        return response.json()
    except Exception as e:
        logger.error(f"Failed to get repo {repo_id}: {e}")
        return None

def create_repo(host: str, token: str, repo_config: dict):
    """Create a Git repo"""
    url = f"{host}/api/2.0/repos"
    headers = get_headers(token)
    
    data = {
        "url": repo_config.get('url'),
        "provider": repo_config.get('provider'),
        "path": repo_config.get('path')
    }
    
    # Add branch if specified
    if 'branch' in repo_config and repo_config['branch']:
        data['branch'] = repo_config['branch']
    
    # Add tag if specified
    if 'tag' in repo_config and repo_config['tag']:
        data['tag'] = repo_config['tag']
    
    try:
        response = make_api_request("POST", url, headers, data)
        logger.info(f"Created Git repo: {data['path']}")
        return response.json()
    except Exception as e:
        logger.error(f"Failed to create Git repo {data['path']}: {e}")
        return None

def migrate_git_repos():
    """Main migration function for Git repos"""
    config = load_config()
    source = config['source']
    target = config['target']
    
    logger.info("Starting Git repos migration...")
    
    # Get repos from source
    logger.info("Fetching Git repos from source workspace...")
    repos = list_repos(source['host'], source['token'])
    logger.info(f"Found {len(repos)} Git repos")
    
    # Get detailed config for each repo
    repo_configs = []
    for repo in repos:
        repo_id = repo['id']
        config_detail = get_repo(source['host'], source['token'], repo_id)
        if config_detail:
            repo_configs.append(config_detail)
    
    # Save backup
    save_backup(repo_configs, "git_repos")
    
    success_count = 0
    failed_count = 0
    
    # Create repos in target
    for repo_config in repo_configs:
        logger.info(f"Creating Git repo: {repo_config['path']}")
        
        if create_repo(target['host'], target['token'], repo_config):
            success_count += 1
        else:
            failed_count += 1
    
    log_migration_result("Git Repos", success_count, failed_count)

if __name__ == "__main__":
    migrate_git_repos()
