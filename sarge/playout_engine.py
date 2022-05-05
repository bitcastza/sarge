from .settings import Settings
from PyQt5.QtCore import QFile, QIODevice
from PyQt5.QtMultimedia import QAudioOutput, QAudioFormat, QAudioDeviceInfo


class PlayOutEngine:
    def __init__(self, item):
        self.settings = Settings()
        self.item = item
        self.sound_file = QFile()
        self.sound_file.setFileName(str(self.item.filename))
        self.sound_file.open(QIODevice.ReadOnly)

        player_format = QAudioFormat()
        player_format.setSampleRate(8000)
        player_format.setChannelCount(1)
        player_format.setSampleSize(8)
        player_format.setCodec("audio/pcm")
        player_format.setByteOrder(QAudioFormat.LittleEndian)
        player_format.setSampleType(QAudioFormat.UnSignedInt)

        info = QAudioDeviceInfo.defaultOutputDevice()
        if not info.isFormatSupported(player_format):
            print("Raw audio fmt not supported by backend, cannot play audio.")

        self.player = QAudioOutput(player_format)

    def play_audio(self):
        self.player.start(self.sound_file)

    def stop_audio(self):
        self.player.stop()
