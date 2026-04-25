import importlib
import sys
import types


class _TensorLike:
    def __init__(self, value):
        self._value = value

    def item(self):
        return self._value


class _Box:
    def __init__(self, cls_idx, conf):
        self.cls = _TensorLike(cls_idx)
        self.conf = _TensorLike(conf)


def _load_inference_module_with_predict_result(monkeypatch, predict_result):
    class DummyYOLO:
        def __init__(self, _model_path):
            self.names = {0: "can", 1: "plastic"}

        def predict(self, _frame, verbose=False):
            return predict_result

    fake_ultralytics = types.SimpleNamespace(YOLO=DummyYOLO)
    monkeypatch.setitem(sys.modules, "ultralytics", fake_ultralytics)
    sys.modules.pop("src.inference", None)
    return importlib.import_module("src.inference")


def test_engine_predict_extracts_label_and_confidence(monkeypatch):
    fake_result = [types.SimpleNamespace(boxes=[_Box(1, 0.91)])]
    inference_module = _load_inference_module_with_predict_result(monkeypatch, fake_result)
    engine = inference_module.InferenceEngine("dummy.pt")

    label, conf = engine.predict(frame="dummy-frame")
    assert label == "plastic"
    assert conf == 0.91


def test_engine_predict_empty_boxes(monkeypatch):
    fake_result = [types.SimpleNamespace(boxes=[])]
    inference_module = _load_inference_module_with_predict_result(monkeypatch, fake_result)
    engine = inference_module.InferenceEngine("dummy.pt")

    label, conf = engine.predict(frame="dummy-frame")
    assert label is None
    assert conf == 0.0


def test_engine_predict_chooses_highest_confidence_box(monkeypatch):
    fake_result = [types.SimpleNamespace(boxes=[_Box(0, 0.51), _Box(1, 0.93), _Box(0, 0.80)])]
    inference_module = _load_inference_module_with_predict_result(monkeypatch, fake_result)
    engine = inference_module.InferenceEngine("dummy.pt")

    label, conf = engine.predict(frame="dummy-frame")
    assert label == "plastic"
    assert conf == 0.93
