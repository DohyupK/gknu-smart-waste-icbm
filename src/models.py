from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class WasteType(Enum):
    CAN = "Can"
    PLASTIC = "Plastic"
    GLASS = "Glass"
    PAPER = "Paper"
    UNKNOWN = "Unknown"


@dataclass
class ClassificationResult:
    label: WasteType
    confidence: float


class HandleClassificationResult(ABC):
    @abstractmethod
    def handleClassification(self, result: ClassificationResult):
        raise NotImplementedError

    def handle_classification(self, result: ClassificationResult):
        # Backward-compatible alias for snake_case callers.
        return self.handleClassification(result)
