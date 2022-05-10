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
import os
import mutagen
from threading import Thread
from PyQt5 import QtCore, QtWidgets
from .utils import get_metadata

TABLE_ORDER = ['title', 'artist', 'length']


class LoadPlaylistThread(QtCore.QThread):
    def __init__(self, directory, model, parent=None):
        super().__init__(parent)
        self.directory = directory
        self.model = model

    def run(self):
        rows = []
        for root, dirs, files in os.walk(self.directory):
            for name in files:
                try:
                    item = get_metadata(os.path.join(root, name))
                    if item is None:
                        continue
                    rows.append(item)
                except mutagen.MutagenError:
                    continue
        self.model.appendRows(rows)


class LibraryModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.horizontal_header = list(map(lambda n: n.title(), TABLE_ORDER))
        self._data = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.horizontal_header)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            item = self._data[index.row()]
            return getattr(item, TABLE_ORDER[index.column()])
        if role == QtCore.Qt.UserRole:
            return self._data[index.row()]
        return None

    def headerData(self, index, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return self.horizontal_header[index]
        else:
            return str(index + 1)

    def appendRow(self, row):
        self.insertRow(self.rowCount(), row)

    def appendRows(self, rows):
        self.insertRows(self.rowCount(), rows)

    def insertRows(self, row, rows, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, row, row + len(rows) - 1)
        for i in range(len(rows)):
            row_i = row + i
            self._data.insert(row_i, rows[i])
        self.endInsertRows()

    def insertRow(self, row, row_data):
        self.insertRows(row, [row_data])

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(count):
            del self._data[row + count - 1]
        self.endRemoveRows()
        return True

    def removeRow(self, row):
        self.removeRows(row, 1)

    def moveRows(self, source_parent, source_first, source_last,
                 destination_parent, destination):
        self.beginMoveRows(source_parent, source_first, source_last,
                           destination_parent, destination)
        items = self._data[source_first:source_last + 1]
        self._data = self._data[:source_first] + self._data[source_last + 1:]
        for i in range(len(items)):
            self._data.insert(destination + i, items[i])
        self.endMoveRows()


class LibraryView(QtWidgets.QTableView):
    column_ratio = [6, 4, 1]

    def resizeEvent(self, event):
        width = self.width()
        total_size = sum(self.column_ratio)
        for i in range(len(self.column_ratio)):
            self.setColumnWidth(i, int(width * self.column_ratio[i] / total_size))
