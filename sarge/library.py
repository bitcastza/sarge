import os
import mutagen
from threading import Thread
from PyQt5 import QtCore, QtWidgets

TABLE_ORDER = [ 'title', 'artist', 'length' ]

def get_key(metadata, key, default=None):
    try:
        return metadata[key][0]
    except KeyError:
        return default


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
                    metadata = mutagen.File(os.path.join(root, name), easy=True)
                    if metadata == None:
                        continue
                    length = metadata.info.length
                    item = {
                        'title': get_key(metadata, 'title', name),
                        'artist': get_key(metadata, 'artist'),
                        'length': '{:0>2.0f}:{:0>2.0f}'.format(length//60, length%60),
                        'filename': name,
                        'file': os.path.join(root, name),
                    }
                    rows.append(item)
                except mutagen.MutagenError:
                    continue
        self.model.appendRows(rows)


class LibraryModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.horizontal_header = list(map(lambda n : n.title(), TABLE_ORDER))
        self.data = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.horizontal_header)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.data[index.row()][TABLE_ORDER[index.column()]]
        return None

    def headerData(self, index, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return self.horizontal_header[index]
        else:
            return str(index + 1)

    def appendRow(self, row):
        self.insertRows(self.rowCount(),[row])

    def appendRows(self, rows):
        self.insertRows(self.rowCount(), rows)

    def insertRows(self, row, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, row, row + len(rows) - 1)
        for i in range(len(rows)):
            row_i = row + i
            self.data.insert(row_i, rows[i])
        self.endInsertRows()

    def insertRow(self, row, row_data):
        self.insertRows(row, [row_data])

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(count):
            del self.data[row + count - 1]
        self.endRemoveRows()
        return True

    def removeRow(self, row):
        self.removeRows(row, 1)

    def moveRows(self, source_parent, source_first, source_last,
            destination_parent, destination):
        self.beginMoveRows(source_parent, source_first, source_last,
                           destination_parent, destination)
        items = self.data[source_first:source_last + 1]
        self.data = self.data[:source_first] + self.data[source_last + 1:]
        for i in range(len(items)):
            self.data.insert(destination + i, items[i])
        self.endMoveRows()


class LibraryView(QtWidgets.QTableView):
    column_ratio = [6, 4, 1]

    def resizeEvent(self, event):
        width = self.width()
        total_size = sum(self.column_ratio)
        for i in range(len(self.column_ratio)):
            self.setColumnWidth(i, int(width * self.column_ratio[i] / total_size))
