from .settings import Settings
from PyQt5.QtCore import QIODevice, QBuffer
from PyQt5.QtMultimedia import QAudioOutput, QAudioFormat, QAudioDeviceInfo
import io
from pydub import AudioSegment


class PlayOutEngine:
    def __init__(self):
        self.settings = Settings()

        self.player_format = QAudioFormat()
        self.player_format.setSampleRate(self.settings.sarge_player_sample_rate)
        self.player_format.setChannelCount(self.settings.sarge_player_channel)
        self.player_format.setSampleSize(16)
        self.player_format.setCodec("audio/pcm")
        self.player_format.setByteOrder(QAudioFormat.LittleEndian)
        self.player_format.setSampleType(QAudioFormat.UnSignedInt)

        info = QAudioDeviceInfo.defaultOutputDevice()
        if not info.isFormatSupported(self.player_format):
            print("Raw audio format not supported by backend, cannot play audio")

        self.player = QAudioOutput(self.player_format)
        self.audio_device = self.player.start()

    def mp3_transcode(self, filename):
        data = open(filename, "rb").read()
        seg = AudioSegment.from_file(io.BytesIO(data))
        seg = seg.set_frame_rate(self.settings.sarge_player_sample_rate)
        seg = seg.set_channels(self.settings.sarge_player_channel)
        seg = seg.set_sample_width(2)
        wave_io = io.BytesIO()
        seg.export(wave_io, format='wav')
        return wave_io.getvalue()

    def play_audio(self, filename):
        self.buffer = QBuffer()
        data = self.mp3_transcode(filename)
        self.buffer.setData(data)
        self.buffer.open(QIODevice.ReadOnly)
        self.buffer_size = self.buffer.size()
        self.player.setBufferSize(self.buffer_size)
        transcoded_bytes = self.buffer.read(self.buffer_size)
        self.audio_device.writeData(transcoded_bytes)

    def stop_audio(self):
        self.player.stop()
