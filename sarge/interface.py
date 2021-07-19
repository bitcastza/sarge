###########################################################################
# Sarge is Copyright (C) 2021 Kyle Robbertze <kyle@bitcast.co.za>
#
# Sarge is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3, or
# any later version as published by the Free Software Foundation.
#
# Sarge is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sarge. If not, see <http://www.gnu.org/licenses/>.
###########################################################################
import sys
import sarge.resources
from importlib.resources import files, as_file
from threading import Thread
from pathlib import Path
from PyQt5 import QtCore, QtWidgets, QtMultimedia, uic
from .settings import SETTINGS
from .library import LibraryModel, LoadPlaylistThread
from .playlist import PlaylistItemWidget, PlaylistModelItem


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
        self.init_library()
        self.show()

    def init_instants(self):
        self.instants = []
        rows = SETTINGS['instants']['rows']
        columns = SETTINGS['instants']['columns']
        num_instants = rows * columns
        current_row = 0
        current_column = 0
        for i in range(num_instants):
            instant = InstantItem(self)
            self.pallet_layout.addWidget(instant, current_row, current_column)
            self.instants.append(instant)
            current_row = current_row + 1
            if current_row >= rows:
                current_column = current_column + 1
                current_row = 0

    def init_library(self):
        self.library_model = LibraryModel(self)
        self.library_view.setModel(self.library_model)
        path = Path(SETTINGS['music_directory']).expanduser()
        self.library_loader = LoadPlaylistThread(path, self.library_model)
        self.library_loader.finished.connect(self.library_loaded)
        self.statusBar().showMessage('Library loading...')
        self.library_loader.start()
        self.library_view.doubleClicked.connect(self.append_item_to_playlist)

    def library_loaded(self):
        self.statusBar().showMessage('Loaded library.')

    def closeEvent(self, event):
        if self.library_loader.isRunning():
            self.library_loader.quit()
        self.player.stop()
        event.accept()

    def append_item_to_playlist(self, index):
        row = self.playlist_view.count()
        data = index.data(QtCore.Qt.UserRole)
        item_model = PlaylistModelItem(data)
        self.playlist_view.insertItem(row, item_model)
        self.playlist_view.setItemWidget(item_model, PlaylistItemWidget(data))


class InstantItem(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_file = files(sarge.resources).joinpath('instant_widget.ui')
        with as_file(ui_file) as ui:
            uic.loadUi(ui, self)
        self.show()


class UserInterface:
    def run(self):
        app = QtWidgets.QApplication(sys.argv)
        ex = MainWindow()
        sys.exit(app.exec_())
