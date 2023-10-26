import cv2

# TODO
# Replace wifi config file and system command in js to python - replace bleno_connect.js
# combine both to replace BLEpiPipeline.py
# Replace BLEpiservice.txt to QRCodeReaderservice.txt with similar format
# Test
# if works remove all js, package files

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
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

    cv2.imshow("QR Code Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
