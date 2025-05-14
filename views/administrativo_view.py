from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QStackedWidget, QHBoxLayout, QFrame, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt

class AdministrativoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel de Administrativo")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background-color: #ECF0F1;")
        self.menu_items = [
            "Panel Principal", "Hospitales", "Doctores", 
            "Pacientes", "Consultorios", "Laboratorios", 
            "Citas", "Farmacia", "Facturacion", "Cerrar Sesión"
        ]
        self.init_ui()
        
    def init_ui(self):
        self.menu = QListWidget()
        self.menu.setFixedWidth(220)
        self.menu.setStyleSheet("""
            QListWidget {
                background-color: #2C3E50;
                color: white;
                border: none;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #34495E;
            }
            QListWidget::item:selected {
                background-color: #3498DB;
                font-weight: bold;
            }
        """)
        
        icons = {
            "Panel Principal": "dashboard",
            "Hospitales": "hospital",
            "Doctores": "doctor",
            "Pacientes": "patient",
            "Consultorios": "office",
            "Laboratorios": "lab",
            "Citas": "calendar",
            "Farmacia": "pharmacy",
            "Facturacion": "billing",
            "Cerrar Sesión": "logout"
        }
        
        for item in self.menu_items:
            icon_name = icons.get(item, "folder")
            list_item = QListWidgetItem(QIcon.fromTheme(icon_name), item)
            self.menu.addItem(list_item)
        
        self.menu.currentRowChanged.connect(self.display_view)

        self.stack = QStackedWidget(self)
        
        # Import modules here to avoid circular imports
        from modules.dashboard_module import DashboardModule
        from modules.hospitals_module import HospitalsModule
        from modules.doctors_module import DoctorsModule
        from modules.patients_module import PatientsModule
        from modules.offices_module import OfficesModule
        from modules.labs_module import LabsModule
        from modules.appointments_module import AppointmentsModule
        from modules.pharmacy_module import PharmacyModule
        from modules.billing_module import BillingModule
        
        # Add widgets in the same order as menu_items
        self.stack.addWidget(DashboardModule())
        self.stack.addWidget(HospitalsModule())
        self.stack.addWidget(DoctorsModule())
        self.stack.addWidget(PatientsModule())
        self.stack.addWidget(OfficesModule())
        self.stack.addWidget(LabsModule())
        self.stack.addWidget(AppointmentsModule())
        self.stack.addWidget(PharmacyModule())
        self.stack.addWidget(BillingModule())
        # Empty widget for logout (not really needed)
        self.stack.addWidget(QWidget())  

        layout = QHBoxLayout()
        layout.addWidget(self.menu)
        layout.addWidget(self.stack)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def display_view(self, index):
        if index == len(self.menu_items) - 1:  # Last item is "Cerrar Sesión"
            reply = QMessageBox.question(
                self, 
                'Cerrar Sesión', 
                '¿Está seguro que desea cerrar sesión?',
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.close()
                # Import here to avoid circular imports
                from views.login_view import LoginWindow
                self.login_window = LoginWindow()
                self.login_window.show()
        else:
            if index < self.stack.count():  # Safety check
                self.stack.setCurrentIndex(index)