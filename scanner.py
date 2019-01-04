from imutils.video import VideoStream
from pyzbar.pyzbar import decode
import imutils
import cv2
import time

class QRScanner:

    def __init__(self, password):
        self.vs = VideoStream().start()
        self.is_running = True
        self.open_door = False
        self.password = password

    def run(self):
        start_time = time.time()
        end_time = time.time()

        while self.is_running and end_time - start_time < 300:
            frame = self.vs.read()
            frame = imutils.resize(frame, width=400)
            barcodes = decode(frame)
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type

                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                self.qr_decode_msg = barcodeData

                self.verify_data(barcodeData)

            cv2.imshow("Barcode Scanner", frame)
            self.quit()

            end_time = time.time()

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
        cv2.destroyAllWindows()
        self.vs.stop()

if __name__ == "__main__":
    password = "1234567890"
    qrscanner = QRScanner(password)
    open_door = qrscanner.run()
    if open_door:
        print("open door")
    else:
        print("close door")
