import os
import sys

def write_wifi_credentials(wifi_network):
    # Create the content for the wpa_supplicant.conf file
    wpa_config_content = f"""ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=US

    network={{
        ssid="{wifi_network['ssid']}"
        psk="{wifi_network['psk']}"
        key_mgmt={wifi_network['key_mgmt']}
    }}
    """

    # Define the file path for wpa_supplicant.conf
    wpa_config_file_path = '/etc/wpa_supplicant/wpa_supplicant.conf'

    # Write the content to the file
    try:
        with open(wpa_config_file_path, 'w') as wpa_config_file:
            wpa_config_file.write(wpa_config_content)
        print('wpa_supplicant.conf file created/updated successfully!')
        restart_wifi_interface()
    except Exception as e:
        print(f'Error writing wpa_supplicant.conf: {e}')

def restart_wifi_interface():
    # Reconfigure wifi
    os.system('wpa_cli -i wlan0 reconfigure')


len_arg = len(sys.argv)

if len_arg == 4:
    
    wifi_network = {
        'ssid': sys.argv[1],
        'psk': sys.argv[2],
        'key_mgmt': sys.argv[3]  # Modify this according to your needs
    }

    write_wifi_credentials(wifi_network)
