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
import sarge.resources
from importlib_resources import files, as_file
from PyQt5 import QtCore, QtWidgets, uic


class PlaylistModelItem(QtWidgets.QListWidgetItem):
    def __init__(self, item, playout_engine, parent=None, type=QtWidgets.QListWidgetItem.ItemType.UserType):
        super().__init__(parent, type)
        self.item = item
        self.playout_engine = playout_engine

    def data(self, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.UserRole:
            return self.item
        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(400, 60)
        return super().data(role)


class PlaylistItemWidget(QtWidgets.QWidget):
    def __init__(self, item, playout_engine, parent=None):
        super().__init__(parent)
        self.item = item
        self.playout_engine = playout_engine
        ui_file = files(sarge.resources).joinpath('playlist_item.ui')
        with as_file(ui_file) as ui:
            uic.loadUi(ui, self)
        self.information_label.setText(self.item.title_artist())
        self.duration_label.setText(item.length)
        self.play_button.clicked.connect(self.play_song_on_playlist)
        self.show()

    def play_song_on_playlist(self):
        self.playout_engine.play_audio(self.item.filename)
