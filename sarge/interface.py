import sys
import sarge.resources
from importlib.resources import files, as_file
from PyQt5 import QtWidgets, uic
from .settings import SETTINGS


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file = files(sarge.resources).joinpath('main_window.ui')
        with as_file(ui_file) as ui:
            uic.loadUi(ui, self)
        self.init_ui()

    def init_ui(self):
        self.instants = []
        for i in range(4):
            instant = InstantItem()
            self.pallet_layout.addWidget(instant,
                                         i // SETTINGS['instants']['rows'],
                                         i % SETTINGS['instants']['columns'])
            self.instants.append(instant)
        self.show()


class InstantItem(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        ui_file = files(sarge.resources).joinpath('instant_widget.ui')
        with as_file(ui_file) as ui:
            uic.loadUi(ui, self)
        self.show()


class UserInterface:
    def run(self):
        app = QtWidgets.QApplication(sys.argv)
        ex = MainWindow()
        sys.exit(app.exec_())
