from fpdf import FPDF
from datetime import datetime
import os

class ReciboPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(left=20, top=20, right=20)
        self.add_page()
        self.set_font('Arial', '', 12)

    def header(self):
        pass  # No se necesita encabezado ya que usamos formularios preimpresos

    def footer(self):
        pass  # No se necesita pie de página

class GeneradorPDF:
    @staticmethod
    def generar_recibo(pago, estudiante, cupon) -> str:
        try:
            # Crear directorio de recibos si no existe
            directorio_recibos = os.path.join(os.getcwd(), 'recibos')
            os.makedirs(directorio_recibos, exist_ok=True)

            # Crear PDF
            pdf = ReciboPDF()
            
            # Determinar nombre de la empresa según el nivel
            nombre_empresa = "Instituto Incorporado San Andrés" if cupon.nivel == "Secundario" else "Colegio Incorporado San Andrés"
            
            # Posición para número de recibo
            pdf.set_xy(150, 25)
            pdf.cell(0, 10, f"Nº {pago.numero_recibo}", 0, 1)
            
            # Posición para fecha
            pdf.set_xy(150, 35)
            pdf.cell(0, 10, f"Fecha: {pago.fecha_pago}", 0, 1)
            
            # Nombre de la empresa
            pdf.set_xy(20, 45)
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, nombre_empresa, 0, 1)
            pdf.set_font('Arial', '', 12)
            
            # Información del estudiante
            pdf.set_xy(20, 60)
            pdf.cell(0, 10, f"Alumno: {estudiante.apellido}, {estudiante.nombre}", 0, 1)
            pdf.set_xy(20, 70)
            pdf.cell(0, 10, f"DNI: {estudiante.dni}", 0, 1)
            pdf.set_xy(20, 80)
            pdf.cell(0, 10, f"Grado: {estudiante.grado}", 0, 1)
            
            # Información del pago
            pdf.set_xy(20, 100)
            pdf.cell(0, 10, f"Concepto: Cuota {cupon.mes}/{cupon.año_academico}", 0, 1)
            pdf.set_xy(20, 110)
            pdf.cell(0, 10, f"Monto: ${cupon.monto_total:.2f}", 0, 1)
            
            # Guardar PDF
            nombre_archivo = os.path.join(directorio_recibos, f"recibo_{pago.numero_recibo}.pdf")
            pdf.output(nombre_archivo)
            
            return nombre_archivo
        except Exception as e:
            print(f"Error al generar PDF: {e}")
            return None