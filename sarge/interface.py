import sys
import sarge.resources
from importlib.resources import files, as_file
from threading import Thread
from pathlib import Path
from PyQt5 import QtCore, QtWidgets, QtMultimedia, uic
from .settings import SETTINGS
from .library import LibraryModel, LoadPlaylistThread


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_player()
        ui_file = files(sarge.resources).joinpath('main_window.ui')
        with as_file(ui_file) as ui:
            uic.loadUi(ui, self)
        self.init_ui()

    def init_player(self):
        player_format = QtMultimedia.QAudioFormat()
        player_format.setSampleRate(SETTINGS['player']['sample_rate'])
        player_format.setChannelCount(SETTINGS['player']['channels'])
        player_format.setSampleSize(8)
        player_format.setCodec("audio/pcm")
        player_format.setByteOrder(QtMultimedia.QAudioFormat.LittleEndian)
        player_format.setSampleType(QtMultimedia.QAudioFormat.UnSignedInt)
        self.player = QtMultimedia.QAudioOutput(player_format, self)
        self.player.start()

    def init_ui(self):
        self.init_instants()
        self.library_model = LibraryModel()
        self.library_view.setModel(self.library_model)
        path = Path(SETTINGS['music_directory']).expanduser()
        self.library_loader = LoadPlaylistThread(path, self.library_model)
        self.library_loader.finished.connect(self.library_loaded)
        self.statusBar().showMessage('Library loading...')
        self.library_loader.start()
        self.show()

    def init_instants(self):
        self.instants = []
        rows = SETTINGS['instants']['rows']
        columns = SETTINGS['instants']['columns']
        num_instants = rows * columns
        current_row = 0
        current_column = 0
        for i in range(num_instants):
            instant = InstantItem()
            self.pallet_layout.addWidget(instant, current_row, current_column)
            self.instants.append(instant)
            current_row = current_row + 1
            if current_row >= rows:
                current_column = current_column + 1
                current_row = 0

    def library_loaded(self):
        self.statusBar().showMessage('Loaded library.')

    def closeEvent(self, event):
        if self.library_loader.isRunning():
            self.library_loader.quit()
        self.player.stop()
        event.accept()


class InstantItem(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        ui_file = files(sarge.resources).joinpath('instant_widget.ui')
        with as_file(ui_file) as ui:
            uic.loadUi(ui, self)
        self.show()


class UserInterface:
    def run(self):
        app = QtWidgets.QApplication(sys.argv)
        ex = MainWindow()
        sys.exit(app.exec_())
