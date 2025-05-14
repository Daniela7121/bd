from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox, QCheckBox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from controllers.auth_controller import autenticar_usuario
from views.admin_view import AdminWindow
from views.doctor_view import DoctorWindow
from views.paciente_view import PacienteWindow
from views.administrativo_view import AdministrativoWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión - Clínica")
        self.setMinimumSize(400, 500) 
        self.center_window()
        
       
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: 'Arial';
            }
            QLabel {
                font-size: 14px;
                color: #7f8c8d;
                margin-bottom: 5px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #bdc3c7;
                margin-bottom: 15px;
                min-width: 250px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
                border: none;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1a6a9c;
            }
            QCheckBox {
                font-size: 13px;
                color: #7f8c8d;
            }
            #logoContainer {
                margin-bottom: 30px;
            }
        """)

        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(20)
        layout_principal.setAlignment(Qt.AlignCenter)

       
        logo_container = QWidget()
        logo_container.setObjectName("logoContainer")
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        
        self.logo = QLabel()
        try:
            pixmap = QPixmap(r'C:\Users\USER\Desktop\bd\img/logo.png')
            self.logo.setPixmap(pixmap.scaledToWidth(300, Qt.SmoothTransformation))
        except:
            self.logo.setText("Logo de la Clínica")
            self.logo.setFont(QFont('Arial', 18, QFont.Bold))
        
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        logo_layout.addWidget(self.logo)
        layout_principal.addWidget(logo_container)

        
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
       
        self.label_usuario = QLabel("Usuario")
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Ingrese su nombre de usuario")
        self.input_usuario.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
       
        self.label_contrasena = QLabel("Contraseña")
        self.input_contrasena = QLineEdit()
        self.input_contrasena.setPlaceholderText("Ingrese su contraseña")
        self.input_contrasena.setEchoMode(QLineEdit.Password)
        self.input_contrasena.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        form_layout.addWidget(self.label_usuario)
        form_layout.addWidget(self.input_usuario)
        form_layout.addWidget(self.label_contrasena)
        form_layout.addWidget(self.input_contrasena)

        
        self.check_remember = QCheckBox("Recordar mi usuario")
        form_layout.addWidget(self.check_remember, alignment=Qt.AlignLeft)
        
        layout_principal.addWidget(form_container)

        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(15)

     
        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.clicked.connect(self.login)
        self.btn_login.setDefault(True)
        self.btn_login.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
      
        self.btn_eliminar = QPushButton("Cerrar")
        self.btn_eliminar.setStyleSheet("background-color: #e74c3c; color: white;")
        self.btn_eliminar.clicked.connect(self.close)
        self.btn_eliminar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        buttons_layout.addWidget(self.btn_login)
        buttons_layout.addWidget(self.btn_eliminar)
        layout_principal.addWidget(buttons_container)

        
        layout_principal.addStretch()

        self.setLayout(layout_principal)

    def center_window(self):
        frame = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())

    def resizeEvent(self, event):
        
        if hasattr(self, 'logo') and isinstance(self.logo.pixmap(), QPixmap):
            new_width = min(self.width() - 80, 400)  # Máximo 400px de ancho
            self.logo.setPixmap(self.logo.pixmap().scaledToWidth(new_width, Qt.SmoothTransformation))
        super().resizeEvent(event)

    def login(self):
        nombre = self.input_usuario.text()
        contrasena = self.input_contrasena.text()

        usuario = autenticar_usuario(nombre, contrasena)
        if usuario:
            QMessageBox.information(self, "Éxito", f"Bienvenido, {usuario['nombre']} ({usuario['rol']})")
            self.open_role_view(usuario['rol'])
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Nombre o contraseña incorrectos.")

    def open_role_view(self, rol):
        if rol == "admin":
            self.ventana = AdminWindow()
        elif rol == "doctor":
            self.ventana = DoctorWindow()
        elif rol == "paciente":
            self.ventana = PacienteWindow()
        elif rol == "administrativo":
            self.ventana = AdministrativoWindow()
            
       
        self.ventana.setWindowState(Qt.WindowMaximized)
        self.ventana.showMaximized()