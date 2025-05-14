from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog,
    QComboBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class UsersModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Gestión de Usuarios")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Barra de herramientas
        tool_frame = QFrame()
        tool_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        tool_layout = QHBoxLayout()
        
        self.user_search = QLineEdit()
        self.user_search.setPlaceholderText("Buscar usuarios...")
        self.user_search.setStyleSheet("padding: 8px; border: 1px solid #DDE1E7; border-radius: 6px;")
        
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
        search_btn.clicked.connect(self.filter_users)
        
        tool_layout.addWidget(self.user_search)
        tool_layout.addWidget(search_btn)
        tool_frame.setLayout(tool_layout)
        layout.addWidget(tool_frame)

        self.user_table = QTableWidget(0, 5)
        self.user_table.setHorizontalHeaderLabels(["ID", "Nombre", "Email", "Rol", "Estado"])
        self.user_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #0984E3;
                color: white;
                font-weight: bold;
                height: 30px;
                padding-left: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.user_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.user_table)

        btn_layout = QHBoxLayout()
        actions = [
            ("Agregar Usuario", self.agregar_usuario),
            ("Editar Usuario", self.editar_usuario),
            ("Cambiar Estado", self.toggle_user_status),
            ("Exportar a CSV", self.export_users)
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
        usuarios = [
            ["1", "Ana Pérez", "admin@clinica.com", "Administrador", "Activo"],
            ["2", "Luis Torres", "doctor@clinica.com", "Doctor", "Activo"],
            ["3", "María Gómez", "paciente@clinica.com", "Paciente", "Inactivo"],
            ["4", "Carlos Ruiz", "administ@clinica.com", "Administrativo", "Activo"]
        ]
        self.user_table.setRowCount(0)
        for usuario in usuarios:
            row = self.user_table.rowCount()
            self.user_table.insertRow(row)
            for col, dato in enumerate(usuario):
                item = QTableWidgetItem(dato)
                if col == 4:  # Columna de estado
                    item.setForeground(QColor(39, 174, 96)) if dato == "Activo" else item.setForeground(QColor(192, 57, 43))
                self.user_table.setItem(row, col, item)

    def filter_users(self):
        search_text = self.user_search.text().lower()
        for row in range(self.user_table.rowCount()):
            match = False
            for col in range(self.user_table.columnCount()):
                item = self.user_table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.user_table.setRowHidden(row, not match)

    def agregar_usuario(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Usuario")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit()),
            ("Email:", QLineEdit()),
            ("Rol:", QComboBox()),
            ("Contraseña:", QLineEdit())
        ]
        fields[2][1].addItems(["Administrador", "Doctor", "Paciente", "Administrativo"])
        fields[3][1].setEchoMode(QLineEdit.Password)
        
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
                row = self.user_table.rowCount()
                self.user_table.insertRow(row)
                self.user_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                for col, dato in enumerate(datos[:-1], start=1):  # Excluir contraseña
                    self.user_table.setItem(row, col, QTableWidgetItem(dato))
                self.user_table.setItem(row, 4, QTableWidgetItem("Activo"))
                self.user_table.item(row, 4).setForeground(QColor(39, 174, 96))
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def editar_usuario(self):
        selected_row = self.user_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Editar", "Seleccione un usuario primero.")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Usuario")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit(self.user_table.item(selected_row, 1).text())),
            ("Email:", QLineEdit(self.user_table.item(selected_row, 2).text())),
            ("Rol:", QComboBox()),
        ]
        
        fields[2][1].addItems(["Administrador", "Doctor", "Paciente", "Administrativo"])
        fields[2][1].setCurrentText(self.user_table.item(selected_row, 3).text())
        
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
            for col, field in enumerate(fields, start=1):
                new_value = field[1].text() if not isinstance(field[1], QComboBox) else field[1].currentText()
                self.user_table.setItem(selected_row, col, QTableWidgetItem(new_value))

    def toggle_user_status(self):
        selected_row = self.user_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Estado", "Seleccione un usuario primero.")
            return
            
        current_status = self.user_table.item(selected_row, 4).text()
        new_status = "Inactivo" if current_status == "Activo" else "Activo"
        
        self.user_table.setItem(selected_row, 4, QTableWidgetItem(new_status))
        self.user_table.item(selected_row, 4).setForeground(
            QColor(39, 174, 96) if new_status == "Activo" else QColor(192, 57, 43))

    def export_users(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Exportar Usuarios", 
                                                 "usuarios.csv", 
                                                 "CSV Files (*.csv)", 
                                                 options=options)
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    headers = []
                    for col in range(self.user_table.columnCount()):
                        headers.append(self.user_table.horizontalHeaderItem(col).text())
                    f.write(','.join(headers) + '\n')
                    
                    for row in range(self.user_table.rowCount()):
                        if not self.user_table.isRowHidden(row):
                            row_data = []
                            for col in range(self.user_table.columnCount()):
                                item = self.user_table.item(row, col)
                                row_data.append(item.text() if item else "")
                            f.write(','.join(row_data) + '\n')
                
                QMessageBox.information(self, "Éxito", f"Usuarios exportados a:\n{file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar:\n{str(e)}")