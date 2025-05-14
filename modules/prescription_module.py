from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                            QTableWidget, QTableWidgetItem, QDialog, 
                            QDialogButtonBox, QHBoxLayout, QLineEdit, 
                            QComboBox, QMessageBox, QFileDialog, QFormLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from fpdf import FPDF
import os
from datetime import datetime

class PrescriptionModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_data()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Generación de Recetas Médicas - IMSS")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Folio", "Paciente", "Fecha", "Medicamentos", "Indicaciones", "Estado"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Agregar Receta")
        btn_edit = QPushButton("Editar Receta")
        btn_generate = QPushButton("Generar PDF")

        btn_add.clicked.connect(self.add_record)
        btn_edit.clicked.connect(self.edit_record)
        btn_generate.clicked.connect(self.generate_selected_pdf)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_generate)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_sample_data(self):
        today = datetime.now().strftime("%A %d de %B del %Y").lower()
        self.add_row([
            "1397081375963", 
            "JOSE MANUEL GARCIA GARCIA", 
            today, 
            "[('fluoxetina (prozac) 20 mg', 'ORAL TABLETAS', 'Tomar 1 tableta cada 12 horas por 12 días'), "
            "('complejo B 100 mg', 'INTRAMUSCULAR', '1 cada 24 horas por 5 días')]",
            "Guardar reposo día en curso. Acudir al término del tratamiento.",
            "Activo"
        ])

    def add_row(self, data):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, val in enumerate(data):
            self.table.setItem(row, col, QTableWidgetItem(val))

    def add_record(self):
        self.show_record_dialog()

    def edit_record(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Seleccione una fila para editar.")
            return
        existing_data = [self.table.item(current_row, i).text() for i in range(6)]
        self.show_record_dialog(existing_data, current_row)

    def show_record_dialog(self, existing_data=None, edit_row=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Receta Médica IMSS")
        dialog.setMinimumWidth(600)
        layout = QVBoxLayout()

        # Formulario principal
        form_layout = QFormLayout()
        
        # Datos básicos
        self.folio_input = QLineEdit()
        self.paciente_input = QLineEdit()
        self.fecha_input = QLineEdit(datetime.now().strftime("%A %d de %B del %Y").lower())
        self.fecha_input.setEnabled(False)
        self.estado_input = QComboBox()
        self.estado_input.addItems(["Activo", "Inactivo"])
        
        form_layout.addRow("Folio:", self.folio_input)
        form_layout.addRow("Paciente:", self.paciente_input)
        form_layout.addRow("Fecha:", self.fecha_input)
        form_layout.addRow("Estado:", self.estado_input)
        
        # Datos IMSS adicionales
        self.nss_input = QLineEdit()
        self.amed_input = QLineEdit()
        self.delegacion_input = QLineEdit("UMF. CARLOS GALVEZ BETANCOURT")
        self.unidad_input = QLineEdit("UMF NO. 26")
        self.consultorio_input = QLineEdit()
        self.turno_input = QComboBox()
        self.turno_input.addItems(["MATUTINO", "VESPERTINO"])
        
        form_layout.addRow("NSS:", self.nss_input)
        form_layout.addRow("A. MED.:", self.amed_input)
        form_layout.addRow("Delegación:", self.delegacion_input)
        form_layout.addRow("Unidad:", self.unidad_input)
        form_layout.addRow("Consultorio:", self.consultorio_input)
        form_layout.addRow("Turno:", self.turno_input)
        
        # Medicamentos
        self.medicamentos_layout = QVBoxLayout()
        self.medicamentos_inputs = []
        
        def add_medicamento_row(medicamento="", via="", indicaciones=""):
            hbox = QHBoxLayout()
            med = QLineEdit(medicamento)
            med.setPlaceholderText("Medicamento y dosis")
            via_input = QComboBox()
            via_input.addItems(["ORAL TABLETAS", "INTRAMUSCULAR", "SUBCUTÁNEA", "TÓPICO", "OTRO"])
            if via: via_input.setCurrentText(via)
            indicaciones_input = QLineEdit(indicaciones)
            indicaciones_input.setPlaceholderText("Indicaciones")
            
            hbox.addWidget(med)
            hbox.addWidget(via_input)
            hbox.addWidget(indicaciones_input)
            self.medicamentos_layout.addLayout(hbox)
            self.medicamentos_inputs.append((med, via_input, indicaciones_input))
        
        add_medicamento_row()
        
        btn_add_medicamento = QPushButton("➕ Agregar otro medicamento")
        btn_add_medicamento.clicked.connect(lambda: add_medicamento_row())
        
        # Indicaciones generales
        self.indicaciones_input = QLineEdit()
        self.indicaciones_input.setPlaceholderText("Ej: Guardar reposo, acudir a valoración...")
        
        form_layout.addRow(QLabel("Medicamentos:"))
        form_layout.addRow(self.medicamentos_layout)
        form_layout.addRow(btn_add_medicamento)
        form_layout.addRow("Indicaciones generales:", self.indicaciones_input)
        
        layout.addLayout(form_layout)
        
        # Botones
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)
        dialog.setLayout(layout)

        # Cargar datos existentes si estamos editando
        if existing_data:
            self.folio_input.setText(existing_data[0])
            self.paciente_input.setText(existing_data[1])
            self.fecha_input.setText(existing_data[2])
            self.estado_input.setCurrentText(existing_data[5])
            self.indicaciones_input.setText(existing_data[4])
            
            # Parsear medicamentos
            medicamentos = eval(existing_data[3]) if existing_data[3].startswith("[") else []
            for m, via, ind in medicamentos:
                add_medicamento_row(m, via, ind)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            # Validar campos obligatorios
            if not all([
                self.folio_input.text(),
                self.paciente_input.text(),
                any(m[0].text() for m in self.medicamentos_inputs)
            ]):
                QMessageBox.warning(self, "Error", "Folio, paciente y al menos un medicamento son obligatorios.")
                return
            
            # Preparar datos
            medicamentos = [
                (m.text(), via.currentText(), ind.text()) 
                for m, via, ind in self.medicamentos_inputs 
                if m.text()
            ]
            
            data = [
                self.folio_input.text(),
                self.paciente_input.text(),
                self.fecha_input.text(),
                str(medicamentos),
                self.indicaciones_input.text(),
                self.estado_input.currentText()
            ]
            
            if edit_row is not None:
                for col, val in enumerate(data):
                    self.table.setItem(edit_row, col, QTableWidgetItem(val))
            else:
                self.add_row(data)

    def generate_selected_pdf(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Seleccione una receta.")
            return

        data = [self.table.item(current_row, i).text() for i in range(6)]
        default_name = f"Receta_{data[0]}_{data[1].split()[0]}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Receta", default_name, "PDF Files (*.pdf)")
        
        if file_path:
            self.generate_imss_pdf(data, file_path)
            QMessageBox.information(self, "Éxito", f"Receta guardada en:\n{file_path}")

    def generate_imss_pdf(self, data, path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Establecer fuentes
        pdf.set_font("Arial", "B", 12)
        
        # Encabezado IMSS (simplificado sin logo)
        pdf.cell(0, 6, "INSTITUTO MEXICANO DEL SEGURO SOCIAL", ln=1, align='C')
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 5, "SEGURIDAD Y EXCLUSIVIDAD SOCIAL", ln=1, align='C')
        pdf.ln(3)
        
        # Dirección
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, "DIRECCIÓN DE PRESTACIONES MÉDICAS", ln=1, align='C')
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "RECETA INDIVIDUAL", ln=1, align='C')
        pdf.ln(5)
        
        # Fecha
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, f"Fecha: {data[2]}", ln=1)
        pdf.ln(3)
        
        # Datos del paciente (simulados)
        pdf.cell(50, 6, f"NSS: {self.nss_input.text() if hasattr(self, 'nss_input') else '5715-96-1862-8'}", ln=0)
        pdf.cell(50, 6, f"A. MED.: {self.amed_input.text() if hasattr(self, 'amed_input') else '1F1986E5'}", ln=1)
        pdf.cell(0, 6, f"NOMBRE DEL PACIENTE: {data[1].upper()}", ln=1)
        pdf.ln(3)
        
        # Datos de la unidad médica (simulados)
        pdf.cell(60, 6, f"DELEGACIÓN: {self.delegacion_input.text() if hasattr(self, 'delegacion_input') else 'UMF. CARLOS GALVEZ BETANCOURT'}", ln=0)
        pdf.cell(60, 6, f"UNIDAD: {self.unidad_input.text() if hasattr(self, 'unidad_input') else 'UMF NO. 26'}", ln=1)
        pdf.cell(60, 6, f"CVE. PTAL: 130901252110", ln=0)
        pdf.cell(40, 6, f"CONSULTORIO: {self.consultorio_input.text() if hasattr(self, 'consultorio_input') else '4'}", ln=0)
        pdf.cell(40, 6, f"TURNO: {self.turno_input.currentText() if hasattr(self, 'turno_input') else 'MATUTINO'}", ln=1)
        pdf.ln(5)
        
        # Folio y advertencia
        pdf.cell(0, 6, f"Folio: {data[0]}", ln=1)
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 5, "ESTA RECETA NO SE SURTIRÁ DESPUÉS DE LAS 72 HORAS DE SU EXPEDICIÓN", ln=1)
        pdf.ln(8)
        
        # Medicamentos
        pdf.set_font("Arial", size=10)
        medicamentos = eval(data[3]) if data[3].startswith("[") else []
        
        for i, (med, via, indic) in enumerate(medicamentos, 1):
            pdf.cell(10, 7, f"{i}.-", ln=0)
            pdf.cell(60, 7, f"{med}", ln=0)
            pdf.cell(40, 7, f"{via}", ln=0)
            pdf.multi_cell(0, 7, f"{indic}", ln=1)
            pdf.ln(2) if i < len(medicamentos) else None
        
        pdf.ln(8)
        
        # Indicaciones generales
        if data[4]:
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 6, data[4])
            pdf.ln(8)
        
        # Firma del médico
        pdf.set_font("Arial", size=10)
        pdf.cell(70, 6, "Nombre y firma del Médico", ln=0)
        pdf.cell(50, 6, "Cédula Profesional", ln=0)
        pdf.cell(50, 6, "Matrícula", ln=1)
        pdf.cell(70, 6, "DR. JUAN PÉREZ GÓMEZ", ln=0)
        pdf.cell(50, 6, "1234567", ln=0)
        pdf.cell(50, 6, "987654321", ln=1)
        pdf.ln(15)
        
        # Firma del paciente
        pdf.cell(0, 6, "PACIENTE", ln=1, align='C')
        pdf.line(pdf.get_x() + 70, pdf.get_y(), pdf.get_x() + 120, pdf.get_y())
        
        pdf.output(path)