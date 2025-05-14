from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog,
    QComboBox, QInputDialog
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class DoctorsModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Gestión de Doctores")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        tool_frame = QFrame()
        tool_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        tool_layout = QHBoxLayout()
        
        self.doctor_search = QLineEdit()
        self.doctor_search.setPlaceholderText("Buscar doctores...")
        self.doctor_search.setStyleSheet("padding: 8px; border: 1px solid #DDE1E7; border-radius: 6px;")
        
        self.doctor_filter = QComboBox()
        self.doctor_filter.addItems(["Todos", "Activos", "Inactivos", "Por especialidad"])
        self.doctor_filter.setStyleSheet("padding: 8px;")
        
        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #9B59B6;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8E44AD;
            }
        """)
        search_btn.clicked.connect(self.filter_doctors)
        
        tool_layout.addWidget(self.doctor_search)
        tool_layout.addWidget(self.doctor_filter)
        tool_layout.addWidget(search_btn)
        tool_frame.setLayout(tool_layout)
        layout.addWidget(tool_frame)

        self.doctor_table = QTableWidget(0, 6)
        self.doctor_table.setHorizontalHeaderLabels(["ID", "Nombre", "Especialidad", "Teléfono", "Email", "Estado"])
        self.doctor_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #9B59B6;
                color: white;
                font-weight: bold;
                height: 30px;
                padding-left: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.doctor_table.horizontalHeader().setStretchLastSection(True)
        self.doctor_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.doctor_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.doctor_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.doctor_table)

        btn_layout = QHBoxLayout()
        actions = [
            ("Agregar Doctor", self.add_doctor),
            ("Editar Doctor", self.edit_doctor),
            ("Cambiar Estado", self.toggle_doctor_status),
            ("Exportar a CSV", self.export_doctors)
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
            ["1", "Dr. Carlos García", "Cardiología", "555-1001", "cgarcia@clinica.com", "Activo"],
            ["2", "Dra. Ana López", "Pediatría", "555-1002", "alopez@clinica.com", "Activo"],
            ["3", "Dr. Luis Martínez", "Neurología", "555-1003", "lmartinez@clinica.com", "Inactivo"],
            ["4", "Dra. Sofía Ramírez", "Dermatología", "555-1004", "sramirez@clinica.com", "Activo"]
        ]
        
        self.doctor_table.setRowCount(0)
        for doctor in sample_data:
            row = self.doctor_table.rowCount()
            self.doctor_table.insertRow(row)
            for col, data in enumerate(doctor):
                item = QTableWidgetItem(data)
                if col == 5:  # Columna de estado
                    item.setForeground(QColor(39, 174, 96)) if data == "Activo" else item.setForeground(QColor(192, 57, 43))
                self.doctor_table.setItem(row, col, item)

    def filter_doctors(self):
        search_text = self.doctor_search.text().lower()
        filter_type = self.doctor_filter.currentText()
        
        for row in range(self.doctor_table.rowCount()):
            match = True
            name = self.doctor_table.item(row, 1).text().lower()
            specialty = self.doctor_table.item(row, 2).text()
            status = self.doctor_table.item(row, 5).text()
            
            if search_text and search_text not in name:
                match = False
            if filter_type == "Activos" and status != "Activo":
                match = False
            if filter_type == "Inactivos" and status != "Inactivo":
                match = False
            if filter_type == "Por especialidad" and specialty.lower() != search_text:
                match = False
                
            self.doctor_table.setRowHidden(row, not match)

    def add_doctor(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Doctor")
        dialog.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit()),
            ("Especialidad:", QComboBox()),
            ("Teléfono:", QLineEdit()),
            ("Email:", QLineEdit()),
        ]
        
        fields[1][1].addItems(["Cardiología", "Pediatría", "Neurología", "Dermatología", "Cirugía", "Medicina General"])
        
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
                row = self.doctor_table.rowCount()
                self.doctor_table.insertRow(row)
                self.doctor_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                for col, dato in enumerate(datos, start=1):
                    self.doctor_table.setItem(row, col, QTableWidgetItem(dato))
                self.doctor_table.setItem(row, 5, QTableWidgetItem("Activo"))
                self.doctor_table.item(row, 5).setForeground(QColor(39, 174, 96))
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def edit_doctor(self):
        selected_row = self.doctor_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un doctor para editar.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Doctor")
        dialog.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit(self.doctor_table.item(selected_row, 1).text())),
            ("Especialidad:", QComboBox()),
            ("Teléfono:", QLineEdit(self.doctor_table.item(selected_row, 3).text())),
            ("Email:", QLineEdit(self.doctor_table.item(selected_row, 4).text())),
        ]
        
        fields[1][1].addItems(["Cardiología", "Pediatría", "Neurología", "Dermatología", "Cirugía", "Medicina General"])
        fields[1][1].setCurrentText(self.doctor_table.item(selected_row, 2).text())
        
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
                    self.doctor_table.setItem(selected_row, col, QTableWidgetItem(dato))
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def toggle_doctor_status(self):
        selected_row = self.doctor_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un doctor para cambiar su estado.")
            return

        current_status = self.doctor_table.item(selected_row, 5).text()
        new_status = "Inactivo" if current_status == "Activo" else "Activo"
        
        reply = QMessageBox.question(
            self, 
            "Confirmar", 
            f"¿Está seguro que desea cambiar el estado del doctor a {new_status}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.doctor_table.setItem(selected_row, 5, QTableWidgetItem(new_status))
            color = QColor(39, 174, 96) if new_status == "Activo" else QColor(192, 57, 43)
            self.doctor_table.item(selected_row, 5).setForeground(color)

    def export_doctors(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "Exportar Doctores a CSV", 
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
                for col in range(self.doctor_table.columnCount()):
                    headers.append(self.doctor_table.horizontalHeaderItem(col).text())
                f.write(",".join(headers) + "\n")
                
                # Escribir datos
                for row in range(self.doctor_table.rowCount()):
                    row_data = []
                    for col in range(self.doctor_table.columnCount()):
                        item = self.doctor_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    f.write(",".join(row_data) + "\n")
                    
            QMessageBox.information(self, "Éxito", "Los datos se exportaron correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el archivo:\n{str(e)}")