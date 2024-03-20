from threading import Thread
import cv2


class Multithreading:
    def __init__(self, src):
        self.capture = cv2.VideoCapture(src)
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
        # self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1536)
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.frame = None
        self.thread.start()

    def update(self):
        while True:
            _, self.frame = self.capture.read()

    def get_frame(self):
        return self.frame

    def get_time(self):
        return self.capture
