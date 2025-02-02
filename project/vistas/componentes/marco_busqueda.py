import customtkinter as ctk
from tkinter import ttk
from modelos.estudiante import Estudiante

class MarcoBusqueda(ctk.CTkFrame):
    def __init__(self, padre, al_resultado_busqueda):
        super().__init__(padre)
        self.al_resultado_busqueda = al_resultado_busqueda
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Marco de búsqueda
        controles_busqueda = ctk.CTkFrame(self)
        controles_busqueda.pack(fill="x", padx=5, pady=5)

        # Búsqueda por DNI
        self.marco_dni = ctk.CTkFrame(controles_busqueda)
        self.marco_dni.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkLabel(self.marco_dni, text="DNI:").pack(side="left", padx=5)
        self.entrada_dni = ctk.CTkEntry(self.marco_dni)
        self.entrada_dni.pack(side="left", fill="x", expand=True, padx=5)
        
        # Búsqueda por apellido
        self.marco_apellido = ctk.CTkFrame(controles_busqueda)
        self.marco_apellido.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkLabel(self.marco_apellido, text="Apellido:").pack(side="left", padx=5)
        self.entrada_apellido = ctk.CTkEntry(self.marco_apellido)
        self.entrada_apellido.pack(side="left", fill="x", expand=True, padx=5)

        # Casilla para incluir inactivos
        self.var_incluir_inactivos = ctk.BooleanVar(value=True)
        self.incluir_inactivos = ctk.CTkCheckBox(
            controles_busqueda,
            text="Incluir dados de baja",
            variable=self.var_incluir_inactivos
        )
        self.incluir_inactivos.pack(side="left", padx=5)

        # Botones de búsqueda
        self.marco_botones = ctk.CTkFrame(controles_busqueda)
        self.marco_botones.pack(side="left", padx=5)
        ctk.CTkButton(
            self.marco_botones,
            text="Buscar por DNI",
            command=self.buscar_por_dni
        ).pack(side="left", padx=2)
        ctk.CTkButton(
            self.marco_botones,
            text="Buscar por Apellido",
            command=self.buscar_por_apellido
        ).pack(side="left", padx=2)

        # Tabla de resultados
        self.configurar_tabla_resultados()

    def configurar_tabla_resultados(self):
        # Marco para la tabla
        marco_tabla = ttk.Frame(self)
        marco_tabla.pack(fill="both", expand=True, padx=5, pady=5)

        # Crear Treeview
        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=("DNI", "Nombre", "Apellido", "Grado", "Doble Jornada", "Estado", "Fecha Registro"),
            show="headings"
        )

        # Configurar columnas
        self.tabla.heading("DNI", text="DNI")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("Grado", text="Grado")
        self.tabla.heading("Doble Jornada", text="Doble Jornada")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading("Fecha Registro", text="Fecha Registro")

        self.tabla.column("DNI", width=100)
        self.tabla.column("Nombre", width=150)
        self.tabla.column("Apellido", width=150)
        self.tabla.column("Grado", width=100)
        self.tabla.column("Doble Jornada", width=100)
        self.tabla.column("Estado", width=100)
        self.tabla.column("Fecha Registro", width=100)

        # Barra de desplazamiento
        barra_desplazamiento = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra_desplazamiento.set)

        # Empaquetar elementos
        self.tabla.pack(side="left", fill="both", expand=True)
        barra_desplazamiento.pack(side="right", fill="y")

        # Vincular evento de selección
        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar)

    def mostrar_resultados(self, estudiantes):
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Insertar resultados
        for estudiante in estudiantes:
            self.tabla.insert("", "end", values=(
                estudiante.dni,
                estudiante.nombre,
                estudiante.apellido,
                estudiante.grado,
                "Sí" if estudiante.doble_jornada else "No",
                "Inactivo" if not estudiante.activo else "Activo",
                estudiante.fecha_registro
            ))

    def al_seleccionar(self, evento):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            dni = item["values"][0]
            self.al_resultado_busqueda(dni, incluir_inactivos=self.var_incluir_inactivos.get())

    def buscar_por_dni(self):
        dni = self.entrada_dni.get().strip()
        if dni:
            self.al_resultado_busqueda(dni, es_dni=True, incluir_inactivos=self.var_incluir_inactivos.get())

    def buscar_por_apellido(self):
        apellido = self.entrada_apellido.get().strip()
        if apellido:
            self.al_resultado_busqueda(apellido, es_dni=False, incluir_inactivos=self.var_incluir_inactivos.get())

    def limpiar_busqueda(self):
        self.entrada_dni.delete(0, 'end')
        self.entrada_apellido.delete(0, 'end')
        self.var_incluir_inactivos.set(True)
        for item in self.tabla.get_children():
            self.tabla.delete(item)