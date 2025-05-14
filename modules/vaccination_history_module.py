from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QDialogButtonBox, QHBoxLayout,
    QLineEdit, QComboBox, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class VaccinationHistoryModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_data()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Historial de Vacunación")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID Paciente", "Vacuna", "Fecha Aplicación", "Dosis", "Observaciones"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        btn_add = QPushButton("Agregar Vacunación")
        btn_add.clicked.connect(self.add_record)
        layout.addWidget(btn_add)

        self.setLayout(layout)

    def load_sample_data(self):
        self.add_row(["1", "COVID-19", "2024-03-10", "2da", "Sin reacciones"])
        self.add_row(["2", "Influenza", "2024-11-01", "Única", "Ligera fiebre"])

    def add_row(self, data):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, val in enumerate(data):
            self.table.setItem(row, col, QTableWidgetItem(val))

    def add_record(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nueva Vacunación")
        layout = QVBoxLayout()

        fields = [
            ("ID Paciente", QLineEdit()),
            ("Vacuna", QLineEdit()),
            ("Fecha Aplicación", QLineEdit("YYYY-MM-DD")),
            ("Dosis", QComboBox()),
            ("Observaciones", QLineEdit())
        ]
        fields[3][1].addItems(["Única", "1ra", "2da", "Refuerzo"])

        for label_text, widget in fields:
            row = QHBoxLayout()
            row.addWidget(QLabel(label_text))
            row.addWidget(widget)
            layout.addLayout(row)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            values = [
                widget.text() if isinstance(widget, QLineEdit) else widget.currentText()
                for _, widget in fields
            ]
            if all(values):
                self.add_row(values)
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
