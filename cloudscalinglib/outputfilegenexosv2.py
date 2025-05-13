import json
import argparse
import random
import csv
import os

def generate_mac(base_mac="00:ab:01:00:00:00", file_num=1):
    """
    Generate an emulated device MAC address based on the base_mac and the file number.
    """
    mac_parts = base_mac.split(":")
    mac_ints = [int(part, 16) for part in mac_parts]
    mac_ints[-1] += file_num
    mac_ints[-1] = mac_ints[-1] % 256
    return ":".join(f"{x:02x}" for x in mac_ints)

def generate_random_mac():
    """
    Generate a random MAC address.
    """
    return ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])

def generate_port_section(inputcsvfile, base_serial, base_mac, ap_base_serial, ap_base_mac, num_aps, v0=False):
    """
    Generate port section data for v0/state/ports and v1/state/ports.
    The function processes entries from the input CSV file and generates
    port data for access points (DeviceFamily = "extreme").

    Args:
        inputcsvfile (str): Path to the input CSV file.
        base_serial (str): Base serial number in the format "04101900460420".
        base_mac (str): Base MAC address in the format "XX:XX:XX:XX:XX:XX".
        ap_base_serial (str): Base serial number for APs.
        ap_base_mac (str): Base MAC address for APs.
        num_aps (int): Number of APs to generate.
        v0 (bool): Whether to generate data for v0 (True) or v1 (False).

    Returns:
        list: A list of dictionaries containing port data.
    """
 
    # Read the input CSV file
    with open(inputcsvfile, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)  # Read the header row

        # Ensure the required columns exist
        if "DeviceFamily" not in headers or "SerialNumber" not in headers:
            raise ValueError("CSV file must contain 'DeviceFamily' and 'SerialNumber' columns.")

        # Get the index of relevant columns
        device_family_index = headers.index("DeviceFamily")
        serial_number_index = headers.index("SerialNumber")

        # Filter entries with DeviceFamily = "extreme"
        ap_entries = [
            row for row in csv_reader if row[device_family_index].strip().lower() == "extreme"
        ]

    # Generate MAC addresses for APs using generate_mac_for_ap
    mac_serial_list = generate_mac_for_ap(ap_base_serial=ap_base_serial, ap_base_mac=ap_base_mac, num_aps=num_aps)

    # Initialize port data
    port_data = []

    # Process AP entries and assign MACs to ports
    for i, ap_entry in enumerate(ap_entries[:num_aps]):  # Limit to num_aps entries
        serial_number = ap_entry[serial_number_index]
        mac_entry = next((entry for entry in mac_serial_list if serial_number in entry), None)

        if mac_entry:
            mac_address = mac_entry[serial_number]
        else:
            continue  # Skip if no matching MAC entry is found

        # Generate port data for ports 1:1 to 1:24
        port_entry = {
            "name": f"1:{i + 1}",
            "settings": {
                "macAddress": mac_address,
                "operState": "UP",
                "operSpeed": "1G",
                "operDuplex": "FULL",
                "type": "ETHERNET",
                "lldp": {
                    "chassisId": mac_address,
                    "sysName": f"AP_{serial_number}",
                    "sysDesc": f"Access Point {serial_number}"
                }
            }
        }

        # Add v0-specific or v1-specific fields
        if v0:
            port_entry["settings"]["transceiverType"] = "NONE"
            port_entry["settings"]["transceiverSpeed"] = "NOT_APPLICABLE"
        else:
            port_entry["settings"]["connectorType"] = "RJ45"

        port_data.append(port_entry)

    return port_data

def generate_lldp_section(base_serial, base_mac, file_num, num_aps=24):
    """
    Generate the LLDP section with MAC addresses for chassis and fabric attach.
    Each neighbor corresponds to a port (1:1 to 1:num_aps).

    Args:
        base_serial (str): Base serial number for APs.
        base_mac (str): Base MAC address for generating MACs.
        file_num (int): The file number to determine the range of APs.
        num_aps (int): Number of APs to include in the LLDP section. Default is 24.

    Returns:
        dict: LLDP section data with neighbors for each port.
    """
    lldp_data = {"neighbors": []}

    # Calculate the starting index for the current file
    start_index = (file_num - 1) * num_aps
    end_index = start_index + num_aps

    # Generate MAC addresses for APs
    mac_serial_list = generate_mac_for_ap(base_serial, base_mac, end_index)

    # Generate LLDP neighbors for ports 1:1 to 1:num_aps
    for i in range(start_index, end_index):
        serial_number = list(mac_serial_list[i].keys())[0]
        chassis_mac = mac_serial_list[i][serial_number]
        sys_name = f"AP_{serial_number}"

        neighbor = {
            "chassisId": chassis_mac,
            "chassisIdSubtype": "MAC_ADDRESS",
            "dot3": {
                "linkAggPortId": 0,
                "linkAggStatus": "AGG_CAPABLE",
                "maxFrameSize": 1500,
                "power": {
                    "class": "CLASS4",
                    "mdiEnabled": False,
                    "mdiSupported": False,
                    "pairControlable": False,
                    "pairs": "SIGNAL",
                    "portClass": "CLASS_PD"
                }
            },
            "fabricAttach": {
                "authEnabled": False,
                "connectionType": "SINGLE_PORT",
                "lagId": 0,
                "linkInfo": "00-00-00-00",
                "macAddr": chassis_mac,
                "mgmtVlanId": 1,
                "portName": f"1:{i - start_index + 1}",
                "smltId": 0,
                "state": 32,
                "type": "CLIENT_WAP1"
            },
            "index": i - start_index + 1,
            "managementAddressList": [
                {
                    "address": "10.127.16.126",
                    "addressIfId": 19,
                    "addressIfSubtype": "IFINDEX",
                    "addressSubtype": "IPV4"
                }
            ],
            "med": {
                "capCurrent": ["CAPABILITIES", "EXTENDED_PD"],
                "capSupported": ["CAPABILITIES", "EXTENDED_PD"],
                "deviceClass": "ENDPOINT_CLASS_1",
                "poe": {
                    "deviceType": "PD_DEVICE",
                    "pd": {
                        "powerPriority": "CRITICAL",
                        "powerReq": 255,
                        "powerSource": "PSE"
                    }
                }
            },
            "orgDefInfoList": [
                {
                    "index": 1,
                    "oui": "00:04:0d",
                    "subtype": 11,
                    "value": "bd:dd:63:1e:33:11:b7:22:51:a6:54:1e:61:83:ff:02:94:0e:32:ed:0e:54:6b:44:c2:6d:7b:e7:e0:51:91:be:1a:00:01:00:00:0a:1a:3a:a7:40:00:00:00:00"
                },
                {
                    "index": 1,
                    "oui": "00:12:bb",
                    "subtype": 1,
                    "value": "00:11:01"
                }
            ],
            "portDesc": "",
            "portId": f"1:{i - start_index + 1}",
            "portIdSubtype": "INTERFACE_NAME",
            "portName": f"1:{i - start_index + 1}",
            "sysCapEnabled": ["BRIDGE", "WLAN_AP"],
            "sysCapSupported": ["BRIDGE", "WLAN_AP"],
            "sysDesc": "",
            "sysName": sys_name,
            "timeMark": 0,
            "unknownTlvList": []
        }

        lldp_data["neighbors"].append(neighbor)

    return lldp_data

def generate_file_content(prefix, file_num, base_mac, inputcsvfile, base_serial, ap_base_serial, ap_base_mac, num_aps):
    file_name = f"{prefix}-{file_num:06}.txt"
    name_value = f"IQEMU-{prefix}-{file_num:06}"

    # SNMP v0 and v1 config
    snmpv1_section = f"""
curl -k -H Host: openapi.00496CE5F82 http://10.139.44.110:20161/rest/openapi/v1/configuration/snmp
{{
    "contact": "https://www.extremenetworks.com/support/",
    "location": "",
    "name": "{name_value}",
    "v1v2": {{
        "enable": false
    }},
    "v3": {{
        "enable": false
    }}
}}
"""

    snmpv0_section = f"""
curl -k -H Host: openapi.00496CE5F82 http://10.139.44.110:20161/rest/openapi/v0/configuration/snmp
{{
    "contact": "https://www.extremenetworks.com/support/",
    "location": "",
    "name": "{name_value}",
    "v1v2": {{
        "enable": false
    }},
    "v3": {{
        "enable": false
    }}
}}
"""

    # /v1/state/port
    port_data_v1 = generate_port_section(inputcsvfile, base_serial, base_mac, ap_base_serial, ap_base_mac, num_aps, v0=False)
    port_section_v1 = 'curl -k -H Host: openapi.00496CE5F82 http://10.139.44.110:20161/rest/openapi/v1/state/ports\n'
    port_section_v1 += json.dumps(port_data_v1, indent=4) + "\n"

    # /v0/state/port
    port_data_v0 = generate_port_section(inputcsvfile, base_serial, base_mac, ap_base_serial, ap_base_mac, num_aps, v0=True)
    port_section_v0 = 'curl -k -H Host: openapi.00496CE5F82 http://10.139.44.110:20161/rest/openapi/v0/state/ports\n'
    port_section_v0 += json.dumps(port_data_v0, indent=4) + "\n"

    # LLDP section
    lldp_section = f"""
curl -k -H Host: openapi.00496CE5F82 http://10.139.44.110:20161/rest/openapi/v0/state/lldp
{json.dumps(generate_lldp_section(base_serial, base_mac, file_num, num_aps), indent=4)}
"""

    # Combine everything with the requested newlines
    full_content = snmpv0_section + snmpv1_section + "\n" + port_section_v1 + "\n" + port_section_v0 + lldp_section

    # Remove any extra newlines at the end of the file and ensure a single newline at the end
    full_content = full_content.strip() + "\n" + "\n" 

    return file_name, full_content

def write_output_files(prefix, num_files, base_mac, output_dir, inputcsvfile, base_serial, ap_base_serial, ap_base_mac, num_aps):
    """
    Generate output files for switches.

    Args:
        prefix (str): Prefix for the output file names.
        num_files (int): Number of files to generate.
        base_mac (str): Base MAC address for switches.
        output_dir (str): Directory to save the output files.
        inputcsvfile (str): Path to the input CSV file.
        base_serial (str): Base serial number for switches.
        ap_base_serial (str): Base serial number for APs.
        ap_base_mac (str): Base MAC address for APs.
        num_aps (int): Number of APs per switch.

    Returns:
        None
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    cmd_lines = []
    for i in range(1, num_files + 1):
        # Generate the file content
        file_name, content = generate_file_content(
            prefix, i, base_mac, inputcsvfile, base_serial, ap_base_serial, ap_base_mac, num_aps
        )
        file_path = f"{output_dir}/{file_name}"
        with open(file_path, "w") as output_file:
            output_file.write(content)
        cmd_lines.append(f"nos upload response {prefix}-{i:06} {file_name}")

    # Write the a.cmd file
    cmd_file_path = f"{output_dir}/a.cmd"
    with open(cmd_file_path, "w") as cmd_file:
        cmd_file.write("\n".join(cmd_lines) + "\n")

def generate_mac_for_ap(ap_base_serial, ap_base_mac, num_aps):
    """
    Generate a dictionary list of serial numbers and corresponding MAC addresses.

    Args:
        base_serial (str): Base serial number in the format "04101900460420".
        base_mac (str): Base MAC address in the format "XX:XX:XX:XX:XX:XX".
        num_aps (int): Number of APs to generate.

    Returns:
        list: A list of dictionaries in the format {SERIAL: MAC_ADDRESS}.
    """
    def increment_mac(mac, increment):
        """Helper function to increment a MAC address by a given value."""
        mac_int = int(mac.replace(":", ""), 16)  # Convert MAC to integer
        mac_int += increment  # Increment the integer
        mac_hex = f"{mac_int:012x}"  # Convert back to hex, ensuring 12 characters
        return ":".join(mac_hex[i:i+2] for i in range(0, 12, 2))  # Format as MAC

    # Initialize the result list
    result = []

    # Convert the base serial number to an integer
    serial_int = int(ap_base_serial)

    # Generate MAC addresses and serial numbers
    current_mac = ap_base_mac
    for i in range(num_aps):
        serial = f"{serial_int + i:014d}"  # Increment the serial number
        mac_address = increment_mac(current_mac, i * 16)  # Increment MAC by 16 for each AP
        result.append({serial: mac_address})

    return result

if __name__ == "__main__":
    filename = "./devicecfg/apscaling.csv"
    generateOnboardCsvWithAP(
        device_type="EXOS",
        num_devices=100,
        model="x435-24s",
        serial_prefix="SA",
        serial_start=1,
        output_file=filename,
        num_aps=1600,
        ap_start_serial="04101900460421",
        ap_model="AP410C"
    )
    ap_base_serial = "04101900460421"
    ap_base_mac = "062978AB2090"
    write_output_files(
        prefix="SA", 
        num_files=100, 
        base_mac="00:ab:00:00:00:00", 
        output_dir="./output", 
        inputcsvfile=filename,
        base_serial="04101900460420",
        ap_base_serial=ap_base_serial,
        ap_base_mac=ap_base_mac,
        num_aps=24
    )

