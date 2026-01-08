#!/usr/bin/env python3
"""
Export Databricks workspace resources to Terraform configurations

This script connects to a source Databricks workspace and generates
Terraform .tf files that can be used to recreate the resources in
a target workspace.
"""

import json
import argparse
import os
from pathlib import Path
import sys

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils import load_config, get_headers, make_api_request

def export_users_groups(host: str, token: str, output_dir: str):
    """Export users and groups to Terraform format"""
    print("Exporting users and groups...")
    
    # Get groups
    url = f"{host}/api/2.0/groups/list"
    headers = get_headers(token)
    response = make_api_request("GET", url, headers)
    groups = response.json().get('group_names', [])
    
    # Generate Terraform config
    tf_config = {
        "groups": {},
        "users": {},
        "group_members": {}
    }
    
    for i, group in enumerate(groups):
        key = f"group_{i}"
        tf_config["groups"][key] = {
            "display_name": group
        }
    
    # Write to file
    output_file = os.path.join(output_dir, "users_groups.auto.tfvars.json")
    with open(output_file, 'w') as f:
        json.dump(tf_config, f, indent=2)
    
    print(f"  ✓ Exported {len(groups)} groups to {output_file}")

def export_clusters(host: str, token: str, output_dir: str):
    """Export clusters to Terraform format"""
    print("Exporting clusters...")
    
    url = f"{host}/api/2.0/clusters/list"
    headers = get_headers(token)
    response = make_api_request("GET", url, headers)
    clusters = response.json().get('clusters', [])
    
    # Filter all-purpose clusters
    all_purpose = [c for c in clusters if c.get('cluster_source') != 'JOB']
    
    tf_config = {"clusters": {}}
    
    for i, cluster in enumerate(all_purpose):
        key = f"cluster_{i}"
        tf_config["clusters"][key] = {
            "cluster_name": cluster.get('cluster_name'),
            "spark_version": cluster.get('spark_version'),
            "node_type_id": cluster.get('node_type_id'),
            "num_workers": cluster.get('num_workers', 1),
            "autotermination_minutes": cluster.get('autotermination_minutes', 120)
        }
        
        if 'spark_conf' in cluster:
            tf_config["clusters"][key]["spark_conf"] = cluster['spark_conf']
    
    output_file = os.path.join(output_dir, "clusters.auto.tfvars.json")
    with open(output_file, 'w') as f:
        json.dump(tf_config, f, indent=2)
    
    print(f"  ✓ Exported {len(all_purpose)} clusters to {output_file}")

def export_notebooks(host: str, token: str, output_dir: str):
    """Export notebooks to Terraform format"""
    print("Exporting notebooks...")
    print("  Note: Notebook content should be stored in files and referenced")
    print("  Consider using databricks_notebook resource with 'source' attribute")

def export_jobs(host: str, token: str, output_dir: str):
    """Export jobs to Terraform format"""
    print("Exporting jobs...")
    
    url = f"{host}/api/2.1/jobs/list"
    headers = get_headers(token)
    response = make_api_request("GET", url, headers)
    jobs = response.json().get('jobs', [])
    
    tf_config = {"jobs": {}}
    
    for i, job in enumerate(jobs):
        key = f"job_{i}"
        tf_config["jobs"][key] = {
            "name": job.get('settings', {}).get('name', f'Job {i}'),
            "max_concurrent_runs": job.get('settings', {}).get('max_concurrent_runs', 1)
        }
        
        # Add basic task info (would need more detailed conversion)
        if 'tasks' in job.get('settings', {}):
            print(f"    ⚠ Job '{tf_config['jobs'][key]['name']}' has multi-task workflow - manual review needed")
    
    output_file = os.path.join(output_dir, "jobs.auto.tfvars.json")
    with open(output_file, 'w') as f:
        json.dump(tf_config, f, indent=2)
    
    print(f"  ✓ Exported {len(jobs)} jobs to {output_file}")
    print(f"    ⚠ Jobs require manual review for task configurations and cluster references")

def export_secret_scopes(host: str, token: str, output_dir: str):
    """Export secret scopes to Terraform format"""
    print("Exporting secret scopes...")
    
    url = f"{host}/api/2.0/secrets/scopes/list"
    headers = get_headers(token)
    response = make_api_request("GET", url, headers)
    scopes = response.json().get('scopes', [])
    
    tf_config = {"secret_scopes": {}}
    
    for i, scope in enumerate(scopes):
        key = f"scope_{i}"
        tf_config["secret_scopes"][key] = {
            "name": scope.get('name')
        }
    
    output_file = os.path.join(output_dir, "secrets.auto.tfvars.json")
    with open(output_file, 'w') as f:
        json.dump(tf_config, f, indent=2)
    
    print(f"  ✓ Exported {len(scopes)} secret scopes to {output_file}")
    print(f"    ⚠ Secret values cannot be exported - must be set manually")

def export_sql_warehouses(host: str, token: str, output_dir: str):
    """Export SQL warehouses to Terraform format"""
    print("Exporting SQL warehouses...")
    
    url = f"{host}/api/2.0/sql/warehouses"
    headers = get_headers(token)
    response = make_api_request("GET", url, headers)
    warehouses = response.json().get('warehouses', [])
    
    tf_config = {"sql_warehouses": {}}
    
    for i, wh in enumerate(warehouses):
        key = f"warehouse_{i}"
        tf_config["sql_warehouses"][key] = {
            "name": wh.get('name'),
            "cluster_size": wh.get('cluster_size'),
            "max_num_clusters": wh.get('max_num_clusters', 1),
            "enable_photon": wh.get('enable_photon', True)
        }
    
    output_file = os.path.join(output_dir, "sql_warehouses.auto.tfvars.json")
    with open(output_file, 'w') as f:
        json.dump(tf_config, f, indent=2)
    
    print(f"  ✓ Exported {len(warehouses)} SQL warehouses to {output_file}")

def export_repos(host: str, token: str, output_dir: str):
    """Export Git repos to Terraform format"""
    print("Exporting Git repos...")
    
    url = f"{host}/api/2.0/repos"
    headers = get_headers(token)
    response = make_api_request("GET", url, headers)
    repos = response.json().get('repos', [])
    
    tf_config = {"repos": {}}
    
    for i, repo in enumerate(repos):
        key = f"repo_{i}"
        tf_config["repos"][key] = {
            "url": repo.get('url'),
            "git_provider": repo.get('provider'),
            "path": repo.get('path')
        }
        
        if 'branch' in repo:
            tf_config["repos"][key]["branch"] = repo['branch']
    
    output_file = os.path.join(output_dir, "repos.auto.tfvars.json")
    with open(output_file, 'w') as f:
        json.dump(tf_config, f, indent=2)
    
    print(f"  ✓ Exported {len(repos)} Git repos to {output_file}")
    print(f"    ⚠ Git credentials will need to be re-authenticated")

def main():
    parser = argparse.ArgumentParser(description='Export Databricks workspace to Terraform')
    parser.add_argument('--config', default='../config.json', help='Path to config file')
    parser.add_argument('--workspace', choices=['source', 'target'], default='source',
                       help='Which workspace to export from')
    parser.add_argument('--output', default='./environments/source',
                       help='Output directory for Terraform files')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    workspace_config = config[args.workspace]
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    print("="*80)
    print(f"Exporting from {args.workspace} workspace to Terraform configs")
    print("="*80)
    print(f"Workspace: {workspace_config['host']}")
    print(f"Output: {args.output}")
    print("")
    
    # Export each resource type
    try:
        export_users_groups(workspace_config['host'], workspace_config['token'], args.output)
        export_clusters(workspace_config['host'], workspace_config['token'], args.output)
        export_secret_scopes(workspace_config['host'], workspace_config['token'], args.output)
        export_sql_warehouses(workspace_config['host'], workspace_config['token'], args.output)
        export_repos(workspace_config['host'], workspace_config['token'], args.output)
        export_jobs(workspace_config['host'], workspace_config['token'], args.output)
        export_notebooks(workspace_config['host'], workspace_config['token'], args.output)
    except Exception as e:
        print(f"\n❌ Error during export: {e}")
        return 1
    
    print("\n" + "="*80)
    print("Export Complete!")
    print("="*80)
    print(f"\nGenerated files in: {args.output}")
    print("\nNext steps:")
    print("1. Review generated .auto.tfvars.json files")
    print("2. Create main.tf to use the modules")
    print("3. Run 'terraform init'")
    print("4. Run 'terraform plan' to preview")
    print("5. Run 'terraform apply' to create resources")
    print("\n⚠  Important: Review and update:")
    print("  - Secret values (cannot be exported)")
    print("  - Git credentials (need re-authentication)")
    print("  - Job cluster references (IDs will change)")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
