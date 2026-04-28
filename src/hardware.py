from enum import Enum
from gpiozero import DistanceSensor
from gpiozero.pins.lgpio import LGPIOFactory

factory = LGPIOFactory()

class SoundType(Enum):
    SUCCESS = "success"
    WARNING = "warning"


class DisplayC:
    def __init__(self):
        self.isScreenOn = True

    def showCategory(self, icon, text):
        print(f"[Display] 화면에 {icon} 아이콘 / 텍스트 '{text}' 표시")
        self.refreshScreen()

    def showWarning(self, message):
        print(f"[Display] 경고: {message}")
        self.refreshScreen()

    def refreshScreen(self):
        print("[Display] 화면 갱신")

    def show_category(self, text):
        self.showCategory(text, text)

    def show_warning(self, msg):
        self.showWarning(msg)


class AudioC:
    def __init__(self):
        self.volume = 5

    def playTTS(self, koreanText):
        print(f"[Audio] '이것은 {koreanText}입니다' 재생")

    def playEffect(self, soundType: SoundType):
        print(f"[Audio] 효과음 재생: {soundType.value}")

    def loadAudioFile(self, path):
        print(f"[Audio] 오디오 파일 로드 시도: {path}")
        return bool(path)

    def play_tts(self, text):
        self.playTTS(text)


class MotorC:
    def __init__(self, pinNumber=18):
        self.currentAngle = 0
        self.pinNumber = pinNumber

    def resetPosition(self):
        self.rotateTo(0)

    def rotateTo(self, angle):
        self.currentAngle = angle
        self.sendPWM(angle)
        print(f"[Motor] {angle}도로 회전하여 분류")

    def sendPWM(self, pulseWidth):
        print(f"[Motor] PWM 전송: pin={self.pinNumber}, pulse={pulseWidth}")

    def rotate_to(self, angle):
        self.rotateTo(angle)


class SensorC:
    def __init__(self, trig=23, echo=25, height_dist=720):
        self.sensor = DistanceSensor(echo=echo, trigger=trig, pin_factory=factory)
        self.empty_bin_dist = height_dist / 10.0
        self.fillThreshold = 0.8

    def checkFillLevel(self):
        current_dist = self.sensor.distance * 100
        filled_height = self.empty_bin_dist - current_dist
        fill_ratio = filled_height / self.empty_bin_dist
        return max(0.0, min(1.0, fill_ratio))

    def isFull(self):
        return self.checkFillLevel() >= self.fillThreshold

    def readAnalogValue(self):
        current_dist = self.sensor.distance * 100
        if current_dist > self.empty_bin_dist:
            current_dist = self.empty_bin_dist
        return (current_dist / self.empty_bin_dist) * 100

    def is_full(self):
        return self.isFull()


class BluetoothC:
    def __init__(self):
        self.isConnected = False

    def connect(self):
        self.isConnected = True
        print("[Bluetooth] 연결 완료")
        return self.isConnected

    def sendAlert(self, message):
        if not self.isConnected:
            self.connect()
        print(f"[Bluetooth] 스마트폰 앱으로 알림 전송: {message}")

    def send_alert(self, msg):
        self.sendAlert(msg)


class MobileApp:
    def __init__(self):
        self.isBluetoothOn = True

    def receiveAlert(self, msg):
        print(f"[MobileApp] 알림 수신: {msg}")
        self.showNotification()

    def showNotification(self):
        print("[MobileApp] 알림 배너 표시")


# Diagram compatibility alias.
ServoC = MotorC
