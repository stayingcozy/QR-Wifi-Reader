import os
import subprocess
import platform

def wifi_check(callback):
    # Check wifi status
    command = "iwconfig wlan0 | grep 'ESSID'"

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
        go_path = "/home/neuralfetch/goPetCamera"

        if result == 1:

            print("WiFi is connected. Proceeding with goPetCamera")

            # WiFi is connected, run the Go program (main)
            main_path = os.path.join(go_path, 'main')

            # Change the current working directory to where the 'main' executable is located
            os.chdir(os.path.dirname(go_path))

            subprocess.run([main_path], text=True)

        else:

            print("WiFi is not connected.")

    wifi_check(on_wifi_status_changed)

if __name__ == "__main__":
    main()
