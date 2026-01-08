#!/usr/bin/env python3
"""
Migrate Jobs/Workflows from source to target Databricks workspace
"""
import logging
from utils import load_config, get_headers, make_api_request, save_backup, log_migration_result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_jobs(host: str, token: str):
    """List all jobs"""
    url = f"{host}/api/2.1/jobs/list"
    headers = get_headers(token)
    all_jobs = []
    
    try:
        has_more = True
        offset = 0
        limit = 25
        
        while has_more:
            data = {"limit": limit, "offset": offset}
            response = make_api_request("GET", url, headers)
            result = response.json()
            
            jobs = result.get('jobs', [])
            all_jobs.extend(jobs)
            
            has_more = result.get('has_more', False)
            offset += limit
            
        return all_jobs
    except Exception as e:
        logger.error(f"Failed to list jobs: {e}")
        return []

def get_job(host: str, token: str, job_id: str):
    """Get details of a specific job"""
    url = f"{host}/api/2.1/jobs/get"
    headers = get_headers(token)
    data = {"job_id": job_id}
    try:
        response = make_api_request("GET", url, headers)
        return response.json()
    except Exception as e:
        logger.error(f"Failed to get job {job_id}: {e}")
        return None

def create_job(host: str, token: str, job_config: dict):
    """Create a job"""
    url = f"{host}/api/2.1/jobs/create"
    headers = get_headers(token)
    
    # Extract job settings
    settings = job_config.get('settings', {})
    
    # Remove fields that shouldn't be in create request
    fields_to_remove = ['creator_user_name', 'created_time', 'job_id']
    for field in fields_to_remove:
        settings.pop(field, None)
    
    try:
        response = make_api_request("POST", url, headers, settings)
        logger.info(f"Created job: {settings.get('name', 'Unnamed')}")
        return response.json()
    except Exception as e:
        logger.error(f"Failed to create job {settings.get('name', 'Unnamed')}: {e}")
        return None

def migrate_jobs():
    """Main migration function for jobs"""
    config = load_config()
    source = config['source']
    target = config['target']
    
    logger.info("Starting jobs migration...")
    logger.warning("NOTE: Jobs will need cluster IDs and paths updated manually after migration")
    
    # Get jobs from source
    logger.info("Fetching jobs from source workspace...")
    jobs = list_jobs(source['host'], source['token'])
    logger.info(f"Found {len(jobs)} jobs")
    
    # Get detailed config for each job
    job_configs = []
    for job in jobs:
        job_id = job['job_id']
        config_detail = get_job(source['host'], source['token'], job_id)
        if config_detail:
            job_configs.append(config_detail)
    
    # Save backup
    save_backup(job_configs, "jobs")
    
    success_count = 0
    failed_count = 0
    
    # Create jobs in target
    for job_config in job_configs:
        job_name = job_config.get('settings', {}).get('name', 'Unnamed')
        logger.info(f"Creating job: {job_name}")
        
        if create_job(target['host'], target['token'], job_config):
            success_count += 1
        else:
            failed_count += 1
    
    log_migration_result("Jobs", success_count, failed_count)
    logger.warning("IMPORTANT: Review and update cluster IDs, notebook paths, and file paths in migrated jobs")

if __name__ == "__main__":
    migrate_jobs()
