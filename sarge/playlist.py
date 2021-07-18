from PyQt5 import QtCore, QtWidgets


class PlaylistModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.horizontal_header = ['Title', 'Artist', 'Duration']
        self.data = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.horizontal_header)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.data[index.row()][index.column()]
        return None

    def setData(self, index, value, role):
        if role != QtCore.Qt.EditRole or not index.isValid() or index.column() != self.columnCount() - 1:
            return False
        # TODO: Needs implementing
        return False

    def headerData(self, index, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return self.horizontal_header[index]
        else:
            return str(index + 1)

    def appendRow(self, row):
        self.insertRows(self.rowCount(),[row])

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


class PlaylistView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        QtWidgets.QTableView.__init__(self, parent)
        column_weighting = [1, 1, 0]
        header = self.horizontalHeader()
        total_weight = 0
        for weight in column_weighting:
            total_weight = total_weight + weight
        total_size = 0
        for i in range(len(column_weighting)):
            total_size = total_size + header.sectionSize(i)
        length = header.length()
        for i in range(len(column_weighting)):
            if column_weighting == 0:
                continue
            new_size = total_size * column_weighting[i] / total_weight
            header.setDefaultSectionSize(i, new_size)
