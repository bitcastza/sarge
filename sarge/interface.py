import sys
import sarge.resources
from importlib.resources import files, as_file
from PyQt5 import QtWidgets, uic
from .settings import SETTINGS
from .playlist import PlaylistModel


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file = files(sarge.resources).joinpath('main_window.ui')
        with as_file(ui_file) as ui:
            uic.loadUi(ui, self)
        self.init_ui()

    def init_ui(self):
        self.init_instants()
        self.library_model = PlaylistModel()
        self.library_view.setModel(self.library_model)
        self.show()

    def init_instants(self):
        self.instants = []
        rows = SETTINGS['instants']['rows']
        columns = SETTINGS['instants']['columns']
        num_instants = rows * columns
        current_row = 0
        current_column = 0
        for i in range(num_instants):
            instant = InstantItem()
            self.pallet_layout.addWidget(instant, current_row, current_column)
            self.instants.append(instant)
            current_row = current_row + 1
            if current_row >= rows:
                current_column = current_column + 1
                current_row = 0


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
