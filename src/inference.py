import time
from typing import Any, Optional

from ultralytics import YOLO

from .models import ClassificationResult, HandleClassificationResult, WasteType


class InferenceEngine:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def predict(self, frame: Any):
        res = self.model.predict(frame, verbose=False)
        if res and len(res[0].boxes) > 0:
            boxes = res[0].boxes
            box = max(boxes, key=lambda b: b.conf.item())
            return self.model.names[int(box.cls.item())], box.conf.item()
        return None, 0.0


class WasteClassifier:
    def __init__(
        self,
        camera=None,
        engine: Optional[InferenceEngine] = None,
        max_count: int = 3,
        interval_ms: int = 1000,
        handler: Optional[HandleClassificationResult] = None,
        camera_mgr=None,
    ):
        self.camera = camera if camera is not None else camera_mgr
        self.engine = engine
        self.handler = handler
        self.max_count = max_count
        self.interval_ms = interval_ms
        self.last_label = None
        self.consecutive_count = 0

    def validate(self, label: Optional[str], conf: float) -> bool:
        if not label or conf < 0.8:
            self.consecutive_count = 0
            return False

        if label == self.last_label:
            self.consecutive_count += 1
        else:
            self.last_label = label
            self.consecutive_count = 1

        return self.consecutive_count == self.max_count

    def map_to_enum(self, label_str: Optional[str]) -> WasteType:
        if not label_str:
            return WasteType.UNKNOWN

        mapping = {
            "can": WasteType.CAN,
            "plastic": WasteType.PLASTIC,
            "glass": WasteType.GLASS,
            "paper": WasteType.PAPER,
            "unknown": WasteType.UNKNOWN,
        }
        return mapping.get(label_str.lower(), WasteType.UNKNOWN)

    def _dispatch_result(self, result: ClassificationResult):
        if not self.handler:
            return

        # Prefer diagram-aligned camelCase API first.
        camel = getattr(self.handler, "handleClassification", None)
        if callable(camel):
            camel(result)
            return

        legacy = getattr(self.handler, "handle_classification", None)
        if callable(legacy):
            legacy(result)

    def run(self):
        print("시스템 가동...")
        try:
            while True:
                frame = self.camera.get_frame()
                if frame is None:
                    print("[Warning] 프레임을 읽지 못했습니다. 다시 시도합니다...")
                    time.sleep(0.1)
                    continue

                label, conf = self.engine.predict(frame)
                if self.validate(label, conf):
                    result = ClassificationResult(
                        label=self.map_to_enum(label),
                        confidence=conf,
                    )
                    self._dispatch_result(result)

                time.sleep(self.interval_ms / 1000.0)
        finally:
            self.camera.release()
