import sys
from PyQt5.QtCore import QSettings, QVariant
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox, QFileDialog


# We need to a way to use QSettings instead of settings in settings.py, below is my attempt
# self.myTableWidget.setItem(X, Y, QtWidgets.QTableWidgetItem('TEXT'))


class Dialog(QDialog):
    """Dialog."""

    def __init__(self, parent=None):
        def pick_directory():
            dialog = QFileDialog()
            folder_path = dialog.getExistingDirectory(None, "Select Folder")
            return folder_path

        settings = QSettings()
        self.columns = ["Select columns", "1", "2", "3"]

        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Preferences')
        colLayout = QHBoxLayout()
        fileLayout = QHBoxLayout()
        sampleLayout = QHBoxLayout()
        channelLayout = QHBoxLayout()
        self.col = QComboBox()
        self.files = QComboBox()
        self.sample_rate = QComboBox()
        self.channels = QComboBox()
        self.new_directory = QPushButton()
        self.new_directory.setText("--Select Directory--")
        self.col.addItems(self.columns)
        settings.setValue('Columns', self.columns)
        self.files.addItems(["Select files",
                             '~/music/jingles/Station ID III (2017).mp3',
                             '~/music/jingles/This is UCT Radio (Voice Only).mp3',
                             '~/music/jingles/Transition Effect.mp3',
                             '~/music/jingles/Turn It Up ( The Soundtrack to Your Campus life).mp3'
                             ])
        self.new_directory.clicked.connect(pick_directory)
        self.sample_rate.addItems(["Choose sample rate", "48000", "50000"])
        self.channels.addItems(["choose channel", "1", "2"])
        colLayout.addWidget(self.col)
        fileLayout.addWidget(self.files)
        sampleLayout.addWidget(self.sample_rate)
        channelLayout.addWidget(self.channels)
        dlgLayout = QVBoxLayout()
        playComps = QFormLayout()
        playComps.addRow("sample rate:", sampleLayout)
        playComps.addRow("channels:", channelLayout)
        formLayout = QFormLayout()
        formLayout.addRow('Columns:', colLayout)
        formLayout.addRow('Files:', fileLayout)
        formLayout.addRow('Music directory:', self.new_directory)
        formLayout.addRow('Player:', playComps)
        dlgLayout.addLayout(formLayout)
        btns = QDialogButtonBox()
        btns.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        dlgLayout.addWidget(btns)
        self.setLayout(dlgLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())
