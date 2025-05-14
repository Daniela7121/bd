from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QMessageBox, QFileDialog, QComboBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class AuditModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Registros de Auditoría")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        filter_frame = QFrame()
        filter_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        filter_layout = QHBoxLayout()
        
        date_filter = QHBoxLayout()
        date_filter.addWidget(QLabel("Desde:"))
        self.audit_date_from = QLineEdit()
        self.audit_date_from.setPlaceholderText("DD/MM/AAAA")
        self.audit_date_from.setStyleSheet("padding: 8px;")
        date_filter.addWidget(self.audit_date_from)
        
        date_filter.addWidget(QLabel("Hasta:"))
        self.audit_date_to = QLineEdit()
        self.audit_date_to.setPlaceholderText("DD/MM/AAAA")
        self.audit_date_to.setStyleSheet("padding: 8px;")
        date_filter.addWidget(self.audit_date_to)
        
        user_filter = QHBoxLayout()
        user_filter.addWidget(QLabel("Usuario:"))
        self.audit_user_filter = QLineEdit()
        self.audit_user_filter.setPlaceholderText("Todos")
        self.audit_user_filter.setStyleSheet("padding: 8px;")
        user_filter.addWidget(self.audit_user_filter)
        
        action_filter = QHBoxLayout()
        action_filter.addWidget(QLabel("Acción:"))
        self.audit_action_filter = QComboBox()
        self.audit_action_filter.addItems(["Todas", "Login", "Logout", "Creación", "Modificación", "Eliminación"])
        self.audit_action_filter.setStyleSheet("padding: 8px;")
        action_filter.addWidget(self.audit_action_filter)
        
        self.audit_search_btn = QPushButton("Buscar")
        self.audit_search_btn.setStyleSheet("""
            QPushButton {
                background-color: #E67E22;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D35400;
            }
        """)
        self.audit_search_btn.clicked.connect(self.filter_audit_logs)
        
        filter_layout.addLayout(date_filter)
        filter_layout.addLayout(user_filter)
        filter_layout.addLayout(action_filter)
        filter_layout.addWidget(self.audit_search_btn)
        filter_frame.setLayout(filter_layout)
        layout.addWidget(filter_frame)

        self.audit_table = QTableWidget(0, 6)
        self.audit_table.setHorizontalHeaderLabels(["Fecha", "Hora", "Usuario", "Acción", "Entidad", "Detalles"])
        self.audit_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #E67E22;
                color: white;
                font-weight: bold;
                height: 30px;
                padding-left: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.audit_table.horizontalHeader().setStretchLastSection(True)
        self.audit_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.audit_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.audit_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.audit_table)

        btn_layout = QHBoxLayout()
        export_btn = QPushButton("Exportar a CSV")
        clear_btn = QPushButton("Limpiar Filtros")
        
        for btn in [export_btn, clear_btn]:
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
        
        export_btn.clicked.connect(self.export_audit_logs)
        clear_btn.clicked.connect(self.clear_audit_filters)
        btn_layout.addWidget(export_btn)
        btn_layout.addWidget(clear_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_sample_data(self):
        sample_data = [
            ["15/05/2023", "09:23:45", "admin@clinica.com", "Login", "Sistema", "Inicio de sesión exitoso"],
            ["15/05/2023", "09:30:12", "admin@clinica.com", "Creación", "Usuario", "Creó usuario doctor@clinica.com"],
            ["15/05/2023", "10:15:33", "doctor@clinica.com", "Login", "Sistema", "Inicio de sesión exitoso"],
            ["15/05/2023", "11:42:18", "admin@clinica.com", "Modificación", "Hospital", "Actualizó datos del hospital central"],
            ["15/05/2023", "12:05:56", "paciente@clinica.com", "Login", "Sistema", "Inicio de sesión fallido"],
            ["15/05/2023", "14:30:00", "admin@clinica.com", "Eliminación", "Usuario", "Eliminó usuario temporal@clinica.com"],
            ["15/05/2023", "16:45:22", "doctor@clinica.com", "Logout", "Sistema", "Cierre de sesión"],
        ]
        
        self.audit_table.setRowCount(0)
        for log in sample_data:
            row = self.audit_table.rowCount()
            self.audit_table.insertRow(row)
            for col, data in enumerate(log):
                item = QTableWidgetItem(data)
                if col == 3:  # Columna de acción
                    if data == "Login":
                        item.setForeground(QColor(41, 128, 185))
                    elif data == "Logout":
                        item.setForeground(QColor(142, 68, 173))
                    elif data in ["Creación", "Modificación"]:
                        item.setForeground(QColor(39, 174, 96))
                    elif data == "Eliminación":
                        item.setForeground(QColor(192, 57, 43))
                self.audit_table.setItem(row, col, item)

    def filter_audit_logs(self):
        date_from = self.audit_date_from.text()
        date_to = self.audit_date_to.text()
        user_filter = self.audit_user_filter.text().lower()
        action_filter = self.audit_action_filter.currentText()
        
        for row in range(self.audit_table.rowCount()):
            match = True
            date = self.audit_table.item(row, 0).text()
            user = self.audit_table.item(row, 2).text().lower()
            action = self.audit_table.item(row, 3).text()
            
            if date_from and date < date_from:
                match = False
            if date_to and date > date_to:
                match = False
            if user_filter and user_filter not in user:
                match = False
            if action_filter != "Todas" and action_filter != action:
                match = False
                
            self.audit_table.setRowHidden(row, not match)

    def clear_audit_filters(self):
        self.audit_date_from.clear()
        self.audit_date_to.clear()
        self.audit_user_filter.clear()
        self.audit_action_filter.setCurrentIndex(0)
        
        for row in range(self.audit_table.rowCount()):
            self.audit_table.setRowHidden(row, False)

    def export_audit_logs(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Exportar Auditoría", 
                                                 "auditoria.csv", 
                                                 "CSV Files (*.csv)", 
                                                 options=options)
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    headers = []
                    for col in range(self.audit_table.columnCount()):
                        headers.append(self.audit_table.horizontalHeaderItem(col).text())
                    f.write(','.join(headers) + '\n')
                    
                    for row in range(self.audit_table.rowCount()):
                        if not self.audit_table.isRowHidden(row):
                            row_data = []
                            for col in range(self.audit_table.columnCount()):
                                item = self.audit_table.item(row, col)
                                row_data.append(item.text() if item else "")
                            f.write(','.join(row_data) + '\n')
                
                QMessageBox.information(self, "Éxito", f"Auditoría exportada a:\n{file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar:\n{str(e)}")