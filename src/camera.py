import cv2
from typing import Any, Optional


class CameraManager:
    def __init__(self, index: int = 0):
        self.cap: Any = cv2.VideoCapture(index)

    def get_frame(self) -> Optional[Any]:
        ret, frame = self.cap.read()
        return frame if ret else None

    def release(self):
        self.cap.release()

