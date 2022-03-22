from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from settings import Settings
from importlib_resources import files, as_file
import sarge.resources
import os


class CustomWidgetDeleteButton(QtWidgets.QWidget):
    # This is the delete button that shows up next to each of the
    # items in the ListView so we can delete them
    def __init__(self, parent=None):
        super(CustomWidgetDeleteButton, self).__init__(parent)
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
        self.column_field.setText(str(self.settings.sarge_columns))
        self.sample_rate_field.setText(str(self.settings.sarge_player_sample_rate))
        self.model = QtGui.QStandardItemModel(self.files_list)
        self.select_files.clicked.connect(self.select_instant_files)
        self.directory_path.setText(self.settings.music_directory)
        self.browse_button.clicked.connect(self.select_directory)
        self.apply_button.clicked.connect(self.save_changes)
        self.apply_button.clicked.connect(self.close)
        # still checking on the part to reload UI

    def select_instant_files(self):
        all_files = []
        filename = QFileDialog.getOpenFileName(self.select_files, "Open file")

        if os.path.basename(filename[0]) != "":
            all_files.append(os.path.basename(filename[0]))
            self.files_list.setModel(self.model)

            for file in all_files:
                item = QtGui.QStandardItem(file)
                self.model.appendRow(item)
                self.files_list.setIndexWidget(item.index(), CustomWidgetDeleteButton())

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
        channel_value = {"Mono": 1, "Stereo": 2}
        sarge_settings = Settings()
        sarge_settings.sarge_columns = int(self.column_field.text())
        sarge_settings.sarge_player_sample_rate = int(self.sample_rate_field.text())
        sarge_settings.sarge_player_channel = channel_value[self.channels_field.currentText()]
        sarge_settings.music_directory = self.directory_path.text()

        # Still investigating how to set the settings.sarge_files because we need
        # all the content of the list but I don't know how to get it
