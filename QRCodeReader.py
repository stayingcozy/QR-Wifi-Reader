import cv2
import time

# Local imports
from wifiConfig import write_wifi_credentials
from wifiStatus import wifi_check
from codePipeline import main

def wait_for_wifi_connect(qrDetected, timeToWait):
    
    # If qr code is detected wait for comp to connect to wifi
    start = time.time()
    while qrDetected:
        tdelta = time.time() - start
        if tdelta < timeToWait:
            if wifi_check():
                break
        else:
            return False
        
    return False

def process_raw_qr(retval, decoded_info, wifiCredentials):

    for info in decoded_info:

        # Process raw input
        str_retval = str(retval)
        split_info = str_retval.split(" ; ")

        if len(split_info) == 2:
            print("Detected QR Code")
            wifiCredentials["ssid"] = split_info[0]
            wifiCredentials["psk"] = split_info[1]

            write_wifi_credentials(wifiCredentials)

            # qrDetected = True
            return True

    return False

def QRCodeReader_main():
    # Initialize the camera
    cap = cv2.VideoCapture(1)

    # Default wifi credentials
    wifiCredentials = {
    "ssid": '',
    "psk": '',
    "key_mgmt": 'WPA-PSK',
    }

    qrDetected = False
    timeToWait = 10 # Wait in seconds for wifi to connect after QR detection

    while True:

        qrDetected = wait_for_wifi_connect(qrDetected, timeToWait)

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
        retval, decoded_info, _ = detector.detectAndDecode(gray)

        if retval:
            qrDetected = process_raw_qr(retval, decoded_info, wifiCredentials)

        # cv2.imshow("QR Code Detection", gray)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    QRCodeReader_main()
    main()