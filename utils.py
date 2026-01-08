"""
Utility functions for Databricks workspace migration
"""
import json
import logging
import requests
from typing import Dict, Any
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """Load configuration from JSON file"""
    with open(config_path, 'r') as f:
        return json.load(f)

def get_headers(token: str) -> Dict[str, str]:
    """Generate headers for API requests"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def make_api_request(
    method: str,
    url: str,
    headers: Dict[str, str],
    data: Dict[str, Any] = None
) -> requests.Response:
    """Make API request with error handling"""
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        if hasattr(e.response, 'text'):
            logging.error(f"Response: {e.response.text}")
        raise

def save_backup(data: Any, object_type: str):
    """Save backup of objects before migration"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{object_type}_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    logging.info(f"Backup saved to {filename}")

def log_migration_result(object_type: str, success: int, failed: int):
    """Log migration results"""
    logging.info(f"Migration completed for {object_type}")
    logging.info(f"  Success: {success}")
    logging.info(f"  Failed: {failed}")
