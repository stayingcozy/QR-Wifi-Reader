import cv2
import time

# Local imports
from wifiConfig import write_wifi_credentials_lp, get_wireless_interface
from wifiStatus import wifi_check_lp
from uidWrite import write_uid

def wait_for_wifi_connect(qrDetected, timeToWait):
    
    # If qr code is detected wait for comp to connect to wifi
    start = time.time()
    while qrDetected:
        tdelta = time.time() - start
        if tdelta < timeToWait:
            if wifi_check_lp():
                break
        else:
            return False
        
    return False

def process_raw_qr(retval, decoded_info, wifiCredentials):

    for info in decoded_info:

        # Process raw input
        str_retval = str(retval)
        split_info = str_retval.split(" ; ")

        wifiCredentials["device"] = get_wireless_interface()

        if len(split_info) == 2:
            print("Detected QR Code")
            wifiCredentials["ssid"] = split_info[0]
            wifiCredentials["psk"] = split_info[1]

            write_wifi_credentials_lp(wifiCredentials)

            # qrDetected = True
            return True
        
        if len(split_info) == 3:
            print("Detected QR Code")
            wifiCredentials["ssid"] = split_info[0]
            wifiCredentials["psk"] = split_info[1]
            uid= split_info[2]

            write_uid(uid)
            write_wifi_credentials_lp(wifiCredentials)

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
    "device": '',
    }

    qrDetected = False
    timeToWait = 10 # Wait in seconds for wifi to connect after QR detection

    while True:

        qrDetected = wait_for_wifi_connect(qrDetected, timeToWait)

        if wifi_check_lp():
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