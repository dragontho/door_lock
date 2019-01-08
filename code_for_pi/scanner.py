from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from pyzbar.pyzbar import decode
 
class QRScanner:

    def __init__(self, password):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        self.is_running = True
        self.open_door = False
        self.password = password

    def run(self):
        start_time = time.time()
        end_time = time.time()
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            barcodes = decode(image)
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(image, text, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                self.verify_data(barcodeData)
            cv2.imshow("QRCode Scanner", image)
            self.rawCapture.truncate(0)
            self.quit()
            end_time = time.time()
            if (self.open_door or (end_time - start_time > 60)):
                break

        return self.open_door

    def verify_data(self, data):
        if self.password == data:
            self.is_running = False
            self.open_door = True

    def quit(self):
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            self.is_running = False

    def __del__(self):
        print("Close camera")
        cv2.destroyAllWindows()

if __name__ == "__main__":
    password = "1234567890"
    qrscanner = QRScanner(password)
    open_door = qrscanner.run()
    if open_door:
        print("open door")
    else:
        print("close door")
