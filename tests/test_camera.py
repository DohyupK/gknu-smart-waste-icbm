import importlib
import sys
import types


def _load_camera_with_fake_cv2(monkeypatch):
    class FakeCapture:
        def __init__(self, _index):
            self.released = False

        def read(self):
            return True, "frame-1"

        def release(self):
            self.released = True

    fake_cv2 = types.SimpleNamespace(VideoCapture=FakeCapture)
    monkeypatch.setitem(sys.modules, "cv2", fake_cv2)
    sys.modules.pop("src.camera", None)
    return importlib.import_module("src.camera")


def test_camera_get_frame_success(monkeypatch):
    camera_module = _load_camera_with_fake_cv2(monkeypatch)
    camera = camera_module.CameraManager()
    assert camera.get_frame() == "frame-1"


def test_camera_get_frame_failure_and_release(monkeypatch):
    class FakeCapture:
        def __init__(self, _index):
            self.released = False

        def read(self):
            return False, None

        def release(self):
            self.released = True

    fake_cv2 = types.SimpleNamespace(VideoCapture=FakeCapture)
    monkeypatch.setitem(sys.modules, "cv2", fake_cv2)
    sys.modules.pop("src.camera", None)
    camera_module = importlib.import_module("src.camera")

    camera = camera_module.CameraManager()
    assert camera.get_frame() is None
    camera.release()
    assert camera.cap.released is True

