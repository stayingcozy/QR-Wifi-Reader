import subprocess

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


if __name__ == "__main__":
    wifi_check()
