import customtkinter as ctk
from utilidades.niveles_grados import NivelesGrados
from vistas.componentes.utilidades_formulario import crear_entrada, crear_combobox

class FormularioEstudiante(ctk.CTkFrame):
    def __init__(self, padre):
        super().__init__(padre)
        self.modo_edicion = False
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Título
        titulo = ctk.CTkLabel(self, text="Datos del Estudiante", font=("Arial", 16, "bold"))
        titulo.pack(pady=5)

        # Contenedor para los campos
        contenedor_campos = ctk.CTkFrame(self)
        contenedor_campos.pack(fill="both", expand=True, padx=5, pady=5)

        # Primera columna - Campos obligatorios
        col1 = ctk.CTkFrame(contenedor_campos)
        col1.pack(side="left", fill="both", expand=True, padx=5)

        self.dni = crear_entrada(col1, "DNI: *")
        self.nombre = crear_entrada(col1, "Nombres: *")
        self.apellido = crear_entrada(col1, "Apellidos: *")
        self.nivel = crear_combobox(
            col1, 
            "Nivel: *", 
            NivelesGrados.obtener_niveles(),
            command=self._al_cambiar_nivel
        )
        self.nivel.set("")
        self.grado = crear_combobox(col1, "Sala/Grado/Año: *", [])
        self.grado.set("")
        
        # Marco para doble jornada
        self.marco_doble_jornada = ctk.CTkFrame(col1)
        self.marco_doble_jornada.pack(fill="x", pady=2)
        self.var_doble_jornada = ctk.BooleanVar(value=False)
        self.casilla_doble_jornada = ctk.CTkCheckBox(
            self.marco_doble_jornada,
            text="Doble Jornada",
            variable=self.var_doble_jornada
        )
        self.casilla_doble_jornada.pack(side="left", padx=5)

        # Segunda columna - Campos opcionales
        col2 = ctk.CTkFrame(contenedor_campos)
        col2.pack(side="left", fill="both", expand=True, padx=5)

        self.fecha_nacimiento = crear_entrada(col2, "Fecha de Nacimiento:")
        self.genero = crear_combobox(col2, "Género:", ["", "Masculino", "Femenino", "Otro"])
        self.genero.set("")
        self.direccion = crear_entrada(col2, "Dirección:")
        self.telefono_emergencia = crear_entrada(col2, "Teléfono de Emergencia:")
        
        # Botones
        self.marco_botones = ctk.CTkFrame(self)
        self.marco_botones.pack(fill="x", pady=10)
        
        self.boton_guardar = ctk.CTkButton(
            self.marco_botones,
            text="Guardar",
            state="normal"
        )
        self.boton_guardar.pack(side="left", padx=5)
        
        self.boton_limpiar = ctk.CTkButton(
            self.marco_botones,
            text="Limpiar"
        )
        self.boton_limpiar.pack(side="left", padx=5)

        self.boton_dar_baja = ctk.CTkButton(
            self.marco_botones,
            text="Dar de Baja",
            fg_color="red",
            state="disabled"
        )
        self.boton_dar_baja.pack(side="left", padx=5)

    def _al_cambiar_nivel(self, nivel):
        """Manejador del evento de cambio de nivel"""
        self.actualizar_grados(nivel)

    def actualizar_grados(self, nivel):
        """Actualiza la lista de grados según el nivel seleccionado"""
        grados = NivelesGrados.obtener_grados_por_nivel(nivel)
        self.grado.configure(values=grados)
        if grados:
            self.grado.set(grados[0])
        
        # Mostrar/ocultar opción de doble jornada según el nivel
        if nivel in ["Inicial", "Primario"]:
            self.casilla_doble_jornada.pack(side="left", padx=5)
        else:
            self.casilla_doble_jornada.pack_forget()
            self.var_doble_jornada.set(False)

    def limpiar_formulario(self):
        # Limpiar campos obligatorios
        self.dni.delete(0, 'end')
        self.nombre.delete(0, 'end')
        self.apellido.delete(0, 'end')
        self.nivel.set("")
        self.grado.set("")
        self.grado.configure(values=[])
        
        # Limpiar campos opcionales
        self.fecha_nacimiento.delete(0, 'end')
        self.genero.set("")
        self.direccion.delete(0, 'end')
        self.telefono_emergencia.delete(0, 'end')
        
        # Resetear doble jornada
        self.var_doble_jornada.set(False)
        
        # Resetear estado de edición
        self.modo_edicion = False
        self.dni.configure(state="normal")
        
        # Resetear botones
        if hasattr(self, 'boton_dar_baja'):
            self.boton_dar_baja.configure(state="disabled")
        if hasattr(self, 'boton_reactivar'):
            self.boton_reactivar.configure(state="disabled")
        if hasattr(self, 'boton_guardar'):
            self.boton_guardar.configure(state="normal")

    def entrar_modo_edicion(self):
        """Activa el modo de edición"""
        self.modo_edicion = True
        self.dni.configure(state="disabled")
        self.boton_dar_baja.configure(state="normal")

    def salir_modo_edicion(self):
        """Desactiva el modo de edición"""
        self.modo_edicion = False
        self.dni.configure(state="normal")
        self.boton_dar_baja.configure(state="disabled")
        if hasattr(self, 'boton_reactivar'):
            self.boton_reactivar.configure(state="disabled")

    def establecer_datos_estudiante(self, estudiante):
        """Establece los datos del estudiante en el formulario"""
        self.dni.delete(0, 'end')
        self.dni.insert(0, estudiante.dni)
        self.nombre.delete(0, 'end')
        self.nombre.insert(0, estudiante.nombre)
        self.apellido.delete(0, 'end')
        self.apellido.insert(0, estudiante.apellido)
        self.fecha_nacimiento.delete(0, 'end')
        self.fecha_nacimiento.insert(0, estudiante.fecha_nacimiento)
        self.genero.set(estudiante.genero)
        self.direccion.delete(0, 'end')
        self.direccion.insert(0, estudiante.direccion)
        self.telefono_emergencia.delete(0, 'end')
        self.telefono_emergencia.insert(0, estudiante.telefono_emergencia)
        
        # Determinar nivel basado en el grado
        for nivel in NivelesGrados.obtener_niveles():
            if estudiante.grado in NivelesGrados.obtener_grados_por_nivel(nivel):
                self.nivel.set(nivel)
                self.actualizar_grados(nivel)
                self.grado.set(estudiante.grado)
                self.var_doble_jornada.set(estudiante.doble_jornada)
                break