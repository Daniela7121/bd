from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog,
    QComboBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class HospitalsModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Gestión de Hospitales")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Barra de herramientas
        tool_frame = QFrame()
        tool_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        tool_layout = QHBoxLayout()
        
        self.hospital_search = QLineEdit()
        self.hospital_search.setPlaceholderText("Buscar hospitales...")
        self.hospital_search.setStyleSheet("padding: 8px; border: 1px solid #DDE1E7; border-radius: 6px;")
        
        self.hospital_filter = QComboBox()
        self.hospital_filter.addItems(["Todos", "Activos", "Inactivos", "Por ciudad"])
        self.hospital_filter.setStyleSheet("padding: 8px;")
        
        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        search_btn.clicked.connect(self.filter_hospitals)
        
        tool_layout.addWidget(self.hospital_search)
        tool_layout.addWidget(self.hospital_filter)
        tool_layout.addWidget(search_btn)
        tool_frame.setLayout(tool_layout)
        layout.addWidget(tool_frame)

        self.hospital_table = QTableWidget(0, 6)
        self.hospital_table.setHorizontalHeaderLabels(["ID", "Nombre", "Dirección", "Ciudad", "Teléfono", "Estado"])
        self.hospital_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #27AE60;
                color: white;
                font-weight: bold;
                height: 30px;
                padding-left: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.hospital_table.horizontalHeader().setStretchLastSection(True)
        self.hospital_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.hospital_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.hospital_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.hospital_table)

        btn_layout = QHBoxLayout()
        actions = [
            ("Agregar Hospital", self.add_hospital),
            ("Editar Hospital", self.edit_hospital),
            ("Activar/Desactivar", self.toggle_hospital_status),
            ("Exportar a CSV", self.export_hospitals)
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
            ["1", "Hospital Central", "Av. Principal 123", "Ciudad Capital", "555-1000", "Activo"],
            ["2", "Clínica Norte", "Calle Secundaria 456", "Ciudad Norte", "555-2000", "Activo"],
            ["3", "Hospital Sur", "Boulevard Este 789", "Ciudad Sur", "555-3000", "Inactivo"],
            ["4", "Centro Médico Oriental", "Diagonal Oeste 321", "Ciudad Este", "555-4000", "Activo"],
            ["5", "Hospital Pediátrico", "Av. Los Niños 654", "Ciudad Capital", "555-5000", "Activo"],
        ]
        
        self.hospital_table.setRowCount(0)
        for hospital in sample_data:
            row = self.hospital_table.rowCount()
            self.hospital_table.insertRow(row)
            for col, data in enumerate(hospital):
                item = QTableWidgetItem(data)
                if col == 5:  # Columna de estado
                    item.setForeground(QColor(39, 174, 96)) if data == "Activo" else item.setForeground(QColor(192, 57, 43))
                self.hospital_table.setItem(row, col, item)

    def filter_hospitals(self):
        search_text = self.hospital_search.text().lower()
        filter_type = self.hospital_filter.currentText()
        
        for row in range(self.hospital_table.rowCount()):
            match = True
            name = self.hospital_table.item(row, 1).text().lower()
            city = self.hospital_table.item(row, 3).text()
            status = self.hospital_table.item(row, 5).text()
            
            if search_text and search_text not in name:
                match = False
            if filter_type == "Activos" and status != "Activo":
                match = False
            if filter_type == "Inactivos" and status != "Inactivo":
                match = False
            if filter_type == "Por ciudad" and city.lower() != search_text:
                match = False
                
            self.hospital_table.setRowHidden(row, not match)

    def add_hospital(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Hospital")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit()),
            ("Dirección:", QLineEdit()),
            ("Ciudad:", QLineEdit()),
            ("Teléfono:", QLineEdit()),
        ]
        
        for label_text, input_field in fields:
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(80)
            h_layout.addWidget(label)
            h_layout.addWidget(input_field)
            layout.addLayout(h_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            datos = [field[1].text() for field in fields]
            
            if all(datos):
                row = self.hospital_table.rowCount()
                self.hospital_table.insertRow(row)
                self.hospital_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                for col, dato in enumerate(datos, start=1):
                    self.hospital_table.setItem(row, col, QTableWidgetItem(dato))
                self.hospital_table.setItem(row, 5, QTableWidgetItem("Activo"))
                self.hospital_table.item(row, 5).setForeground(QColor(39, 174, 96))
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def edit_hospital(self):
        selected_row = self.hospital_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Editar", "Seleccione un hospital primero.")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Hospital")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit(self.hospital_table.item(selected_row, 1).text())),
            ("Dirección:", QLineEdit(self.hospital_table.item(selected_row, 2).text())),
            ("Ciudad:", QLineEdit(self.hospital_table.item(selected_row, 3).text())),
            ("Teléfono:", QLineEdit(self.hospital_table.item(selected_row, 4).text())),
        ]
        
        for label_text, input_field in fields:
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(80)
            h_layout.addWidget(label)
            h_layout.addWidget(input_field)
            layout.addLayout(h_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            for col, field in enumerate(fields, start=1):
                self.hospital_table.setItem(selected_row, col, QTableWidgetItem(field[1].text()))

    def toggle_hospital_status(self):
        selected_row = self.hospital_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Estado", "Seleccione un hospital primero.")
            return
            
        current_status = self.hospital_table.item(selected_row, 5).text()
        new_status = "Inactivo" if current_status == "Activo" else "Activo"
        
        self.hospital_table.setItem(selected_row, 5, QTableWidgetItem(new_status))
        self.hospital_table.item(selected_row, 5).setForeground(
            QColor(39, 174, 96) if new_status == "Activo" else QColor(192, 57, 43))

    def export_hospitals(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Exportar Hospitales", 
                                                 "hospitales.csv", 
                                                 "CSV Files (*.csv)", 
                                                 options=options)
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    headers = []
                    for col in range(self.hospital_table.columnCount()):
                        headers.append(self.hospital_table.horizontalHeaderItem(col).text())
                    f.write(','.join(headers) + '\n')
                    
                    for row in range(self.hospital_table.rowCount()):
                        if not self.hospital_table.isRowHidden(row):
                            row_data = []
                            for col in range(self.hospital_table.columnCount()):
                                item = self.hospital_table.item(row, col)
                                row_data.append(item.text() if item else "")
                            f.write(','.join(row_data) + '\n')
                
                QMessageBox.information(self, "Éxito", f"Hospitales exportados a:\n{file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar:\n{str(e)}")