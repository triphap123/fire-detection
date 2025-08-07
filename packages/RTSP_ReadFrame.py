# rtsp_reader.py
import cv2
import threading

class RTSPReader:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src, cv2.CAP_FFMPEG)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
        self.latest_frame = None
        self.running = True
        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.latest_frame = frame

    def read(self):
        return self.latest_frame

    def stop(self):
        self.running = False
        self.cap.release()
