import tkinter.messagebox as messagebox
from repositorios.repositorio_estudiantes import RepositorioEstudiantes
from repositorios.repositorio_tutores import RepositorioTutores

class ManejadorBusqueda:
    def __init__(self, pestaña_registro):
        self.pestaña_registro = pestaña_registro

    def manejar_resultado_busqueda(self, termino_busqueda, es_dni=True, incluir_inactivos=False):
        if es_dni:
            self._manejar_busqueda_dni(termino_busqueda, incluir_inactivos)
        else:
            self._manejar_busqueda_apellido(termino_busqueda, incluir_inactivos)

    def _manejar_busqueda_dni(self, dni, incluir_inactivos):
        estudiante = RepositorioEstudiantes.obtener_por_dni(dni, incluir_inactivos)
        if estudiante:
            self.pestaña_registro.estudiante_actual = estudiante
            self.pestaña_registro.formulario_estudiante.establecer_datos_estudiante(estudiante)
            self.pestaña_registro.formulario_estudiante.entrar_modo_edicion()
            
            # Configurar botones según estado del estudiante
            if estudiante.activo:
                self.pestaña_registro.formulario_estudiante.boton_dar_baja.configure(state="normal")
                self.pestaña_registro.formulario_estudiante.boton_reactivar.configure(state="disabled")
                self.pestaña_registro.formulario_estudiante.boton_guardar.configure(state="normal")
            else:
                self.pestaña_registro.formulario_estudiante.boton_dar_baja.configure(state="disabled")
                self.pestaña_registro.formulario_estudiante.boton_reactivar.configure(state="normal")
                self.pestaña_registro.formulario_estudiante.boton_guardar.configure(state="disabled")
                messagebox.showinfo("Aviso", "Este estudiante está dado de baja")
            
            # Cargar datos de los tutores
            tutores = RepositorioTutores.obtener_tutores_por_id_estudiante(estudiante.id)
            if tutores:
                self.pestaña_registro.formulario_tutor.establecer_datos_tutor(tutores)
            messagebox.showinfo("Éxito", "Estudiante encontrado")
        else:
            messagebox.showinfo("Aviso", "DNI disponible para registro")

    def _manejar_busqueda_apellido(self, apellido, incluir_inactivos):
        estudiantes = RepositorioEstudiantes.buscar_por_apellido(apellido, incluir_inactivos)
        if estudiantes:
            self.pestaña_registro.marco_busqueda.mostrar_resultados(estudiantes)
        else:
            messagebox.showinfo("Aviso", "No se encontraron estudiantes")