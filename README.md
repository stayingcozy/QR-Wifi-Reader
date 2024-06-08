<p align="center">
    <img src="assets/QR Code Reader Logo.png" width=300 height=300>
</p>

# QR Wifi Reader
Read QR code with WiFi SSID and password information to pass along to the reader on a embedded device with a camera.

## Usage
Install code on your linux embedded device with a camera. Move .service file into the proper systemd directory. Verify the path to the code in service file is the same as your install path. Also verify python is installed on your device. Restart systemd or restart the device for the service to run continously. 

Once the device recognises a QR code it will pull WiFi SSID and password information from it. Once done the device will be connected to the inputted Wifi. You can now have the potential to ssh and update your device without a monitor. 