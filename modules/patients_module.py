from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog,
    QComboBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class PatientsModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Gestión de Pacientes")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        tool_frame = QFrame()
        tool_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        tool_layout = QHBoxLayout()
        
        self.patient_search = QLineEdit()
        self.patient_search.setPlaceholderText("Buscar pacientes...")
        self.patient_search.setStyleSheet("padding: 8px; border: 1px solid #DDE1E7; border-radius: 6px;")
        
        self.patient_filter = QComboBox()
        self.patient_filter.addItems(["Todos", "Activos", "Inactivos", "Por género"])
        self.patient_filter.setStyleSheet("padding: 8px;")
        
        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        search_btn.clicked.connect(self.filter_patients)
        
        tool_layout.addWidget(self.patient_search)
        tool_layout.addWidget(self.patient_filter)
        tool_layout.addWidget(search_btn)
        tool_frame.setLayout(tool_layout)
        layout.addWidget(tool_frame)

        self.patient_table = QTableWidget(0, 7)
        self.patient_table.setHorizontalHeaderLabels(["ID", "Nombre", "Edad", "Género", "Email", "Teléfono", "Estado"])
        self.patient_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #3498DB;
                color: white;
                font-weight: bold;
                height: 30px;
                padding-left: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.patient_table.horizontalHeader().setStretchLastSection(True)
        self.patient_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.patient_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.patient_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.patient_table)

        btn_layout = QHBoxLayout()
        actions = [
            ("Agregar Paciente", self.add_patient),
            ("Editar Paciente", self.edit_patient),
            ("Cambiar Estado", self.toggle_patient_status),
            ("Exportar a CSV", self.export_patients)
        ]
        
        for text, handler in actions:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2C3E50;
                    color: white;
                    padding: 10px 15px;
                    border-radius: 8px;
                    font-weight: bold;
                    margin-right: 10px;
                }
                QPushButton:hover {
                    background-color: #34495E;
                }
            """)
            btn.clicked.connect(handler)
            btn_layout.addWidget(btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_sample_data(self):
        sample_data = [
            ["1", "Juan Pérez", "25", "M", "juan@email.com", "555-2001", "Activo"],
            ["2", "María Gómez", "32", "F", "maria@email.com", "555-2002", "Activo"],
            ["3", "Carlos Ruiz", "45", "M", "carlos@email.com", "555-2003", "Activo"],
            ["4", "Ana Torres", "28", "F", "ana@email.com", "555-2004", "Inactivo"]
        ]
        
        self.patient_table.setRowCount(0)
        for patient in sample_data:
            row = self.patient_table.rowCount()
            self.patient_table.insertRow(row)
            for col, data in enumerate(patient):
                item = QTableWidgetItem(data)
                if col == 6:  # Columna de estado
                    item.setForeground(QColor(39, 174, 96)) if data == "Activo" else item.setForeground(QColor(192, 57, 43))
                self.patient_table.setItem(row, col, item)

    def filter_patients(self):
        search_text = self.patient_search.text().lower()
        filter_type = self.patient_filter.currentText()
        
        for row in range(self.patient_table.rowCount()):
            match = True
            name = self.patient_table.item(row, 1).text().lower()
            gender = self.patient_table.item(row, 3).text()
            status = self.patient_table.item(row, 6).text()
            
            if search_text and search_text not in name:
                match = False
            if filter_type == "Activos" and status != "Activo":
                match = False
            if filter_type == "Inactivos" and status != "Inactivo":
                match = False
            if filter_type == "Por género" and gender.lower() != search_text:
                match = False
                
            self.patient_table.setRowHidden(row, not match)

    def add_patient(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Paciente")
        dialog.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit()),
            ("Edad:", QLineEdit()),
            ("Género:", QComboBox()),
            ("Email:", QLineEdit()),
            ("Teléfono:", QLineEdit()),
        ]
        
        fields[2][1].addItems(["M", "F", "Otro"])
        
        for label_text, input_field in fields:
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(100)
            h_layout.addWidget(label)
            h_layout.addWidget(input_field)
            layout.addLayout(h_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            datos = [field[1].text() if not isinstance(field[1], QComboBox) else field[1].currentText() 
                    for field in fields]
            
            if all(datos):
                row = self.patient_table.rowCount()
                self.patient_table.insertRow(row)
                self.patient_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                for col, dato in enumerate(datos, start=1):
                    self.patient_table.setItem(row, col, QTableWidgetItem(dato))
                self.patient_table.setItem(row, 6, QTableWidgetItem("Activo"))
                self.patient_table.item(row, 6).setForeground(QColor(39, 174, 96))
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def edit_patient(self):
        selected_row = self.patient_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un paciente para editar.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Paciente")
        dialog.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit(self.patient_table.item(selected_row, 1).text())),
            ("Edad:", QLineEdit(self.patient_table.item(selected_row, 2).text())),
            ("Género:", QComboBox()),
            ("Email:", QLineEdit(self.patient_table.item(selected_row, 4).text())),
            ("Teléfono:", QLineEdit(self.patient_table.item(selected_row, 5).text())),
        ]
        
        fields[2][1].addItems(["M", "F", "Otro"])
        fields[2][1].setCurrentText(self.patient_table.item(selected_row, 3).text())
        
        for label_text, input_field in fields:
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(100)
            h_layout.addWidget(label)
            h_layout.addWidget(input_field)
            layout.addLayout(h_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            datos = [field[1].text() if not isinstance(field[1], QComboBox) else field[1].currentText() 
                    for field in fields]
            
            if all(datos):
                for col, dato in enumerate(datos, start=1):
                    if col != 6:  # No actualizamos el estado al editar
                        self.patient_table.setItem(selected_row, col, QTableWidgetItem(dato))
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def toggle_patient_status(self):
        selected_row = self.patient_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un paciente para cambiar su estado.")
            return

        current_status = self.patient_table.item(selected_row, 6).text()
        new_status = "Inactivo" if current_status == "Activo" else "Activo"
        
        reply = QMessageBox.question(
            self, 
            "Confirmar", 
            f"¿Está seguro que desea cambiar el estado del paciente a {new_status}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.patient_table.setItem(selected_row, 6, QTableWidgetItem(new_status))
            color = QColor(39, 174, 96) if new_status == "Activo" else QColor(192, 57, 43)
            self.patient_table.item(selected_row, 6).setForeground(color)

    def export_patients(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "Exportar Pacientes a CSV", 
            "", 
            "CSV Files (*.csv)", 
            options=options
        )
        
        if not file_name:
            return
            
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                # Escribir encabezados
                headers = []
                for col in range(self.patient_table.columnCount()):
                    headers.append(self.patient_table.horizontalHeaderItem(col).text())
                f.write(",".join(headers) + "\n")
                
                # Escribir datos
                for row in range(self.patient_table.rowCount()):
                    row_data = []
                    for col in range(self.patient_table.columnCount()):
                        item = self.patient_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    f.write(",".join(row_data) + "\n")
                    
            QMessageBox.information(self, "Éxito", "Los datos se exportaron correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el archivo:\n{str(e)}")