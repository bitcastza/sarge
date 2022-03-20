import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from .settings import Settings
from importlib_resources import files, as_file
import sarge.resources
import os


class CustomWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)
        self.button = QtWidgets.QPushButton("button")
        lay = QtWidgets.QHBoxLayout(self)
        lay.addWidget(self.button, alignment=Qt.AlignRight)
        lay.setContentsMargins(0, 0, 0, 0)


class PreferenceDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        ui_file = files(sarge.resources).joinpath('preference_window.ui')
        with as_file(ui_file) as ui:
            uic.loadUi(ui, self)
        self.init_preference()

    def init_preference(self):
        self.column_field.setText(self.settings.sarge_columns)
        self.sample_rate_field.setText(self.settings.sarge_player_sample_rate)
        self.model = QtGui.QStandardItemModel(self.files_list)
        self.select_files.clicked.connect(self.select_instant_files)
        self.directory_path.setText(self.settings.music_directory)
        self.browse_button.clicked.connect(self.select_directory)
        self.apply_button.clicked.connect(self.save_changes)

    def select_instant_files(self):
        all_files = []
        filename = QFileDialog.getOpenFileName(self.select_files, "Open file")

        if os.path.basename(filename[0]) != "":
            all_files.append(os.path.basename(filename[0]))
            self.files_list.setModel(self.model)

            for file in all_files:
                item = QtGui.QStandardItem(file)
                self.model.appendRow(item)
                self.files_list.setIndexWidget(item.index(), CustomWidget())

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self.browse_button, "Open directory", self.directory_path.text())
        self.directory_path.setText(directory)

    def delete_item_from_list(self):
        for index in self.files_list.selectedIndexes():
            selected_item = self.files_list.model().itemFromIndex(index)
            model = self.files_list.model()
            for item in model.findItems(selected_item.text()):
                model.removeRow(item.row())

    def save_changes(self):
        sarge_settings = Settings()
        sarge_settings.sarge_columns = self.column_field.text()
        sarge_settings.sarge_player_sample_rate = self.sample_rate_field.text()
        sarge_settings.sarge_player_channel = self.channels_field.currentText()
        sarge_settings.music_directory = self.directory_path.text()
        # Still investigating how to set the settings.sarge_files because we need
        # all the content of the list but I don't know how to get it


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    interface = PreferenceDialog()
    settings = Settings()
    combobox_index = interface.channels_field.findText(settings.sarge_player_channel, Qt.MatchFixedString)
    interface.channels_field.setCurrentIndex(combobox_index)
    interface.cancel_button.clicked.connect(lambda: PreferenceDialog.close(interface))
    interface.show()
    sys.exit(app.exec_())
