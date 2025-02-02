import customtkinter as ctk
from tkinter import messagebox
from modelos.estudiante import Estudiante
from modelos.tutor import Tutor
from repositorios.repositorio_estudiantes import RepositorioEstudiantes
from repositorios.repositorio_tutores import RepositorioTutores
from vistas.componentes.marco_busqueda import MarcoBusqueda
from vistas.componentes.formulario_estudiante import FormularioEstudiante
from vistas.componentes.formulario_tutor import FormularioTutor
from vistas.componentes.marco_lista_estudiantes import MarcoListaEstudiantes
from vistas.manejadores.manejador_busqueda import ManejadorBusqueda
from base_datos.supabase_config import conexion_exitosa

class PestañaRegistro(ctk.CTkFrame):
    def __init__(self, padre):
        super().__init__(padre)
        self.estudiante_actual = None
        self.manejador_busqueda = ManejadorBusqueda(self)
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Verificar conexión
        if not conexion_exitosa:
            label_error = ctk.CTkLabel(
                self,
                text="Error de conexión: Algunas funciones no estarán disponibles",
                text_color="red"
            )
            label_error.pack(pady=10)

        # Marco de búsqueda
        self.marco_busqueda = MarcoBusqueda(self, self.manejador_busqueda.manejar_resultado_busqueda)
        self.marco_busqueda.pack(fill="x", padx=10, pady=5)

        # Marco para lista de estudiantes
        self.lista_estudiantes = MarcoListaEstudiantes(self, self.al_seleccionar_estudiante)
        self.lista_estudiantes.pack(fill="x", padx=10, pady=5)

        # Marco para formularios
        contenedor_formularios = ctk.CTkFrame(self)
        contenedor_formularios.pack(fill="both", expand=True, padx=10, pady=5)

        # Formulario de estudiante (lado izquierdo)
        self.formulario_estudiante = FormularioEstudiante(contenedor_formularios)
        self.formulario_estudiante.pack(side="left", fill="both", expand=True, padx=5)

        # Formulario de tutor (lado derecho)
        self.formulario_tutor = FormularioTutor(contenedor_formularios)
        self.formulario_tutor.pack(side="right", fill="both", expand=True, padx=5)

        # Configurar callbacks
        self.formulario_estudiante.boton_guardar.configure(command=self.guardar_estudiante)
        self.formulario_estudiante.boton_limpiar.configure(command=self.limpiar_todos_formularios)
        self.formulario_estudiante.boton_dar_baja.configure(command=self.dar_baja_estudiante)
        
        # Agregar botón de reactivar
        self.formulario_estudiante.boton_reactivar = ctk.CTkButton(
            self.formulario_estudiante.marco_botones,
            text="Reactivar",
            fg_color="green",
            state="disabled",
            command=self.reactivar_estudiante
        )
        self.formulario_estudiante.boton_reactivar.pack(side="left", padx=5)

    def al_seleccionar_estudiante(self, dni):
        """Maneja la selección de un estudiante de la lista"""
        self.manejador_busqueda.manejar_resultado_busqueda(dni, es_dni=True, incluir_inactivos=True)

    def limpiar_todos_formularios(self):
        """Limpia todos los formularios y resetea el estado"""
        self.estudiante_actual = None
        self.formulario_estudiante.limpiar_formulario()
        self.formulario_tutor.limpiar_formulario()
        self.marco_busqueda.limpiar_busqueda()

    def guardar_estudiante(self):
        """Guarda o actualiza un estudiante"""
        if not conexion_exitosa:
            messagebox.showerror("Error", "No hay conexión con la base de datos")
            return

        try:
            # Verificar campos obligatorios
            campos_obligatorios = {
                'DNI': self.formulario_estudiante.dni.get().strip(),
                'Nombre': self.formulario_estudiante.nombre.get().strip(),
                'Apellido': self.formulario_estudiante.apellido.get().strip(),
                'Grado': self.formulario_estudiante.grado.get()
            }
            
            campos_vacios = [campo for campo, valor in campos_obligatorios.items() if not valor]
            
            if campos_vacios:
                messagebox.showerror(
                    "Error", 
                    f"Por favor complete los siguientes campos obligatorios:\n- {'\n- '.join(campos_vacios)}"
                )
                return

            # Crear estudiante con los datos del formulario
            estudiante = Estudiante(
                dni=campos_obligatorios['DNI'],
                nombre=campos_obligatorios['Nombre'],
                apellido=campos_obligatorios['Apellido'],
                fecha_nacimiento=self.formulario_estudiante.fecha_nacimiento.get().strip(),
                genero=self.formulario_estudiante.genero.get(),
                direccion=self.formulario_estudiante.direccion.get().strip(),
                telefono_emergencia=self.formulario_estudiante.telefono_emergencia.get().strip(),
                grado=campos_obligatorios['Grado'],
                doble_jornada=self.formulario_estudiante.var_doble_jornada.get()
            )

            if self.formulario_estudiante.modo_edicion:
                # Actualizar estudiante existente
                if RepositorioEstudiantes.actualizar_estudiante(estudiante):
                    # Actualizar tutores
                    tutores = self.formulario_tutor.obtener_datos_tutor(self.estudiante_actual.id)
                    exito = True
                    for tutor in tutores:
                        if not RepositorioTutores.actualizar_tutor(tutor):
                            exito = False
                            break

                    if exito:
                        messagebox.showinfo("Éxito", "Estudiante y tutores actualizados correctamente")
                        self.limpiar_todos_formularios()
                        self.lista_estudiantes.actualizar_lista_estudiantes()
                    else:
                        messagebox.showerror("Error", "Error al actualizar los tutores")
                else:
                    messagebox.showerror("Error", "Error al actualizar el estudiante")
            else:
                # Verificar si el DNI ya existe
                if RepositorioEstudiantes.obtener_por_dni(estudiante.dni, incluir_inactivos=True):
                    messagebox.showerror("Error", "El DNI ya está registrado")
                    return

                # Guardar nuevo estudiante
                if RepositorioEstudiantes.guardar_estudiante(estudiante):
                    # Guardar tutores
                    tutores = self.formulario_tutor.obtener_datos_tutor(estudiante.id)
                    exito = True
                    for tutor in tutores:
                        if not RepositorioTutores.guardar_tutor(tutor):
                            exito = False
                            break

                    if exito:
                        messagebox.showinfo("Éxito", "Estudiante y tutores registrados correctamente")
                        self.limpiar_todos_formularios()
                        self.lista_estudiantes.actualizar_lista_estudiantes()
                    else:
                        messagebox.showerror("Error", "Error al registrar los tutores")
                else:
                    messagebox.showerror("Error", "Error al registrar el estudiante")

        except Exception as e:
            messagebox.showerror("Error", f"Error en el registro: {str(e)}")

    def dar_baja_estudiante(self):
        """Da de baja a un estudiante"""
        if self.estudiante_actual and messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de dar de baja al estudiante?"
        ):
            if RepositorioEstudiantes.dar_de_baja_estudiante(self.estudiante_actual.dni):
                messagebox.showinfo("Éxito", "Estudiante dado de baja correctamente")
                self.limpiar_todos_formularios()
                self.lista_estudiantes.actualizar_lista_estudiantes()
            else:
                messagebox.showerror("Error", "Error al dar de baja al estudiante")

    def reactivar_estudiante(self):
        """Reactiva un estudiante dado de baja"""
        if self.estudiante_actual and messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de reactivar al estudiante?"
        ):
            if RepositorioEstudiantes.reactivar_estudiante(self.estudiante_actual.dni):
                messagebox.showinfo("Éxito", "Estudiante reactivado correctamente")
                self.limpiar_todos_formularios()
                self.lista_estudiantes.actualizar_lista_estudiantes()
            else:
                messagebox.showerror("Error", "Error al reactivar al estudiante")