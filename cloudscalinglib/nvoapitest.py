import pytest
import nvorestlib

# Mock data for testing
auth_token = "your_auth_token"

# Default payloads and params based on nvoapi.yaml
default_payloads = {
    "retrieve_topology": {
        "deviceId": ["example_device_id"],
        "type": ["VLAN_Service", "L2VSN_Service", "L3VSN_Service"],
        "detail": True
    },
    "hide": {
        "nodeId": "example_node_id",
        "linkId": "example_link_id"
    },
    "unhide": {
        "nodeId": "example_node_id",
        "linkId": "example_link_id"
    },
    "create_tag": {
        "name": "example_tag_name",
        "description": "example_description"
    },
    "update_tag": {
        "id": "example_tag_id",
        "name": "updated_tag_name",
        "description": "updated_description"
    },
    "delete_tag": {
        "id": "example_tag_id"
    },
    "associate_tag_entities": {
        "tagId": "example_tag_id",
        "entityIds": ["example_entity_id"]
    },
    "disassociate_tag_entities": {
        "tagId": "example_tag_id",
        "entityIds": ["example_entity_id"]
    },
    "create_user_preferences": {
        "preferenceKey": "example_key",
        "preferenceValue": "example_value"
    },
    "update_custom_position": {
        "positionId": "example_position_id",
        "coordinates": {"x": 0, "y": 0}
    },
    "sync_devices": {
        "deviceIds": ["example_device_id"]
    },
    "retrieve_services": {
        "deviceId": ["example_device_id"],
        "type": ["VLAN_Service", "L2VSN_Service", "L3VSN_Service"],
        "detail": True
    },
    "retrieve_vlans": {
        "deviceId": ["example_device_id"],
        "type": ["VLAN_Service"],
        "detail": True
    },
    "retrieve_vrfs": {
        "deviceId": ["example_device_id"],
        "type": ["VRF_Service"],
        "detail": True
    },
    "refresh_group": {
        "groupId": "example_group_id"
    }
}

default_params = {
    "get_tags": {
        "filter": "example_filter"
    },
    "get_user_preferences": {
        "userId": "example_user_id"
    },
    "delete_user_preferences": {
        "preferenceKey": "example_key"
    },
    "delete_custom_position": {
        "positionId": "example_position_id"
    },
    "get_device_physical_link_details": {
        "deviceId": "example_device_id"
    },
    "get_device_fabric_link_details": {
        "deviceId": "example_device_id"
    },
    "get_device_physical_details": {
        "deviceId": "example_device_id"
    },
    "get_device_fabric_details": {
        "deviceId": "example_device_id"
    },
    "get_schemas": {
        "schemaType": "example_schema_type"
    },
    "get_suggestions": {
        "query": "example_query"
    }
}

def test_retrieve_topology():
    response = nvorestlib.retrieve_topology(auth_token, default_payloads["retrieve_topology"])
    assert response is not None
    assert "topology" in response

def test_hide():
    response = nvorestlib.hide(auth_token, default_payloads["hide"])
    assert response is not None
    assert "status" in response

def test_unhide():
    response = nvorestlib.unhide(auth_token, default_payloads["unhide"])
    assert response is not None
    assert "status" in response

def test_get_group_hierarchy():
    response = nvorestlib.get_group_hierarchy(auth_token)
    assert response is not None
    assert "groups" in response

def test_get_tags():
    response = nvorestlib.get_tags(auth_token, default_params["get_tags"])
    assert response is not None
    assert "tags" in response

def test_create_tag():
    response = nvorestlib.create_tag(auth_token, default_payloads["create_tag"])
    assert response is not None
    assert "tag" in response

def test_update_tag():
    response = nvorestlib.update_tag(auth_token, default_payloads["update_tag"])
    assert response is not None
    assert "tag" in response

def test_delete_tag():
    response = nvorestlib.delete_tag(auth_token, default_payloads["delete_tag"])
    assert response is not None
    assert "status" in response

def test_associate_tag_entities():
    response = nvorestlib.associate_tag_entities(auth_token, default_payloads["associate_tag_entities"])
    assert response is not None
    assert "status" in response

def test_disassociate_tag_entities():
    response = nvorestlib.disassociate_tag_entities(auth_token, default_payloads["disassociate_tag_entities"])
    assert response is not None
    assert "status" in response

def test_get_user_preferences():
    response = nvorestlib.get_user_preferences(auth_token, default_params["get_user_preferences"])
    assert response is not None
    assert "preferences" in response

def test_create_user_preferences():
    response = nvorestlib.create_user_preferences(auth_token, default_payloads["create_user_preferences"])
    assert response is not None
    assert "preference" in response

def test_delete_user_preferences():
    response = nvorestlib.delete_user_preferences(auth_token, default_params["delete_user_preferences"])
    assert response is not None
    assert "status" in response

def test_update_custom_position():
    response = nvorestlib.update_custom_position(auth_token, default_payloads["update_custom_position"])
    assert response is not None
    assert "status" in response

def test_delete_custom_position():
    response = nvorestlib.delete_custom_position(auth_token, default_params["delete_custom_position"])
    assert response is not None
    assert "status" in response

def test_get_device_physical_link_details():
    response = nvorestlib.get_device_physical_link_details(auth_token, default_params["get_device_physical_link_details"])
    assert response is not None
    assert "links" in response

def test_get_device_fabric_link_details():
    response = nvorestlib.get_device_fabric_link_details(auth_token, default_params["get_device_fabric_link_details"])
    assert response is not None
    assert "links" in response

def test_get_device_physical_details():
    response = nvorestlib.get_device_physical_details(auth_token, default_params["get_device_physical_details"])
    assert response is not None
    assert "devices" in response

def test_get_device_fabric_details():
    response = nvorestlib.get_device_fabric_details(auth_token, default_params["get_device_fabric_details"])
    assert response is not None
    assert "devices" in response

def test_sync_devices():
    response = nvorestlib.sync_devices(auth_token, default_payloads["sync_devices"])
    assert response is not None
    assert "status" in response

def test_retrieve_services():
    response = nvorestlib.retrieve_services(auth_token, default_payloads["retrieve_services"])
    assert response is not None
    assert "services" in response

def test_retrieve_vlans():
    response = nvorestlib.retrieve_vlans(auth_token, default_payloads["retrieve_vlans"])
    assert response is not None
    assert "vlans" in response

def test_retrieve_vrfs():
    response = nvorestlib.retrieve_vrfs(auth_token, default_payloads["retrieve_vrfs"])
    assert response is not None
    assert "vrfs" in response

def test_get_schemas():
    response = nvorestlib.get_schemas(auth_token, default_params["get_schemas"])
    assert response is not None
    assert "schemas" in response

def test_get_suggestions():
    response = nvorestlib.get_suggestions(auth_token, default_params["get_suggestions"])
    assert response is not None
    assert "suggestions" in response

def test_refresh_group():
    response = nvorestlib.refresh_group(auth_token, default_payloads["refresh_group"])
    assert response is not None
    assert "status" in response