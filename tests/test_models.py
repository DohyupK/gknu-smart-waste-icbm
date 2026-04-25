from src.models import ClassificationResult, HandleClassificationResult, WasteType


def test_waste_type_values():
    assert WasteType.CAN.value == "Can"
    assert WasteType.PLASTIC.value == "Plastic"
    assert WasteType.GLASS.value == "Glass"
    assert WasteType.PAPER.value == "Paper"
    assert WasteType.UNKNOWN.value == "Unknown"


def test_classification_result_creation():
    result = ClassificationResult(label=WasteType.CAN, confidence=0.93)
    assert result.label is WasteType.CAN
    assert result.confidence == 0.93


def test_handler_interface_snake_case_alias():
    class DummyHandler(HandleClassificationResult):
        def __init__(self):
            self.called = False

        def handleClassification(self, result):
            self.called = result.label is WasteType.PLASTIC

    handler = DummyHandler()
    handler.handle_classification(ClassificationResult(WasteType.PLASTIC, 0.91))
    assert handler.called is True
