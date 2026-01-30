import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QMessageBox, QInputDialog, QDialog, QDialogButtonBox, QToolBar)
from PySide6.QtWidgets import (
    QPushButton, QVBoxLayout,
    QWidget, QTextEdit,
    QLineEdit,QLabel, QFontDialog)
from PySide6.QtCore import Qt


class Dashboard_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.resize(800, 700)

        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("Main", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.toolbar_button_clicked)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction("RHUs", self)
        button_action2.setStatusTip("This is your button")
        button_action2.triggered.connect(self.toolbar_button_clicked)
        toolbar.addAction(button_action2)

        



    def toolbar_button_clicked(self, s):
        print("click", s)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard_window()
    window.show()
    sys.exit(app.exec())
