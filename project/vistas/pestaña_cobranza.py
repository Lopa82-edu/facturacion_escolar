import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
from repositorios.repositorio_pagos import RepositorioPagos
from utilidades.generador_pdf import GeneradorPDF
from utilidades.utilidades_meses import UtilidadesMeses
from utilidades.niveles_grados import NivelesGrados
from repositorios.repositorio_estudiantes import RepositorioEstudiantes
from repositorios.repositorio_cupones_pago import RepositorioCuponesPago
from modelos.pago import Pago
import os
import platform
import subprocess

class PestañaCobranza(ctk.CTkFrame):
    def __init__(self, padre):
        super().__init__(padre)
        self.cupon_actual = None
        self.estudiante_actual = None
        self.configurar_interfaz()
        self.establecer_filtros_actuales()
        self.configurar_estilos_tabla()

    def configurar_estilos_tabla(self):
        """Configura estilos personalizados para la tabla"""
        estilo = ttk.Style()
        estilo.configure("Pagado.Treeview.Row", background="#90EE90")  # Verde claro para filas pagadas

    def configurar_interfaz(self):
        # Marco de control principal
        marco_control = ctk.CTkFrame(self)
        marco_control.pack(fill="x", padx=5, pady=5)

        # Marco de búsqueda de estudiantes
        marco_busqueda = ctk.CTkFrame(marco_control)
        marco_busqueda.pack(side="left", padx=5)
        
        # Búsqueda por DNI
        ctk.CTkLabel(marco_busqueda, text="DNI:").pack(side="left", padx=5)
        self.entrada_dni = ctk.CTkEntry(marco_busqueda, width=100)
        self.entrada_dni.pack(side="left", padx=5)
        
        # Botón buscar por DNI
        self.boton_buscar_dni = ctk.CTkButton(
            marco_busqueda,
            text="Buscar por DNI",
            command=self._buscar_por_dni
        )
        self.boton_buscar_dni.pack(side="left", padx=5)
        
        # Búsqueda por apellido
        ctk.CTkLabel(marco_busqueda, text="Apellido:").pack(side="left", padx=5)
        self.entrada_apellido = ctk.CTkEntry(marco_busqueda, width=150)
        self.entrada_apellido.pack(side="left", padx=5)
        
        # Botón buscar por apellido
        self.boton_buscar_apellido = ctk.CTkButton(
            marco_busqueda,
            text="Buscar por Apellido",
            command=lambda: self._al_cambiar_apellido(None)
        )
        self.boton_buscar_apellido.pack(side="left", padx=5)

        # Botón limpiar búsqueda
        self.boton_limpiar = ctk.CTkButton(
            marco_busqueda,
            text="Limpiar Búsqueda",
            command=self._limpiar_busqueda
        )
        self.boton_limpiar.pack(side="left", padx=5)

        # Marco de filtros
        marco_filtros = ctk.CTkFrame(marco_control)
        marco_filtros.pack(side="left", padx=5)

        # Selección de nivel
        ctk.CTkLabel(marco_filtros, text="Nivel:").pack(side="left", padx=5)
        self.combo_nivel = ctk.CTkComboBox(
            marco_filtros,
            values=[""] + NivelesGrados.obtener_niveles(),
            command=self._al_cambiar_nivel,
            width=120
        )
        self.combo_nivel.pack(side="left", padx=5)

        # Selección de grado
        ctk.CTkLabel(marco_filtros, text="Grado:").pack(side="left", padx=5)
        self.combo_grado = ctk.CTkComboBox(
            marco_filtros,
            values=[""],
            command=self._al_cambiar_filtro,
            width=120
        )
        self.combo_grado.pack(side="left", padx=5)

        # Selección de mes
        ctk.CTkLabel(marco_filtros, text="Mes:").pack(side="left", padx=5)
        self.combo_mes = ctk.CTkComboBox(
            marco_filtros,
            values=[""] + UtilidadesMeses.obtener_meses(),
            command=self._al_cambiar_filtro,
            width=120
        )
        self.combo_mes.pack(side="left", padx=5)

        # Marco de información del estudiante
        self.marco_info_estudiante = ctk.CTkFrame(self)
        self.marco_info_estudiante.pack(fill="x", padx=5, pady=5)
        self.etiqueta_info_estudiante = ctk.CTkLabel(
            self.marco_info_estudiante,
            text="",
            font=("Arial", 12, "bold")
        )
        self.etiqueta_info_estudiante.pack(pady=5)

        # Marco de resultados de búsqueda
        self.marco_resultados_busqueda = ctk.CTkFrame(self)
        self.lista_resultados_busqueda = None

        # Marco de cupones
        self.marco_cupones = ctk.CTkFrame(self)
        self.marco_cupones.pack(fill="both", expand=True, padx=5, pady=5)

        # Configurar tabla
        self.configurar_tabla()

        # Marco de botones
        marco_botones = ctk.CTkFrame(self)
        marco_botones.pack(fill="x", padx=5, pady=5)

        # Botón de pago
        self.boton_pagar = ctk.CTkButton(
            marco_botones,
            text="Registrar Pago",
            command=self._procesar_pago,
            state="disabled",
            font=("Arial", 16)
        )
        self.boton_pagar.pack(side="left", padx=5)

        # Botón de anular pago
        self.boton_anular_pago = ctk.CTkButton(
            marco_botones,
            text="Anular Pago",
            command=self._anular_pago,
            state="disabled",
            fg_color="red",
            font=("Arial", 16)
        )
        self.boton_anular_pago.pack(side="left", padx=5)

        # Vincular eventos
        self.entrada_dni.bind('<Return>', lambda e: self._buscar_por_dni())
        self.entrada_apellido.bind('<KeyRelease>', self._al_cambiar_apellido)

    def configurar_tabla(self):
        """Configura la tabla de cupones"""
        columnas = (
            "ID", "Mes", "Año", "Nivel", "Grado", 
            "Monto", "Cargo Especial", "Estado", "N° Recibo"
        )
        
        self.tabla = ttk.Treeview(
            self.marco_cupones,
            columns=columnas,
            show="headings",
            height=10
        )

        # Configurar columnas
        for col in columnas:
            self.tabla.heading(col, text=col)
            ancho = 100
            if col == "ID":
                ancho = 0  # Ocultar columna ID
            elif col in ["Mes", "Año", "Nivel", "Grado", "Estado"]:
                ancho = 100
            elif col in ["Monto", "N° Recibo"]:
                ancho = 120
            elif col == "Cargo Especial":
                ancho = 150
            self.tabla.column(col, width=ancho)

        # Agregar barra de desplazamiento
        barra_desplazamiento = ttk.Scrollbar(
            self.marco_cupones,
            orient="vertical",
            command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=barra_desplazamiento.set)

        # Empaquetar elementos
        self.tabla.pack(side="left", fill="both", expand=True)
        barra_desplazamiento.pack(side="right", fill="y")

        # Vincular evento de selección
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_cupon)

    def establecer_filtros_actuales(self):
        """Establece el mes actual en los filtros"""
        mes_actual = datetime.now().month
        if 3 <= mes_actual <= 12:  # Meses del año escolar
            nombre_mes = UtilidadesMeses.obtener_nombre_mes(mes_actual)
            if nombre_mes in UtilidadesMeses.obtener_meses():
                self.combo_mes.set(nombre_mes)

    def _limpiar_busqueda(self):
        """Limpia los campos de búsqueda y reinicia el estado"""
        self.entrada_dni.delete(0, 'end')
        self.entrada_apellido.delete(0, 'end')
        self.etiqueta_info_estudiante.configure(text="")
        self.estudiante_actual = None
        self.combo_nivel.set("")
        self.combo_grado.set("")
        self._ocultar_resultados_busqueda()
        self._actualizar_tabla_cupones([])

    def _buscar_por_dni(self):
        """Busca estudiante por DNI"""
        dni = self.entrada_dni.get().strip()
        if dni:
            estudiante = RepositorioEstudiantes.obtener_por_dni(dni)
            if estudiante:
                self._seleccionar_estudiante(estudiante)
            else:
                messagebox.showinfo("Aviso", "No se encontró ningún estudiante con ese DNI")

    def _al_cambiar_apellido(self, evento):
        """Maneja los cambios en la entrada de búsqueda por apellido"""
        apellido = self.entrada_apellido.get().strip()
        if len(apellido) >= 3:  # Buscar después de 3 caracteres
            estudiantes = RepositorioEstudiantes.buscar_por_apellido(apellido)
            self._mostrar_resultados_busqueda(estudiantes)
        else:
            self._ocultar_resultados_busqueda()

    def _mostrar_resultados_busqueda(self, estudiantes):
        """Muestra el desplegable de resultados de búsqueda"""
        if self.lista_resultados_busqueda:
            self.lista_resultados_busqueda.destroy()

        if estudiantes:
            # Crear marco de lista
            self.lista_resultados_busqueda = ctk.CTkFrame(self.marco_resultados_busqueda)
            self.marco_resultados_busqueda.pack(fill="x", padx=5)
            self.lista_resultados_busqueda.pack(fill="x")

            # Agregar botones de estudiantes
            for estudiante in estudiantes:
                btn = ctk.CTkButton(
                    self.lista_resultados_busqueda,
                    text=f"{estudiante.apellido}, {estudiante.nombre} - {estudiante.dni}",
                    command=lambda e=estudiante: self._seleccionar_estudiante(e),
                    fg_color="transparent",
                    text_color="black",
                    hover_color="gray75"
                )
                btn.pack(fill="x", padx=2, pady=1)

    def _ocultar_resultados_busqueda(self):
        """Oculta el desplegable de resultados de búsqueda"""
        if self.lista_resultados_busqueda:
            self.lista_resultados_busqueda.destroy()
            self.lista_resultados_busqueda = None
        self.marco_resultados_busqueda.pack_forget()

    def _seleccionar_estudiante(self, estudiante):
        """Maneja la selección de un estudiante"""
        self.estudiante_actual = estudiante
        self.entrada_dni.delete(0, 'end')
        self.entrada_dni.insert(0, estudiante.dni)
        self.entrada_apellido.delete(0, 'end')
        self.entrada_apellido.insert(0, estudiante.apellido)
        self._ocultar_resultados_busqueda()
        
        # Actualizar información del estudiante y filtros
        self.etiqueta_info_estudiante.configure(
            text=f"Estudiante: {estudiante.apellido}, {estudiante.nombre} - DNI: {estudiante.dni} - Grado: {estudiante.grado}"
        )
        
        # Establecer filtros basados en el grado del estudiante
        for nivel in NivelesGrados.obtener_niveles():
            if estudiante.grado in NivelesGrados.obtener_grados_por_nivel(nivel):
                self.combo_nivel.set(nivel)
                self._al_cambiar_nivel(nivel)  # Esto actualizará los grados
                self.combo_grado.set(estudiante.grado)
                break
        
        # Buscar cupones del estudiante
        cupones = RepositorioCuponesPago.obtener_cupones_por_dni_estudiante(estudiante.dni)
        self._actualizar_tabla_cupones(cupones)

    def _al_cambiar_nivel(self, _):
        """Maneja el cambio de nivel"""
        nivel = self.combo_nivel.get()
        if nivel:
            grados = NivelesGrados.obtener_grados_por_nivel(nivel)
            self.combo_grado.configure(values=[""] + grados)
            self.combo_grado.set("")
        else:
            self.combo_grado.configure(values=[""])
            self.combo_grado.set("")
        self._al_cambiar_filtro(None)

    def _al_cambiar_filtro(self, _):
        """Maneja cambios en los filtros"""
        # Si hay un estudiante seleccionado, mostrar solo sus cupones
        if self.estudiante_actual:
            cupones = RepositorioCuponesPago.obtener_cupones_por_dni_estudiante(self.estudiante_actual.dni)
            self._actualizar_tabla_cupones(cupones)
            return

        # Si no hay estudiante seleccionado, filtrar por nivel, grado y mes
        nivel = self.combo_nivel.get()
        nombre_mes = self.combo_mes.get()
        
        if nivel and nombre_mes:
            numero_mes = UtilidadesMeses.obtener_numero_mes(nombre_mes)
            año = datetime.now().year
            cupones = RepositorioCuponesPago.obtener_cupones_por_filtros(nivel, numero_mes, año)
            self._actualizar_tabla_cupones(cupones)

    def _actualizar_tabla_cupones(self, cupones):
        """Actualiza la tabla con los cupones proporcionados"""
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Insertar cupones
        for cupon in cupones:
            # Obtener información de pago si existe
            pago = RepositorioPagos.obtener_pago_por_id_cupon(cupon.id)
            numero_recibo = pago.numero_recibo if pago else ""

            valores = (
                cupon.id,
                UtilidadesMeses.obtener_nombre_mes(cupon.mes),
                cupon.año_academico,
                cupon.nivel,
                cupon.grado,
                f"${cupon.monto_total:.2f}",
                "Sí (50%)" if cupon.es_cargo_especial else "No",
                "Pagado" if cupon.estado == "paid" else "Activo" if cupon.estado == "active" else "Anulado",
                numero_recibo
            )
            
            # Insertar con etiqueta si está pagado
            etiquetas = ("pagado",) if cupon.estado == "paid" else ()
            self.tabla.insert("", "end", values=valores, tags=etiquetas)

    def _al_seleccionar_cupon(self, evento):
        """Maneja la selección de un cupón"""
        seleccion = self.tabla.selection()
        if seleccion:
            # Obtener valores del cupón seleccionado
            item = self.tabla.item(seleccion[0])
            valores = item["values"]
            estado = valores[7]  # Índice actualizado
            
            # Habilitar/deshabilitar botones según estado
            if estado == "Activo":
                self.boton_pagar.configure(state="normal")
                self.boton_anular_pago.configure(state="disabled")
                self.cupon_actual = self._obtener_cupon_por_id(valores[0])  # ID del cupón
            elif estado == "Pagado":
                self.boton_pagar.configure(state="disabled")
                self.boton_anular_pago.configure(state="normal")
                self.cupon_actual = self._obtener_cupon_por_id(valores[0])  # ID del cupón
            else:
                self.boton_pagar.configure(state="disabled")
                self.boton_anular_pago.configure(state="disabled")
                self.cupon_actual = None
        else:
            self.boton_pagar.configure(state="disabled")
            self.boton_anular_pago.configure(state="disabled")
            self.cupon_actual = None

    def _obtener_cupon_por_id(self, id_cupon):
        """Obtiene un cupón por su ID"""
        if self.estudiante_actual:
            cupones = RepositorioCuponesPago.obtener_cupones_por_dni_estudiante(self.estudiante_actual.dni)
        else:
            nombre_mes = self.combo_mes.get()
            numero_mes = UtilidadesMeses.obtener_numero_mes(nombre_mes)
            año = datetime.now().year
            nivel = self.combo_nivel.get()
            cupones = RepositorioCuponesPago.obtener_cupones_por_filtros(nivel, numero_mes, año)
            
        return next((c for c in cupones if c.id == id_cupon), None)

    def _procesar_pago(self):
        """Procesa el pago del cupón seleccionado"""
        if not self.cupon_actual:
            messagebox.showwarning("Aviso", "Por favor seleccione un cupón para pagar")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de registrar el pago?"):
            # Crear pago
            pago = Pago(id_cupon=self.cupon_actual.id)
            
            # Guardar pago
            if RepositorioPagos.guardar_pago(pago):
                # Obtener información del estudiante
                estudiante = RepositorioEstudiantes.obtener_por_dni(self.cupon_actual.dni_estudiante)
                
                # Generar PDF
                ruta_pdf = GeneradorPDF.generar_recibo(pago, estudiante, self.cupon_actual)
                
                if ruta_pdf:
                    messagebox.showinfo(
                        "Éxito", 
                        f"Pago registrado correctamente\nRecibo N°: {pago.numero_recibo}\n"
                        f"El comprobante se guardó en: {ruta_pdf}"
                    )
                    
                    # Abrir PDF
                    try:
                        if platform.system() == 'Darwin':  # macOS
                            subprocess.run(['open', ruta_pdf])
                        elif platform.system() == 'Windows':
                            os.startfile(ruta_pdf)
                        else:  # Linux
                            subprocess.run(['xdg-open', ruta_pdf])
                    except:
                        messagebox.showinfo(
                            "Información",
                            "El PDF se generó correctamente pero no se pudo abrir automáticamente.\n"
                            f"Puede encontrarlo en: {ruta_pdf}"
                        )
                    
                    # Actualizar lista de cupones
                    if self.estudiante_actual:
                        cupones = RepositorioCuponesPago.obtener_cupones_por_dni_estudiante(self.estudiante_actual.dni)
                    else:
                        nombre_mes = self.combo_mes.get()
                        numero_mes = UtilidadesMeses.obtener_numero_mes(nombre_mes)
                        año = datetime.now().year
                        nivel = self.combo_nivel.get()
                        cupones = RepositorioCuponesPago.obtener_cupones_por_filtros(nivel, numero_mes, año)
                    self._actualizar_tabla_cupones(cupones)
                else:
                    messagebox.showerror(
                        "Error",
                        "El pago se registró pero hubo un error al generar el PDF"
                    )
            else:
                messagebox.showerror("Error", "Error al registrar el pago")

    def _anular_pago(self):
        """Anula el pago del cupón seleccionado"""
        if not self.cupon_actual:
            messagebox.showwarning("Aviso", "Por favor seleccione un cupón para anular el pago")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de anular el pago? Esta acción no se puede deshacer."):
            if RepositorioPagos.anular_pago(self.cupon_actual.id):
                messagebox.showinfo("Éxito", "Pago anulado correctamente")
                # Actualizar lista de cupones
                if self.estudiante_actual:
                    cupones = RepositorioCuponesPago.obtener_cupones_por_dni_estudiante(self.estudiante_actual.dni)
                else:
                    nombre_mes = self.combo_mes.get()
                    numero_mes = UtilidadesMeses.obtener_numero_mes(nombre_mes)
                    año = datetime.now().year
                    nivel = self.combo_nivel.get()
                    cupones = RepositorioCuponesPago.obtener_cupones_por_filtros(nivel, numero_mes, año)
                self._actualizar_tabla_cupones(cupones)
            else:
                messagebox.showerror("Error", "Error al anular el pago")