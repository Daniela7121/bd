from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QDialogButtonBox, QHBoxLayout,
    QLineEdit, QTextEdit, QComboBox, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class MedicalHistoryModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.data = []
        self.load_sample_data()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Historial Médico")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID Paciente", "Fecha", "Diagnóstico", "Tratamiento", "Notas"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        btn_add = QPushButton("Agregar Registro Médico")
        btn_add.clicked.connect(self.add_record)
        layout.addWidget(btn_add)

        self.setLayout(layout)

    def load_sample_data(self):
        self.add_row(["1", "2025-01-15", "Gripe", "Paracetamol", "Reposo 3 días"])
        self.add_row(["2", "2025-02-10", "Migraña", "Ibuprofeno", "Evitar pantallas"])

    def add_row(self, data):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, val in enumerate(data):
            self.table.setItem(row, col, QTableWidgetItem(val))

    def add_record(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nuevo Registro Médico")
        layout = QVBoxLayout()

        fields = [
            ("ID Paciente", QLineEdit()),
            ("Fecha", QLineEdit("YYYY-MM-DD")),
            ("Diagnóstico", QLineEdit()),
            ("Tratamiento", QLineEdit()),
            ("Notas", QTextEdit())
        ]

        for label_text, widget in fields:
            row = QHBoxLayout()
            row.addWidget(QLabel(label_text))
            row.addWidget(widget)
            layout.addLayout(row)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            values = [widget.text() if isinstance(widget, QLineEdit) else widget.toPlainText() for _, widget in fields]
            if all(values):
                self.add_row(values)
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
