#w24024373 erin rose rine
import sys
import json

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,
    QListWidget, QListWidgetItem,
    QTabWidget, QDialog, QToolBar, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt


# ---------------- DIALOG CLASS ----------------
class AllocationDialog(QDialog):
    def __init__(self, licensee, rhus, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Allocate {licensee['name']}")
        self.resize(600, 500)
        self.licensee = licensee
        self.rhus = rhus
        self.selected_rhus = []

        layout = QVBoxLayout()

        header = QLabel(f"Allocate: {licensee['name']}")
        header.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(header)



        self.results_list = QListWidget()
        self.populate_matches()
        layout.addWidget(self.results_list)

        choose_label = QLabel("Choose RHU")
        layout.addWidget(choose_label)

        self.checkbox_widgets = []
        for rhu in rhus:
            cb = QCheckBox(rhu['name'])
            layout.addWidget(cb)
            self.checkbox_widgets.append((cb, rhu))

        save_btn = QPushButton("[Save button]")
        save_btn.clicked.connect(self.save_allocation)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    # ---------------- MATCHES ----------------

    def populate_matches(self):
        for rhu in self.rhus:
            matches = []

            if self.licensee.get('nighttime_curfew') == rhu.get('provides_curfew'):
                matches.append("Curfew match")
            if self.licensee.get('drug_searches_required') == rhu.get('provides_drug_searches'):
                matches.append("Drug searches match")
            if self.licensee.get('gender') in rhu.get('accepts_gender', ''):
                matches.append("Gender match")

            if len(matches) == 3:
                status = "ALL CRITERIA MET"
            elif len(matches) >= 1:
                status = "MOST CRITERIA MET"
            else:
                status = "XXX CRITERIA NOT MET"

            item_text = f"{rhu['name']}\n{status}"
            if not matches:
                item_text += "\nNo accessibility support"

            self.results_list.addItem(item_text)

    def save_allocation(self):
        selected = [rhu['name'] for cb, rhu in self.checkbox_widgets if cb.isChecked()]
        if selected:
            self.licensee['status'] = 'Allocated'
            self.licensee['current_rhu'] = selected[0]
            QMessageBox.information(self, "Saved", f"Allocated to {selected[0]}")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Please select an RHU")


# ---------------- DASH CLASS ----------------

class Dashboard_window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Prison Housing Allocation System")
        self.resize(800, 600)

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

        self.fetch_data()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        label = QLabel("Licensees")
        label.setAlignment(Qt.AlignCenter)

        self.list_widget = QListWidget()

        for i, person in enumerate(self.all_data):
            item = QListWidgetItem()
            item_widget = QWidget()

            if person["status"] != "Pending":
                continue

            name_label = QLabel(person["name"])

            view_button = QPushButton("View")
            view_button.setObjectName(str(i))
            view_button.clicked.connect(self.open_dialog)

            allocate_button = QPushButton("Allocate")
            allocate_button.setObjectName(str(i))
            allocate_button.clicked.connect(self.open_allocation)

            row_layout = QHBoxLayout()
            row_layout.addWidget(name_label)
            row_layout.addStretch()
            row_layout.addWidget(view_button)
            row_layout.addWidget(allocate_button)
            row_layout.setContentsMargins(5, 5, 5, 5)

            item_widget.setLayout(row_layout)
            item.setSizeHint(item_widget.sizeHint())

            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, item_widget)

        main_layout.addWidget(label)
        main_layout.addWidget(self.list_widget)

        main_widget.setLayout(main_layout)
        self.tabs.addTab(main_widget, "Licensees")

    def open_allocation(self):
        button = self.sender()
        index = int(button.objectName())
        person = self.all_data[index]

        dialog = AllocationDialog(person, self.rhu_data, self)
        if dialog.exec():
            self.save_data()
            QMessageBox.information(self, "Success", "Allocation saved")

    def open_dialog(self):
        button = self.sender()
        index = int(button.objectName())
        person = self.all_data[index]

        dialog = QDialog(self)
        dialog.setWindowTitle("Licensee Details")
        dialog.resize(300, 200)

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Name: {person['name']}"))
        layout.addWidget(QLabel(f"Prison Role ID: {person['prison_role_id']}"))

        layout.addStretch()

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec()

    def fetch_data(self):
        try:
            with open("prison_housing_data.json", "r", encoding="utf-8") as f:
                self.all_data = json.load(f)
        except Exception:
            self.all_data = []

        try:
            with open("rhu_data.json", "r", encoding="utf-8") as f:
                self.rhu_data = json.load(f)
        except Exception:
            self.rhu_data = [
                {"name": "Hostel A", "capacity": 30, "provides_curfew": True, "provides_drug_searches": True,
                 "accepts_gender": "Male"},
                {"name": "Durham House", "capacity": 40, "provides_curfew": False, "provides_drug_searches": True,
                 "accepts_gender": "Mixed"},
                {"name": "Safe Haven", "capacity": 20, "provides_curfew": True, "provides_drug_searches": False,
                 "accepts_gender": "Female"}
            ]

    def save_data(self):
        with open("prison_housing_data.json", "w", encoding="utf-8") as f:
            json.dump(self.all_data, f, indent=2)

    def toolbar_button_clicked(self, name):
        print(f"Clicked {name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard_window()
    window.show()
    sys.exit(app.exec())