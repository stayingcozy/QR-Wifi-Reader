import subprocess
import re

def wifi_check():
    # Check wifi status
    command = 'iwconfig wlan0 | grep "ESSID"'

    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout
        isConnected = not output.strip().endswith('ESSID:off/any')

        if isConnected:
            # WiFi is connected
            return True
        else:
            # WiFi is not connected
            return False
        
    except subprocess.CalledProcessError as e:
        print(f'Error while executing command: {e.stderr}')
        return False
    
def wifi_check_lp():
    # Check wifi status
    interface = check_internet_interface()
    command = "iwconfig %s | grep 'ESSID'" % interface

    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout
        isConnected = not output.strip().endswith('ESSID:off/any')

        if isConnected:
            # WiFi is connected
            return True
        else:
            # WiFi is not connected
            return False
        
    except subprocess.CalledProcessError as e:
        print(f'Error while executing command: {e.stderr}')
        return False

def check_internet_interface(interface_pattern="wlx"):
    try:
        # Run iwconfig and capture the output
        result = subprocess.run(["iwconfig"], text=True, capture_output=True)

        # Use regular expression to find matching interfaces
        pattern = re.compile(f"{interface_pattern}\w*")
        matches = pattern.findall(result.stdout)
        # print(f"check_internet_interface {matches[0]}")

        if matches:
            return matches[0]

        else:
            print(f"No matching interface found for pattern: {interface_pattern}")
            return ""

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    wifi_check()
