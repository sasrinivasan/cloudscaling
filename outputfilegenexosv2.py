import json
import argparse
import random

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

def generate_port_section(base_mac, file_num, v0=False):
    """
    Generate port section data for v0/state/ports and v1/state/ports
    The 'v0' is true transceiver keys are not included
    """
    port_data = [
        {"name": f"1:{i}", "settings": {
            "congPkts": 0,
            "connectorType": "RJ45",
            "ifIndex": 1000 + i,
            "localName": str(i),
            "macAddress": base_mac,
            "operAutoNegotiation": True,
            "operDuplex": "FULL",
            "operSpeed": "1G",
            "operState": "UP",
            "transceiverCableLength": "NOT_APPLICABLE",
            "transceiverSpeed": "NOT_APPLICABLE",
            "transceiverType": "NONE",
            "type": "ETHERNET",
            "utilization": {
                "rx": {
                    "avg": 0.0,
                    "max": 0.0,
                    "min": 0.0
                },
                "tx": {
                    "avg": 0.0,
                    "max": 0.0,
                    "min": 0.0
                }
            }
        }} for i in range(1, 11)  # Generate ports 1 to 10
    ]
    
    # Remove unwanted keys for v0/state/ports only
    if v0:
        for port in port_data:
            # Delete the unwanted keys from v0 ports
            if "transceiverCableLength" in port['settings']:
                del port['settings']["transceiverCableLength"]
            if "transceiverSpeed" in port['settings']:
                del port['settings']["transceiverSpeed"]
            if "transceiverType" in port['settings']:
                del port['settings']["transceiverType"]

    # Update macAddress for each entry
    for i, port in enumerate(port_data):
        port['settings']['macAddress'] = generate_mac(base_mac, file_num)

    return port_data

def generate_lldp_section():
    """
    Generate the LLDP section with random MAC addresses for chassis.
    """
    lldp_data = {
        "neighbors": [
            {
                "chassisId": generate_random_mac(),
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
                    "macAddr": generate_random_mac(),
                    "mgmtVlanId": 1,
                    "portName": "1:3",
                    "smltId": 0,
                    "state": 32,
                    "type": "CLIENT_WAP1"
                },
                "index": 1,
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
                "portId": "mgt0",
                "portIdSubtype": "INTERFACE_NAME",
                "portName": "1:3",
                "sysCapEnabled": ["BRIDGE", "WLAN_AP"],
                "sysCapSupported": ["BRIDGE", "WLAN_AP"],
                "sysDesc": "",
                "sysName": "X435_1_AP1\u0000",
                "timeMark": 0,
                "unknownTlvList": []
            }
        ]
    }

    return lldp_data

def generate_file_content(prefix, file_num, base_mac):
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
    port_data_v1 = generate_port_section(base_mac, file_num, v0=False)
    port_section_v1 = 'curl -k -H Host: openapi.00496CE5F82 http://10.139.44.110:20161/rest/openapi/v1/state/ports\n'
    port_section_v1 += json.dumps(port_data_v1, indent=4) + "\n"

    # /v0/state/port
    port_data_v0 = generate_port_section(base_mac, file_num, v0=True)
    port_section_v0 = 'curl -k -H Host: openapi.00496CE5F82 http://10.139.44.110:20161/rest/openapi/v0/state/ports\n'
    port_section_v0 += json.dumps(port_data_v0, indent=4) + "\n"

    # LLDP section
    lldp_section = f"""
curl -k -H Host: openapi.00496CE5F82 http://10.139.44.110:20161/rest/openapi/v0/state/lldp
{json.dumps(generate_lldp_section(), indent=4)}
"""

    # Combine everything with the requested newlines
    full_content = snmpv0_section + snmpv1_section + "\n" + port_section_v1 + "\n" + port_section_v0 + lldp_section

    # Remove any extra newlines at the end of the file and ensure a single newline at the end
    full_content = full_content.strip() + "\n" + "\n" 

    return file_name, full_content

def write_output_files(prefix, num_files, base_mac, output_dir):
    cmd_lines = []
    for i in range(1, num_files + 1):
        file_name, content = generate_file_content(prefix, i, base_mac)
        file_path = f"{output_dir}/{file_name}"
        with open(file_path, "w") as output_file:
            output_file.write(content)
        cmd_lines.append(f"nos upload response {prefix}-{i:06} {file_name}")

    # Write the a.cmd file
    cmd_file_path = f"{output_dir}/a.cmd"
    with open(cmd_file_path, "w") as cmd_file:
        cmd_file.write("\n".join(cmd_lines) + "\n")

def main():
    #example run: python3 outputfilegenexos.py SKS 10 00:ab:01:00:00:00 /Users/sasrinivasan/Downloads/output
    parser = argparse.ArgumentParser(description="Generate configuration files with dynamic MAC addresses.")
    parser.add_argument("prefix", help="Prefix to use for file names (e.g., SKS).")
    parser.add_argument("num_files", type=int, help="Number of files to generate.")
    parser.add_argument("base_mac", help="Base MAC address (e.g., 00:04:96:CE:5F:82).")
    parser.add_argument("output_dir", help="Directory to save the generated files.")
    
    args = parser.parse_args()

    # Generate files for emulator
    write_output_files(args.prefix, args.num_files, args.base_mac, args.output_dir)

if __name__ == "__main__":
    main()
