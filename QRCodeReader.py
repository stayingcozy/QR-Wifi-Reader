import cv2
import time

# Local imports
from wifiConfig import write_wifi_credentials
from wifiStatus import wifi_check

# Initialize the camera
cap = cv2.VideoCapture(0)

# Default wifi credentials
wifiCredentials = {
  "ssid": '',
  "psk": '',
  "key_mgmt": 'WPA-PSK',
}

while True:

    if wifi_check():
        # Connected to wifi break loop
        break

    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale for QR code detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use OpenCV's QRCodeDetector to detect QR codes
    detector = cv2.QRCodeDetector()
    retval, decoded_info, _ = detector.detectAndDecodeMulti(gray)

    if retval:
        for info in decoded_info:
            print("Detected QR Code:", info)

            # Process raw input
            split_info = info.split(" ; ")

            if len(split_info) == 2:
                wifiCredentials["ssid"] = split_info[0]
                wifiCredentials["psk"] = split_info[1]

                write_wifi_credentials(wifiCredentials)

                time.sleep(10) # wait 10 seconds to allow comp to connect

    # cv2.imshow("QR Code Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
