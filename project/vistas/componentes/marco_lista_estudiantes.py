import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
from utilidades.niveles_grados import NivelesGrados

class MarcoListaEstudiantes(ctk.CTkFrame):
    def __init__(self, padre, al_seleccionar_estudiante=None):
        super().__init__(padre)
        self.al_seleccionar_estudiante = al_seleccionar_estudiante
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Marco de control
        marco_control = ctk.CTkFrame(self)
        marco_control.pack(fill="x", padx=5, pady=5)

        # Selección de año
        marco_año = ctk.CTkFrame(marco_control)
        marco_año.pack(side="left", padx=5)
        ctk.CTkLabel(marco_año, text="Año:").pack(side="left", padx=5)
        año_actual = datetime.now().year
        self.combo_año = ctk.CTkComboBox(
            marco_año,
            values=[str(año) for año in range(año_actual-2, año_actual+1)],
            command=self._al_cambiar_filtro,
            width=100
        )
        self.combo_año.pack(side="left", padx=5)
        self.combo_año.set(str(año_actual))

        # Selección de nivel
        marco_nivel = ctk.CTkFrame(marco_control)
        marco_nivel.pack(side="left", padx=5)
        ctk.CTkLabel(marco_nivel, text="Nivel:").pack(side="left", padx=5)
        self.combo_nivel = ctk.CTkComboBox(
            marco_nivel,
            values=[""] + NivelesGrados.obtener_niveles(),
            command=self._al_cambiar_nivel,
            width=120
        )
        self.combo_nivel.pack(side="left", padx=5)
        self.combo_nivel.set("")

        # Selección de grado
        marco_grado = ctk.CTkFrame(marco_control)
        marco_grado.pack(side="left", padx=5)
        ctk.CTkLabel(marco_grado, text="Sala/Grado/Año:").pack(side="left", padx=5)
        self.combo_grado = ctk.CTkComboBox(
            marco_grado,
            values=[],
            command=self._al_cambiar_filtro,
            width=120
        )
        self.combo_grado.pack(side="left", padx=5)

        # Configurar tabla
        self.configurar_tabla()

    def configurar_tabla(self):
        marco_tabla = ttk.Frame(self)
        marco_tabla.pack(fill="both", expand=True, padx=5, pady=5)

        # Crear Treeview
        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=("DNI", "Apellido", "Nombre", "Fecha Registro", "Estado"),
            show="headings"
        )

        # Configurar columnas
        self.tabla.heading("DNI", text="DNI")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Fecha Registro", text="Fecha Registro")
        self.tabla.heading("Estado", text="Estado")

        self.tabla.column("DNI", width=100)
        self.tabla.column("Apellido", width=150)
        self.tabla.column("Nombre", width=150)
        self.tabla.column("Fecha Registro", width=100)
        self.tabla.column("Estado", width=100)

        # Agregar barra de desplazamiento
        barra_desplazamiento = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra_desplazamiento.set)

        # Empaquetar elementos
        self.tabla.pack(side="left", fill="both", expand=True)
        barra_desplazamiento.pack(side="right", fill="y")

        # Vincular evento de selección
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_estudiante)

    def _al_cambiar_nivel(self, _):
        nivel = self.combo_nivel.get()
        grados = NivelesGrados.obtener_grados_por_nivel(nivel)
        self.combo_grado.configure(values=grados)
        if grados:
            self.combo_grado.set(grados[0])
        else:
            self.combo_grado.set("")
        self._al_cambiar_filtro(None)

    def _al_cambiar_filtro(self, _):
        self.actualizar_lista_estudiantes()

    def _al_seleccionar_estudiante(self, _):
        if self.al_seleccionar_estudiante and self.tabla.selection():
            item = self.tabla.item(self.tabla.selection()[0])
            dni = item["values"][0]
            self.al_seleccionar_estudiante(dni)

    def actualizar_lista_estudiantes(self):
        # Limpiar lista actual
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Obtener filtros
        año = self.combo_año.get()
        grado = self.combo_grado.get()
        
        if not grado:
            return

        # Obtener estudiantes del repositorio
        estudiantes = self.obtener_estudiantes_por_grado_y_año(grado, año)
        
        # Actualizar tabla
        for estudiante in estudiantes:
            self.tabla.insert("", "end", values=(
                estudiante.dni,
                estudiante.apellido,
                estudiante.nombre,
                estudiante.fecha_registro,
                "Activo" if estudiante.activo else "Inactivo"
            ))

    def obtener_estudiantes_por_grado_y_año(self, grado, año):
        from repositorios.repositorio_estudiantes import RepositorioEstudiantes
        return RepositorioEstudiantes.obtener_estudiantes_por_grado_y_año(grado, año)