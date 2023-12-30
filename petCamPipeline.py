import os
import subprocess

from wifiStatus import check_internet_interface
from QRCodeReader import QRCodeReader_main

def get_home_directory():
    home_directory = os.path.expanduser("~")

    return home_directory



def wifi_check(callback):
    # Check wifi status
    interface = check_internet_interface()
    command = "iwconfig %s | grep 'ESSID'" % interface

    try:
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        output = result.stdout
        is_connected = "ESSID:off/any" not in output

        if is_connected:
            # WiFi is connected
            callback(1)  # Pass 1 to the callback
        else:
            # WiFi is not connected
            callback(0)  # Pass 0 to the callback

    except subprocess.CalledProcessError as e:
        print(f"Error while executing command: {e}")
        callback(0)  # Pass 0 to the callback


def main():
    def on_wifi_status_changed(result):

        # get home dir, add firepub path
        home_dir = get_home_directory()
        go_path = os.path.join(home_dir, "firepub")

        if result == 1:

            print("WiFi is connected. Proceeding with firepub")

            # WiFi is connected, run the Go program (main -> firepub)
            main_path = os.path.join(go_path, 'firepub')

            # Change the current working directory to where the 'main' executable is located
            os.chdir(os.path.dirname(go_path))

            subprocess.run([main_path], text=True)

        else:

            print("WiFi is not connected. Running QR detection")

            # run QR detection code
            QRCodeReader_main()

    wifi_check(on_wifi_status_changed)

if __name__ == "__main__":
    while True:
        main()
