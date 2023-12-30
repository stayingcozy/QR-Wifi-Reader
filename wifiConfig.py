import os
import subprocess
import re

def get_wireless_interface():
    # 
    start_interface = "wlx"
    result = subprocess.run(f"ip -o link | grep {start_interface}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

    pattern = re.compile(f"{start_interface}\w*")
    matches = pattern.findall(result.stdout)
    # print(f"get_wireless_interface {matches[0]}")

    return matches[0]

def write_wifi_credentials_lp(wifi_network):
    # write wifi credentials for le potato
    # Create the content for the /etc/netplan/wireless.yaml file
    wpa_config_content = f"""network:
    wifis:
        "{wifi_network['device']}":
            optional: true
            access-points:
                "{wifi_network['ssid']}":
                    password: "{wifi_network['psk']}"
            dhcp4: true
    version: 2"""

    # Define the file path for /etc/netplan/wireless.yaml
    wpa_config_file_path = '/etc/netplan/wireless.yaml'

    # Write the content to the file
    try:
        with open(wpa_config_file_path, 'w') as wpa_config_file:
            wpa_config_file.write(wpa_config_content)
        print('/etc/netplan/wireless.yaml file created/updated successfully!')
        restart_wifi_interface_lp()
    except Exception as e:
        print(f'Error writing /etc/netplan/wireless.yaml: {e}')

def restart_wifi_interface_lp():
    # Reconfigure wifi
    os.system('sudo netplan apply')

# def write_wifi_credentials(wifi_network):
#     # Create the content for the wpa_supplicant.conf file
#     wpa_config_content = f"""ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
#     update_config=1
#     country=US

#     network={{
#         ssid="{wifi_network['ssid']}"
#         psk="{wifi_network['psk']}"
#         key_mgmt={wifi_network['key_mgmt']}
#     }}
#     """

#     # Define the file path for wpa_supplicant.conf
#     wpa_config_file_path = '/etc/wpa_supplicant/wpa_supplicant.conf'

#     # Write the content to the file
#     try:
#         with open(wpa_config_file_path, 'w') as wpa_config_file:
#             wpa_config_file.write(wpa_config_content)
#         print('wpa_supplicant.conf file created/updated successfully!')
#         restart_wifi_interface()
#     except Exception as e:
#         print(f'Error writing wpa_supplicant.conf: {e}')

# def restart_wifi_interface():
#     # Reconfigure wifi
#     os.system('wpa_cli -i wlan0 reconfigure')


# len_arg = len(sys.argv)

# if len_arg == 4:

#     wifi_network = {
#         'ssid': sys.argv[1],
#         'psk': sys.argv[2],
#         'key_mgmt': sys.argv[3]  # Modify this according to your needs
#     }

#     write_wifi_credentials(wifi_network)
