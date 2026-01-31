#w24024373 erinroserine
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QMessageBox, QInputDialog, QDialog, QDialogButtonBox)
from PySide6.QtWidgets import (
    QPushButton, QVBoxLayout,
    QWidget, QTextEdit,
    QLineEdit,QLabel, QFontDialog)
from PySide6.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt6 Dialogs with PySide6")
        self.resize(800,700)

        self.title = QLabel("PRISON HOUSING ALLOCATION SYSTEM")
        self.title.setText("<b><font color='red'>PRISON HOUSING ALLOCATION SYSTEM</font></b>")
        self.title.setAlignment(Qt.AlignCenter)


        self.pass_label = QLabel("Password")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter password")
        self.password.setEchoMode(QLineEdit.Password)

        # Button
        self.login_btn = QPushButton("Login")
        self.login_btn.setFixedWidth(80)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title)
        layout.addSpacing(30)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.password)
        layout.addSpacing(20)
        layout.addWidget(self.login_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
