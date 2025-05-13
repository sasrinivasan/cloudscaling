import requests
import logging

BASE_URL = "https://ws3-cloudapi.qa.xcloudiq.com"

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Function to retrieve the topology
def retrieve_topology(auth_token, payload):
    url = f"{BASE_URL}/retrieve-topology"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error retrieving topology: {e}")
        return None

# Function to hide a node or link on a topology
def hide(auth_token, payload):
    url = f"{BASE_URL}/hide"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error hiding node or link: {e}")
        return None

# Function to unhide a node or link on a topology
def unhide(auth_token, payload):
    url = f"{BASE_URL}/unhide"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error unhiding node or link: {e}")
        return None

# Function to get the group hierarchy
def get_group_hierarchy(auth_token):
    url = f"{BASE_URL}/group"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting group hierarchy: {e}")
        return None

# Function to retrieve a list of tags
def get_tags(auth_token, params=None):
    url = f"{BASE_URL}/tags"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting tags: {e}")
        return None

# Function to create a new tag
def create_tag(auth_token, payload):
    url = f"{BASE_URL}/tags"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating tag: {e}")
        return None

# Function to update an existing tag
def update_tag(auth_token, payload):
    url = f"{BASE_URL}/tags"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating tag: {e}")
        return None

# Function to delete a tag
def delete_tag(auth_token, payload):
    url = f"{BASE_URL}/tags"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.delete(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting tag: {e}")
        return None

# Function to associate entities with a tag
def associate_tag_entities(auth_token, payload):
    url = f"{BASE_URL}/tags/entities"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error associating tag entities: {e}")
        return None

# Function to disassociate entities from a tag
def disassociate_tag_entities(auth_token, payload):
    url = f"{BASE_URL}/tags/entities"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.delete(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error disassociating tag entities: {e}")
        return None

# Function to get user preferences
def get_user_preferences(auth_token, params=None):
    url = f"{BASE_URL}/user/preferences"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting user preferences: {e}")
        return None

# Function to create user preferences
def create_user_preferences(auth_token, payload):
    url = f"{BASE_URL}/user/preferences"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating user preferences: {e}")
        return None

# Function to delete user preferences
def delete_user_preferences(auth_token, params=None):
    url = f"{BASE_URL}/user/preferences"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Accept': 'application/json'
    }
    try:
        response = requests.delete(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting user preferences: {e}")
        return None

# Function to update custom positions
def update_custom_position(auth_token, payload):
    url = f"{BASE_URL}/custom-positions"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating custom positions: {e}")
        return None

# Function to delete custom positions
def delete_custom_position(auth_token, params=None):
    url = f"{BASE_URL}/custom-positions"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Accept': 'application/json'
    }
    try:
        response = requests.delete(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting custom positions: {e}")
        return None

# Function to get device physical link details
def get_device_physical_link_details(auth_token, params=None):
    url = f"{BASE_URL}/device/physical/link"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting device physical link details: {e}")
        return None

# Function to get device fabric link details
def get_device_fabric_link_details(auth_token, params=None):
    url = f"{BASE_URL}/device/fabric/link"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting device fabric link details: {e}")
        return None

# Function to get device physical details
def get_device_physical_details(auth_token, params=None):
    url = f"{BASE_URL}/device/physical"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting device physical details: {e}")
        return None

# Function to get device fabric details
def get_device_fabric_details(auth_token, params=None):
    url = f"{BASE_URL}/device/fabric"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting device fabric details: {e}")
        return None

# Function to sync devices
def sync_devices(auth_token, payload):
    url = f"{BASE_URL}/device/sync"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error syncing devices: {e}")
        return None

# Function to retrieve services
def retrieve_services(auth_token, payload):
    url = f"{BASE_URL}/retrieve-services"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error retrieving services: {e}")
        return None

# Function to retrieve VLANs
def retrieve_vlans(auth_token, payload):
    url = f"{BASE_URL}/services/retrieve-vlans"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error retrieving VLANs: {e}")
        return None

# Function to retrieve VRFs
def retrieve_vrfs(auth_token, payload):
    url = f"{BASE_URL}/services/retrieve-vrfs"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error retrieving VRFs: {e}")
        return None

# Function to get schemas
def get_schemas(auth_token, params=None):
    url = f"{BASE_URL}/schemas"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting schemas: {e}")
        return None

# Function to get suggestions
def get_suggestions(auth_token, params=None):
    url = f"{BASE_URL}/suggestions"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting suggestions: {e}")
        return None

# Function to refresh group
def refresh_group(auth_token, payload):
    url = f"{BASE_URL}/group/refresh"
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error refreshing group: {e}")
        return None