import json
import sys
import random

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QMessageBox, QInputDialog, QDialog, QDialogButtonBox, QToolBar, QTabWidget, QListView,
                               QDateEdit)
from PySide6.QtWidgets import (
    QPushButton, QVBoxLayout,
    QWidget, QTextEdit, QHBoxLayout,
    QLineEdit, QLabel, QFontDialog, QComboBox, QFormLayout)
from PySide6.QtCore import Qt, QStringListModel, QDate


class CreateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Licensee")
        self.resize(400, 300)

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.prison_id_input = QLineEdit()
        self.prison_id_input.setText(f"PR{random.randint(100000, 999999)}")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female"])
        self.category_combo = QComboBox()
        self.category_combo.addItems(["A", "B", "C", "D"])
        #self.release_date_input = QDateEdit()
        #self.release_date_input.setDate(QDate.currentDate())

        layout.addRow("Name:", self.name_input)
        layout.addRow("Prison ID:", self.prison_id_input)
        layout.addRow("Gender:", self.gender_combo)
        layout.addRow("Category:", self.category_combo)
        #layout.addRow("Release Date:", self.release_date_input)


        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    # ---------------- DEFAULT DATA  ----------------
    def get_data(self):
        return {
            "name": self.name_input.text(),
            "prison_role_id": self.prison_id_input.text(),
            "gender": self.gender_combo.currentText(),
            "category": self.category_combo.currentText(),
            "release_date": "2026-06-01",
            "end_of_licence": "2027-06-01",
            "current_location": "HMP Durham",
            "home_address": "Unknown",
            "photo": None,
            "security_category": self.category_combo.currentText(),
            "night_curfew": False,
            "weekend_curfew": False,
            "victim_exclusion_zones": [],
            "school_exclusion_distance_m": 0,
            "excluded_prisoners": "None",
            "disability": "None",
            "accessibility_needs": False,
            "general_exclusion_zone": "None",
            "drug_search_required": False,
            "associate_restrictions": "None",
            "young_offender_suitable": False,
            "medical_access_needed": "None",
            "transport_links_needed": [],
            "religious_needs": "None",
            "mental_health_needs": "None",
            "family_access_location": "Unknown",
            "prior_rhu_experience": "None",
            "employment_or_training": "None",
            "offending_triggers": "None",
            "licence_period_days": 365,
            "future_expansion_1": "None",
            "future_expansion_2": 0,
            "future_expansion_3": "N/A",
            "pet_therapy": "No",
            "support_level": "Medium",
            "notes": "Newly created",
            "status": "Pending",
            "current_rhu": None,
            "days_until_housing": 30,
            "days_until_exit": None
        }


class Dashboard_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prison Housing Allocation System")
        self.resize(800, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        # ---------------- TOOLBAR  ----------------

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

        pending_widget = QWidget()
        pending_layout = QVBoxLayout()

        label = QLabel("Pending Licensees")
        label.setAlignment(Qt.AlignCenter)

        btn_row = QHBoxLayout()
        create_btn = QPushButton("Create New")
        create_btn.clicked.connect(self.create_new)
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_person)
        btn_row.addWidget(create_btn)
        btn_row.addWidget(delete_btn)
        btn_row.addStretch()

        self.pending_list = QListView()

        self.fetch_data()
        self.data = self.all_data

        pending_display = []
        for i in self.data:
            if i["status"] == "Pending":
                days = i.get("days_until_housing")
                pending_display.append(f'{i["name"]} - {days} days left')

        self.pending_model = QStringListModel(pending_display)
        self.pending_list.setModel(self.pending_model)

        pending_layout.addWidget(label)
        pending_layout.addLayout(btn_row)
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

    def save_data(self):
        with open('prison_housing_data.json', 'w', encoding='utf-8') as f:
            json.dump(self.all_data, f, indent=4)

    def create_new(self):
        dialog = CreateDialog(self)
        if dialog.exec():
            new_person = dialog.get_data()
            self.all_data.append(new_person)
            self.save_data()
            self.update_lists()

    def delete_person(self):
        index = self.pending_list.currentIndex()
        if index.isValid():
            row = index.row()
            pending_items = [p for p in self.all_data if p["status"] == "Pending"]
            if row < len(pending_items):
                person = pending_items[row]
                reply = QMessageBox.question(self, "Delete", f"Delete {person['name']}?")
                if reply == QMessageBox.Yes:
                    self.all_data.remove(person)
                    self.save_data()
                    self.update_lists()
        else:
            QMessageBox.warning(self, "Error", "Select someone")

    def update_lists(self):
        pending_display = []
        for i in self.all_data:
            if i["status"] == "Pending":
                days = i.get("days_until_housing")
                pending_display.append(f'{i["name"]} - {days} days left')
        self.pending_model.setStringList(pending_display)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard_window()
    window.show()
    sys.exit(app.exec())