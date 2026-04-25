from .camera import CameraManager
from .inference import InferenceEngine, WasteClassifier
from .output_mgr import OutputM


def main():
    cam = CameraManager()
    engine = InferenceEngine("yolov8n.pt")
    output_system = OutputM()

    classifier = WasteClassifier(
        camera=cam,
        engine=engine,
        max_count=3,
        interval_ms=500,
        handler=output_system,
    )
    classifier.run()


if __name__ == "__main__":
    main()
