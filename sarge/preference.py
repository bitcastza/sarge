from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from .settings import Settings
from importlib_resources import files, as_file
import sarge.resources
import os


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
        self.files_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.select_files.clicked.connect(self.select_instant_files)
        self.directory_path.setText(self.settings.music_directory)
        if len(self.settings.sarge_files) != 0:
            for file in self.settings.sarge_files:
                self.files_list.addItem(file)

        self.browse_button.clicked.connect(self.select_directory)
        self.apply_button.clicked.connect(self.save_changes)
        self.delete_button.clicked.connect(self.delete_selected_items)

    def select_instant_files(self):
        all_files = []
        filename = QFileDialog.getOpenFileName(self.select_files,
                                               "Open file", "", "Audio "
                                               "files(*.au *.mid *.rmi *.mp3 *.mp4 "
                                               "*.ogg *.aif *.aiff *.m3u *.ra *.ram "
                                               "*.vorbis *.snd *.wav)")

        if os.path.basename(filename[0]) != "":
            all_files.append(filename[0])
        filename = QFileDialog.getOpenFileName(self.pushButton, "Open file", "", "Audio "
                                                                                 "files(*.au *.mid *.rmi *.mp3 *.mp4 "
                                                                                 "*.ogg *.aif *.aiff *.m3u *.ra *.ram "
                                                                                 "*.vorbis *.snd *.wav)")
        if os.path.basename(filename[0]) != "":
            all_files.append(os.path.basename(filename[0]))

            for file in all_files:
                self.files_list.addItem(file)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self.browse_button, "Open directory", self.directory_path.text())
        if directory is not None:
            self.directory_path.setText(directory)

    def delete_selected_items(self):
        items = self.files_list.selectedItems()
        for item in items:
            self.files_list.takeItem(self.files_list.row(item))

    def save_changes(self):
        channel_value = {"Mono": 1, "Stereo": 2}
        sarge_settings = Settings()
        sarge_settings.sarge_columns = int(self.column_field.text())
        sarge_settings.sarge_player_sample_rate = int(self.sample_rate_field.text())
        sarge_settings.sarge_player_channel = channel_value[self.channels_field.currentText()]
        sarge_settings.music_directory = self.directory_path.text()
        sarge_settings.sarge_files = [self.files_list.item(i).text() for i in range(self.files_list.count())]
