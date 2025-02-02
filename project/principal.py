import customtkinter as ctk
from base_datos.db_config import init_db
from vistas.pestaña_registro import PestañaRegistro
from vistas.pestaña_precios import PestañaPrecios
from vistas.pestaña_pagos import PestañaPagos
from vistas.pestaña_cobranza import PestañaCobranza

class AppGestionEscolar:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title("Instituto Incorporado San Andrés por Pablo Sánchez")
        
        # Obtener dimensiones de la pantalla
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        
        # Configurar geometría para pantalla completa
        self.ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
        
        # Maximizar ventana
        self.ventana.state('zoomed')

        # Configurar tamaño de fuente predeterminado
        ctk.set_widget_scaling(1.2)  # Aumentar tamaño de widgets en 20%
        ctk.set_window_scaling(1.2)  # Aumentar escala de ventana en 20%
        
        # Inicializar base de datos
        init_db()

        # Crear notebook (pestañas) con texto más grande
        self.notebook = ctk.CTkTabview(
            self.ventana, 
            text_color="black", 
            segmented_button_fg_color="gray85", 
            segmented_button_selected_color="gray75", 
            segmented_button_selected_hover_color="gray70",
            segmented_button_unselected_color="gray90", 
            segmented_button_unselected_hover_color="gray80"
        )
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Agregar pestañas
        self.notebook.add("Registro de estudiantes")
        self.notebook.add("Carga de items")
        self.notebook.add("Generación de pagos")
        self.notebook.add("Cobranza")
        
        # Agregar contenido a las pestañas
        self.pestaña_registro = PestañaRegistro(self.notebook.tab("Registro de estudiantes"))
        self.pestaña_registro.pack(expand=True, fill="both", padx=10, pady=10)

        self.pestaña_precios = PestañaPrecios(self.notebook.tab("Carga de items"))
        self.pestaña_precios.pack(expand=True, fill="both", padx=10, pady=10)

        self.pestaña_pagos = PestañaPagos(self.notebook.tab("Generación de pagos"))
        self.pestaña_pagos.pack(expand=True, fill="both", padx=10, pady=10)

        self.pestaña_cobranza = PestañaCobranza(self.notebook.tab("Cobranza"))
        self.pestaña_cobranza.pack(expand=True, fill="both", padx=10, pady=10)

        # Establecer pestaña inicial en "Cobranza"
        self.notebook.set("Cobranza")

    def ejecutar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = AppGestionEscolar()
    app.ejecutar()