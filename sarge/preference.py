# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sarge.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QPushButton, QHBoxLayout
import os
from PyQt5.QtCore import Qt
from settings import Settings


class CustomWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)
        self.button = QPushButton("delete")
        lay = QHBoxLayout(self)
        lay.addWidget(self.button, alignment=Qt.AlignRight)
        lay.setContentsMargins(0, 0, 0, 0)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(551, 563)
        self.settings = Settings()
        self.Instants_label = QtWidgets.QLabel(Dialog)
        self.Instants_label.setGeometry(QtCore.QRect(20, 20, 81, 21))
        self.Instants_label.setObjectName("Instants_label")
        self.columns_label = QtWidgets.QLabel(Dialog)
        self.columns_label.setGeometry(QtCore.QRect(20, 50, 131, 31))
        self.columns_label.setObjectName("columns_label")
        self.library_label = QtWidgets.QLabel(Dialog)
        self.library_label.setGeometry(QtCore.QRect(20, 240, 71, 31))
        self.library_label.setObjectName("library_label")
        self.directory_label = QtWidgets.QLabel(Dialog)
        self.directory_label.setGeometry(QtCore.QRect(20, 300, 111, 31))
        self.directory_label.setObjectName("directory_label")
        self.Player_label = QtWidgets.QLabel(Dialog)
        self.Player_label.setGeometry(QtCore.QRect(20, 360, 71, 31))
        self.Player_label.setObjectName("Player_label")
        self.channel_label = QtWidgets.QLabel(Dialog)
        self.channel_label.setGeometry(QtCore.QRect(20, 410, 71, 16))
        self.channel_label.setObjectName("channel_label")
        self.sample_rate_label = QtWidgets.QLabel(Dialog)
        self.sample_rate_label.setGeometry(QtCore.QRect(20, 460, 91, 21))
        self.sample_rate_label.setObjectName("sample_rate_label")
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        self.cancel_button.setGeometry(QtCore.QRect(320, 490, 75, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.cancel_button.setFont(font)
        self.cancel_button.setObjectName("cancel_button")
        self.apply_button = QtWidgets.QPushButton(Dialog)
        self.apply_button.setGeometry(QtCore.QRect(410, 490, 75, 31))
        self.apply_button.clicked.connect(self.save_changes)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.apply_button.setFont(font)
        self.apply_button.setObjectName("apply_button")
        self.sample_rate_field = QtWidgets.QLineEdit(Dialog)
        self.sample_rate_field.setGeometry(QtCore.QRect(170, 460, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sample_rate_field.setFont(font)
        self.sample_rate_field.setObjectName("sample_rate_field")
        self.sample_rate_field.setText(str(self.settings.sarge_player_sample_rate))
        self.browse_button = QtWidgets.QPushButton(Dialog)
        self.browse_button.setGeometry(QtCore.QRect(380, 310, 91, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.browse_button.setFont(font)
        self.browse_button.setObjectName("browse_button")
        self.browse_button.clicked.connect(self.select_directory)
        self.column_field = QtWidgets.QLineEdit(Dialog)
        self.column_field.setText(self.settings.sarge_columns)
        self.column_field.setGeometry(QtCore.QRect(170, 59, 113, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.column_field.setFont(font)
        self.column_field.setObjectName("column_field")
        self.channels_field = QtWidgets.QComboBox(Dialog)
        self.channels_field.setGeometry(QtCore.QRect(170, 410, 121, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.channels_field.setFont(font)
        self.channels_field.setObjectName("channels_field")
        self.channels_field.addItem("")
        self.channels_field.addItem("")
        self.channels_field.setItemText(0, self.settings.sarge_player_channel)
        self.instant_files_label = QtWidgets.QLabel(Dialog)
        self.instant_files_label.setGeometry(QtCore.QRect(20, 110, 101, 21))
        self.instant_files_label.setObjectName("instant_files_label")
        self.select_files = QtWidgets.QPushButton(Dialog)
        self.select_files.setGeometry(QtCore.QRect(170, 230, 261, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.select_files.setFont(font)
        self.select_files.setObjectName("select_files")
        self.select_files.clicked.connect(self.select_instant_files)

        self.directory_path = QtWidgets.QLineEdit(Dialog)
        self.directory_path.setGeometry(QtCore.QRect(170, 310, 201, 21))
        self.directory_path.setObjectName("directory_path")
        self.directory_path.setText(self.settings.music_directory)
        self.files_list = QtWidgets.QListView(Dialog)
        self.files_list.setGeometry(QtCore.QRect(170, 100, 261, 131))
        self.files_list.setObjectName("files_list")
        model = QtGui.QStandardItemModel(self.files_list)
        self.files_list.setModel(model)
        for row in self.settings.sarge_files:
            item = QtGui.QStandardItem(row)
            model.appendRow(item)

        self.model = QtGui.QStandardItemModel(self.files_list)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

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

    def save_changes(self):
        settings = Settings()
        settings.sarge_columns = self.column_field.text()
        settings.sarge_player_sample_rate = self.sample_rate_field.text()
        settings.sarge_player_channel = self.channels_field.currentText()
        settings.music_directory = self.directory_path.text()
        # Still investigating how to set the settings.sarge_files because we need
        # all the content of the list but I don't know how to get it

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Preferences"))
        self.Instants_label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:16pt;\">Instants</span></p></body></html>"))
        self.columns_label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:11pt;\">Number of columns</span></p></body></html>"))
        self.library_label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:16pt;\">Library</span></p></body></html>"))
        self.directory_label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:11pt;\">Library directory</span></p></body></html>"))
        self.Player_label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:16pt;\">Player</span></p></body></html>"))
        self.channel_label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:11pt; color:#000000;\">Channels</span></p></body></html>"))
        self.sample_rate_label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:11pt; color:#000000;\">Sample rate</span></p></body></html>"))
        self.cancel_button.setText(_translate("Dialog", "Cancel"))
        self.apply_button.setText(_translate("Dialog", "Apply"))
        self.sample_rate_field.setPlaceholderText(_translate("Dialog", "Enter a value"))
        self.browse_button.setText(_translate("Dialog", "Browse"))
        self.column_field.setPlaceholderText(_translate("Dialog", "Enter a value"))
        self.channels_field.setItemText(0, _translate("Dialog", "Mono"))
        self.channels_field.setItemText(1, _translate("Dialog", "Stereo"))
        self.instant_files_label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:11pt;\">Instant files</span></p></body></html>"))
        self.select_files.setText(_translate("Dialog", "+"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    ui.cancel_button.clicked.connect(lambda: Dialog.close())
    Dialog.show()
    sys.exit(app.exec_())
