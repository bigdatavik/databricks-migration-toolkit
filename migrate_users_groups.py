#!/usr/bin/env python3
"""
Migrate AD Groups and Users from source to target Databricks workspace
"""
import logging
from utils import load_config, get_headers, make_api_request, save_backup, log_migration_result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_groups(host: str, token: str):
    """Get all groups from workspace"""
    url = f"{host}/api/2.0/groups/list"
    headers = get_headers(token)
    response = make_api_request("GET", url, headers)
    return response.json().get('group_names', [])

def get_group_members(host: str, token: str, group_name: str):
    """Get members of a specific group"""
    url = f"{host}/api/2.0/groups/list-members"
    headers = get_headers(token)
    data = {"group_name": group_name}
    response = make_api_request("GET", url, headers)
    return response.json()

def create_group(host: str, token: str, group_name: str):
    """Create a group in target workspace"""
    url = f"{host}/api/2.0/groups/create"
    headers = get_headers(token)
    data = {"group_name": group_name}
    try:
        response = make_api_request("POST", url, headers, data)
        logger.info(f"Created group: {group_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to create group {group_name}: {e}")
        return False

def add_user_to_workspace(host: str, token: str, user_name: str):
    """Add user to workspace using SCIM API"""
    url = f"{host}/api/2.0/preview/scim/v2/Users"
    headers = get_headers(token)
    data = {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "userName": user_name,
        "active": True
    }
    try:
        response = make_api_request("POST", url, headers, data)
        logger.info(f"Added user: {user_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to add user {user_name}: {e}")
        return False

def add_member_to_group(host: str, token: str, group_name: str, member_name: str):
    """Add member to group"""
    url = f"{host}/api/2.0/groups/add-member"
    headers = get_headers(token)
    data = {
        "group_name": group_name,
        "user_name": member_name
    }
    try:
        response = make_api_request("POST", url, headers, data)
        logger.info(f"Added {member_name} to group {group_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to add {member_name} to group {group_name}: {e}")
        return False

def migrate_users_and_groups():
    """Main migration function"""
    config = load_config()
    source = config['source']
    target = config['target']
    
    logger.info("Starting users and groups migration...")
    
    # Get groups from source
    logger.info("Fetching groups from source workspace...")
    groups = get_groups(source['host'], source['token'])
    logger.info(f"Found {len(groups)} groups")
    
    # Save backup
    save_backup(groups, "groups")
    
    success_count = 0
    failed_count = 0
    
    # Migrate each group
    for group in groups:
        logger.info(f"Processing group: {group}")
        
        # Create group in target
        if create_group(target['host'], target['token'], group):
            success_count += 1
            
            # Get members from source
            try:
                members_response = get_group_members(source['host'], source['token'], group)
                members = members_response.get('members', [])
                
                # Add members to target
                for member in members:
                    member_name = member.get('user_name')
                    if member_name:
                        # First ensure user exists in target workspace
                        add_user_to_workspace(target['host'], target['token'], member_name)
                        # Then add to group
                        add_member_to_group(target['host'], target['token'], group, member_name)
            except Exception as e:
                logger.error(f"Failed to migrate members for group {group}: {e}")
        else:
            failed_count += 1
    
    log_migration_result("Users and Groups", success_count, failed_count)

if __name__ == "__main__":
    migrate_users_and_groups()
