from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QDialogButtonBox, QHBoxLayout,
    QLineEdit, QComboBox, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from fpdf import FPDF
from num2words import num2words
import os

class BillingModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_data()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Gestión de Facturación")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID Factura", "ID Paciente", "Fecha", "Conceptos", "Monto", "Estado"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Agregar Factura")
        btn_edit = QPushButton("Editar Factura")
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
        self.add_row(["F001", "1", "2025-05-01", "[('Consulta general', '500.00')]", "500.00", "Pagado"])
        self.add_row(["F002", "2", "2025-05-03", "[('Análisis de sangre', '850.00')]", "850.00", "Pendiente"])

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
        dialog.setWindowTitle("Factura")
        layout = QVBoxLayout()

        fields = [
            ("ID Factura", QLineEdit()),
            ("ID Paciente", QLineEdit()),
            ("Fecha", QLineEdit("YYYY-MM-DD")),
            ("Estado", QComboBox())
        ]
        fields[3][1].addItems(["Pagado", "Pendiente"])

        for label_text, widget in fields:
            row = QHBoxLayout()
            row.addWidget(QLabel(label_text))
            row.addWidget(widget)
            layout.addLayout(row)

        concept_layout = QVBoxLayout()
        concept_inputs = []

        def add_concept_row(concept="", price=""):
            hbox = QHBoxLayout()
            concepto = QLineEdit(concept)
            monto = QLineEdit(price)
            concepto.setPlaceholderText("Concepto")
            monto.setPlaceholderText("Monto")
            hbox.addWidget(concepto)
            hbox.addWidget(monto)
            concept_layout.addLayout(hbox)
            concept_inputs.append((concepto, monto))

        add_concept_row()

        btn_add_concept = QPushButton("Agregar otro concepto")
        btn_add_concept.clicked.connect(lambda: add_concept_row())

        layout.addWidget(QLabel("Conceptos y montos:"))
        layout.addLayout(concept_layout)
        layout.addWidget(btn_add_concept)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)
        dialog.setLayout(layout)

        if existing_data:
            for i, (_, widget) in enumerate(fields):
                if isinstance(widget, QLineEdit):
                    widget.setText(existing_data[i])
                elif isinstance(widget, QComboBox):
                    widget.setCurrentText(existing_data[i])
            conceptos = eval(existing_data[3]) if existing_data[3].startswith("[") else [(existing_data[3], existing_data[4])]
            concept_inputs.clear()
            for c, m in conceptos:
                add_concept_row(c, m)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            values = [widget.text() if isinstance(widget, QLineEdit) else widget.currentText() for _, widget in fields]
            conceptos = [(c.text(), m.text()) for c, m in concept_inputs if c.text() and m.text()]
            total = sum(float(m) for _, m in conceptos)

            if all(values) and conceptos:
                if edit_row is not None:
                    for col, val in enumerate(values):
                        self.table.setItem(edit_row, col, QTableWidgetItem(val))
                    self.table.setItem(edit_row, 3, QTableWidgetItem(str(conceptos)))
                    self.table.setItem(edit_row, 4, QTableWidgetItem(f"{total:.2f}"))
                else:
                    self.add_row([*values[:3], str(conceptos), f"{total:.2f}", values[3]])
            else:
                QMessageBox.warning(self, "Error", "Todos los campos y conceptos son obligatorios.")

    def generate_selected_pdf(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Seleccione una fila.")
            return

        data = [self.table.item(current_row, i).text() for i in range(6)]
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Factura", f"{data[0]}.pdf", "PDF Files (*.pdf)")

        if file_path:
            self.generate_pdf(data, file_path)
            QMessageBox.information(self, "Éxito", "Factura generada correctamente.")

    def generate_pdf(self, data, path):
        conceptos = eval(data[3]) if data[3].startswith("[") else [(data[3], data[4])]
        total = sum(float(m) for _, m in conceptos)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 10)
        pdf.image(os.path.join(os.path.dirname(__file__), r"../img/imss.png"), x=10, y=8, w=30)
        pdf.cell(0, 10, "INSTITUTO MEXICANO DEL SEGURO SOCIAL", ln=1, align='C')
        pdf.set_font("Arial", size=9)
        pdf.cell(0, 6, "Reforma 476, Col. Juárez, Del. Cuauhtémoc. México D.F., 06600", ln=1, align='C')
        pdf.cell(0, 6, "PERSONA MORAL CON FINES NO LUCRATIVOS - RFC: IMS421231I45", ln=1, align='C')
        pdf.cell(0, 6, f"Folio: {data[0]}", ln=1, align='R')
        pdf.cell(0, 6, f"Fecha de Emisión: {data[2]}", ln=1, align='R')
        pdf.ln(4)

        pdf.set_fill_color(220, 220, 220)
        pdf.set_font("Arial", "B", 9)
        pdf.cell(20, 8, "Cantidad", 1, 0, 'C', 1)
        pdf.cell(35, 8, "Unidad", 1, 0, 'C', 1)
        pdf.cell(65, 8, "Descripción", 1, 0, 'C', 1)
        pdf.cell(30, 8, "Precio Unitario", 1, 0, 'C', 1)
        pdf.cell(30, 8, "Importe", 1, 1, 'C', 1)

        pdf.set_font("Arial", size=9)
        for concepto, monto in conceptos:
            pdf.cell(20, 8, "1", 1, 0, 'C')
            pdf.cell(35, 8, "Servicio", 1, 0, 'C')
            pdf.cell(65, 8, concepto, 1, 0, 'L')
            pdf.cell(30, 8, f"${monto}", 1, 0, 'R')
            pdf.cell(30, 8, f"${monto}", 1, 1, 'R')

        pdf.ln(4)
        total_letra = num2words(total, lang='es').upper() + " PESOS M.N."
        pdf.multi_cell(0, 6, f"Total con letra: {total_letra}", 0, 'L')
        pdf.cell(0, 6, f"TOTAL: ${total:.2f}", ln=1, align='R')
        pdf.ln(10)

        pdf.set_font("Arial", size=8)
        pdf.multi_cell(0, 5, "Sello Digital del CFDI: [Simulación]\nSello del SAT: [Simulación]\nCadena Original del complemento de certificación digital del SAT: [Simulación]", 0, 'L')
        pdf.ln(3)
        pdf.cell(0, 5, "Este documento es una representación impresa de un CFDI", 0, 1, 'C')

        pdf.output(path)
