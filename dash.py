import json
import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QMessageBox, QInputDialog, QDialog, QDialogButtonBox, QToolBar, QTabWidget, QListView)
from PySide6.QtWidgets import (
    QPushButton, QVBoxLayout,
    QWidget, QTextEdit,
    QLineEdit, QLabel, QFontDialog)
from PySide6.QtCore import Qt, QStringListModel


# ---------------- BASIC OPTIONS ----------------

class Dashboard_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prison Housing Allocation System")
        self.resize(800, 700)

        # Create tab widget as central widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create toolbar
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("Main", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(lambda: self.toolbar_button_clicked("Main"))
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction("RHUs", self)
        button_action2.setStatusTip("This is your button")
        button_action2.triggered.connect(lambda: self.toolbar_button_clicked("RHUs"))
        toolbar.addAction(button_action2)

        toolbar.addSeparator()

        button_action3 = QAction("Allocations", self)
        button_action3.setStatusTip("This is your button")
        button_action3.triggered.connect(lambda: self.toolbar_button_clicked("Allocations"))
        toolbar.addAction(button_action3)

        toolbar.addSeparator()

        button_action4 = QAction("Releases", self)
        button_action4.setStatusTip("This is your button")
        button_action4.triggered.connect(lambda: self.toolbar_button_clicked("Releases"))
        toolbar.addAction(button_action4)

        toolbar.addSeparator()

        button_action5 = QAction("Costs", self)
        button_action5.setStatusTip("This is your button")
        button_action5.triggered.connect(lambda: self.toolbar_button_clicked("Costs"))
        toolbar.addAction(button_action5)

        # ---------------- LIST VIEW ----------------

        pending_widget = QWidget()
        pending_layout = QVBoxLayout()

        label = QLabel("Pending Licensees")
        label.setAlignment(Qt.AlignCenter)

        self.pending_list = QListView()

        self.fetch_data()
        self.data = self.all_data

        pending_display = []
        for i in self.data:
            if i["status"] == "Pending":
                days = i.get("days_until_housing")
                pending_display.append(f'{i["name"]} - {days} days left')

        pending_model = QStringListModel(pending_display)
        self.pending_list.setModel(pending_model)

        pending_layout.addWidget(label)
        pending_layout.addWidget(self.pending_list)
        pending_widget.setLayout(pending_layout)

        self.tabs.addTab(pending_widget, "Pending")

        allocated_widget = QWidget()
        allocated_layout = QVBoxLayout()

        label2 = QLabel("Allocated Licensees")
        label2.setAlignment(Qt.AlignCenter)

        self.allocated_list = QListView()

        allocated_display = []
        for i in self.data:
            if i["status"] == "Allocated":
                rhu = i.get("current_rhu")
                allocated_display.append(f'{i["name"]} - {rhu}')

        allocated_model = QStringListModel(allocated_display)
        self.allocated_list.setModel(allocated_model)

        allocated_layout.addWidget(label2)
        allocated_layout.addWidget(self.allocated_list)
        allocated_widget.setLayout(allocated_layout)

        self.tabs.addTab(allocated_widget, "Allocated")

        exited_widget = QWidget()
        exited_layout = QVBoxLayout()

        label3 = QLabel("Exited Licensees")
        label3.setAlignment(Qt.AlignCenter)

        self.exited_list = QListView()

        exited_display = []
        for i in self.data:
            if i["status"] == "Exited":
                exited_display.append(i["name"])

        exited_model = QStringListModel(exited_display)
        self.exited_list.setModel(exited_model)

        exited_layout.addWidget(label3)
        exited_layout.addWidget(self.exited_list)
        exited_widget.setLayout(exited_layout)

        self.tabs.addTab(exited_widget, "Exited")

        # Style the tabs
        self.setStyleSheet("""
            QTabBar::tab {
                color: #FF0000;
                padding: 10px;
            }
        """)

    def toolbar_button_clicked(self, button_name):
        print("click", button_name)

    def fetch_data(self):
        try:
            with open('prison_housing_data.json', 'r', encoding='utf-8') as f:
                self.all_data = json.load(f)
            print(" Loaded")
        except FileNotFoundError:
            print("prisoner_data.json not found")
            self.all_data = []
        except json.JSONDecodeError:
            print("Error reading JSON file")
            self.all_data = []
            #self.data = json.load()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard_window()
    window.show()
    sys.exit(app.exec())