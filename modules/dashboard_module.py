from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

class DashboardModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

       
        title = QLabel("Resumen General")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        stats_grid.setContentsMargins(0, 0, 0, 20)
        
        stats = [
            ("Usuarios", "124", "#3498DB", "user"),
            ("Hospitales", "8", "#27AE60", "hospital"),
            ("Doctores", "24", "#9B59B6", "doctor"),
            ("Pacientes", "156", "#3498DB", "patient"),
            ("Citas Hoy", "18", "#E67E22", "calendar"),
            ("Medicamentos", "45", "#1ABC9C", "pharmacy"),
            ("Consultorios", "12", "#1ABC9C", "office"),
            ("Laboratorios", "5", "#3498DB", "lab"),
        ]
        
        for i, (label, count, color, icon) in enumerate(stats):
            card = self.create_stat_card(label, count, color, icon)
            stats_grid.addWidget(card, i // 4, i % 4)

        main_layout.addLayout(stats_grid)

        
        charts_container = QFrame()
        charts_container.setStyleSheet("background: transparent;")
        charts_layout = QHBoxLayout(charts_container)
        charts_layout.setSpacing(15)
        
        
        left_chart_container = QFrame()
        left_chart_container.setStyleSheet("background: white; border-radius: 8px;")
        left_chart_layout = QVBoxLayout(left_chart_container)
        left_chart_layout.setContentsMargins(10, 10, 10, 10)
        
        pie_chart = self.create_pie_chart()
        pie_chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_chart_layout.addWidget(pie_chart)
        
        
        right_chart_container = QFrame()
        right_chart_container.setStyleSheet("background: white; border-radius: 8px;")
        right_chart_layout = QVBoxLayout(right_chart_container)
        right_chart_layout.setContentsMargins(10, 10, 10, 10)
        
        bar_chart = self.create_bar_chart()
        bar_chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_chart_layout.addWidget(bar_chart)
        
        charts_layout.addWidget(left_chart_container, 60)
        charts_layout.addWidget(right_chart_container, 40)
        main_layout.addWidget(charts_container)

        
        activities_frame = self.create_activity_frame()
        activities_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(activities_frame)

        self.setLayout(main_layout)

    def create_stat_card(self, label, count, color, icon):
        card = QFrame()
        card.setMinimumHeight(100)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                padding: 15px;
                border-left: 5px solid {color};
            }}
            QLabel#count {{
                font-size: 28px;
                font-weight: bold;
                color: {color};
            }}
            QLabel#label {{
                font-size: 14px;
                color: #7F8C8D;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(5)
        
       
        top_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_pixmap = QIcon.fromTheme(icon).pixmap(24, 24)
        icon_label.setPixmap(icon_pixmap)
        
        count_label = QLabel(count)
        count_label.setObjectName("count")
        
        top_layout.addWidget(icon_label)
        top_layout.addWidget(count_label)
        top_layout.addStretch()
        
        
        label_label = QLabel(label)
        label_label.setObjectName("label")
        
        card_layout.addLayout(top_layout)
        card_layout.addWidget(label_label)
        card_layout.addStretch()
        
        return card

    def create_pie_chart(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        roles = ['Admin', 'Doctor', 'Paciente', 'Administrativo']
        counts = [10, 35, 65, 14]
        colors = ['#3498DB', '#9B59B6', '#3498DB', '#E74C3C']
        
        
        wedges, texts, autotexts = ax.pie(
            counts, 
            labels=roles, 
            colors=colors, 
            autopct='%1.1f%%', 
            startangle=140,
            shadow=True,
            explode=(0.05, 0.05, 0.05, 0.05),
            textprops={'fontsize': 8}
        )
        
        
        ax.axis('equal')  
        ax.set_title("Distribución de Usuarios", pad=20, fontsize=10)
        
        canvas = FigureCanvas(fig)
        canvas.setStyleSheet("background: transparent;")
        return canvas

    def create_bar_chart(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']
        citas = [12, 15, 8, 18, 20, 5]
        
        
        gradient = np.linspace(0.3, 1, len(dias))
        colors = plt.cm.Greens(gradient)
        
        bars = ax.bar(dias, citas, color=colors, edgecolor='#27AE60', linewidth=1)
        
      
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height}',
                    ha='center', va='bottom', fontsize=8)
        
        ax.set_title("Citas por Día", pad=15, fontsize=10)
        ax.set_ylabel("Número de Citas", fontsize=8)
        ax.tick_params(axis='both', which='major', labelsize=8)
        
        canvas = FigureCanvas(fig)
        canvas.setStyleSheet("background: transparent;")
        return canvas

    def create_activity_frame(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
            }
            QLabel#title {
                font-size: 16px;
                font-weight: bold;
                color: #2C3E50;
                margin-bottom: 10px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(10)
        
        title = QLabel("Últimas Actividades")
        title.setObjectName("title")
        layout.addWidget(title)
        
        activities = [
            ("15/05 09:30", "admin@clinica.com", "Creó nuevo usuario doctor@clinica.com"),
            ("15/05 11:42", "admin@clinica.com", "Actualizó datos del hospital central"),
            ("15/05 14:30", "admin@clinica.com", "Eliminó usuario temporal@clinica.com"),
            ("15/05 16:45", "doctor@clinica.com", "Cierre de sesión"),
        ]
        
        for date, user, action in activities:
            item_frame = QFrame()
            item_frame.setStyleSheet("""
                QFrame {
                    background-color: #F8F9FA;
                    border-radius: 6px;
                    padding: 8px;
                }
                QLabel {
                    font-size: 12px;
                }
            """)
            
            item_layout = QHBoxLayout(item_frame)
            item_layout.setContentsMargins(5, 5, 5, 5)
            
            date_label = QLabel(date)
            date_label.setStyleSheet("color: #7F8C8D; min-width: 80px;")
            
            user_label = QLabel(user)
            user_label.setStyleSheet("color: #3498DB; min-width: 150px; font-weight: bold;")
            
            action_label = QLabel(action)
            action_label.setStyleSheet("color: #2C3E50;")
            action_label.setWordWrap(True)
            
            item_layout.addWidget(date_label)
            item_layout.addWidget(user_label)
            item_layout.addWidget(action_label)
            item_layout.setStretch(2, 1)
            
            layout.addWidget(item_frame)
        
        return frame