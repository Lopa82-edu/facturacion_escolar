import customtkinter as ctk
from tkinter import ttk
from utilidades.niveles_grados import NivelesGrados
from modelos.item_precio import ItemPrecio

class FormularioPrecio(ctk.CTkFrame):
    def __init__(self, padre):
        super().__init__(padre)
        self.item_actual = None
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Título
        titulo = ctk.CTkLabel(self, text="Precios por Nivel", font=("Arial", 16, "bold"))
        titulo.pack(pady=5)

        # Marco para selección de nivel
        marco_nivel = ctk.CTkFrame(self)
        marco_nivel.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(marco_nivel, text="Nivel:").pack(side="left", padx=5)
        self.combo_nivel = ctk.CTkComboBox(
            marco_nivel,
            values=NivelesGrados.obtener_niveles(),
            command=self._al_cambiar_nivel
        )
        self.combo_nivel.pack(side="left", padx=5)
        self.combo_nivel.set(NivelesGrados.obtener_niveles()[0])

        # Marco para nuevo item
        marco_item = ctk.CTkFrame(self)
        marco_item.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(marco_item, text="Concepto:").pack(side="left", padx=5)
        self.entrada_nombre = ctk.CTkEntry(marco_item, width=150)
        self.entrada_nombre.pack(side="left", padx=5)
        
        ctk.CTkLabel(marco_item, text="Monto:").pack(side="left", padx=5)
        self.entrada_monto = ctk.CTkEntry(marco_item, width=100)
        self.entrada_monto.pack(side="left", padx=5)

        # Agregar casilla de doble jornada
        self.var_doble_jornada = ctk.BooleanVar(value=False)
        self.casilla_doble_jornada = ctk.CTkCheckBox(
            marco_item,
            text="Solo Doble Jornada",
            variable=self.var_doble_jornada
        )
        self.casilla_doble_jornada.pack(side="left", padx=5)

        # Agregar casilla de mantenimiento
        self.var_mantenimiento = ctk.BooleanVar(value=False)
        self.casilla_mantenimiento = ctk.CTkCheckBox(
            marco_item,
            text="Aplica a Mantenimiento",
            variable=self.var_mantenimiento
        )
        self.casilla_mantenimiento.pack(side="left", padx=5)
        
        # Botones
        marco_botones = ctk.CTkFrame(self)
        marco_botones.pack(fill="x", padx=5, pady=5)
        
        self.boton_guardar = ctk.CTkButton(
            marco_botones,
            text="Guardar",
            width=80
        )
        self.boton_guardar.pack(side="left", padx=2)
        
        self.boton_limpiar = ctk.CTkButton(
            marco_botones,
            text="Limpiar",
            width=80
        )
        self.boton_limpiar.pack(side="left", padx=2)
        
        self.boton_dar_baja = ctk.CTkButton(
            marco_botones,
            text="Dar de Baja",
            fg_color="red",
            state="disabled",
            width=80
        )
        self.boton_dar_baja.pack(side="left", padx=2)
        
        self.boton_reactivar = ctk.CTkButton(
            marco_botones,
            text="Reactivar",
            fg_color="green",
            state="disabled",
            width=80
        )
        self.boton_reactivar.pack(side="left", padx=2)

        # Configurar tabla
        self.configurar_tabla_items()

    def configurar_tabla_items(self):
        marco_tabla = ttk.Frame(self)
        marco_tabla.pack(fill="both", expand=True, padx=5, pady=5)

        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=("Concepto", "Monto", "Estado", "ID"),
            show="headings",
            height=10
        )

        self.tabla.heading("Concepto", text="Concepto")
        self.tabla.heading("Monto", text="Monto")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading("ID", text="ID")

        self.tabla.column("Concepto", width=200)
        self.tabla.column("Monto", width=100)
        self.tabla.column("Estado", width=100)
        self.tabla.column("ID", width=0, stretch=False)

        barra_desplazamiento = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra_desplazamiento.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        barra_desplazamiento.pack(side="right", fill="y")

    def _al_cambiar_nivel(self, nivel):
        """Manejar cambio de nivel"""
        # Mostrar/ocultar casilla de doble jornada según nivel
        if nivel in ["Inicial", "Primario"]:
            self.casilla_doble_jornada.pack(side="left", padx=5)
        else:
            self.casilla_doble_jornada.pack_forget()
            self.var_doble_jornada.set(False)
        
        self.actualizar_tabla_items()
        self.limpiar_formulario()

    def insertar_item(self, nombre, monto, estado, id_item, solo_doble_jornada, item_mantenimiento):
        """Insertar un item en la tabla"""
        etiquetas = []
        if solo_doble_jornada:
            etiquetas.append("Doble Jornada")
        if item_mantenimiento:
            etiquetas.append("Mantenimiento")
            
        nombre_mostrar = f"{nombre} ({', '.join(etiquetas)})" if etiquetas else nombre
        self.tabla.insert("", "end", values=(nombre_mostrar, monto, estado, id_item))

    def limpiar_formulario(self):
        """Limpiar el formulario"""
        self.entrada_nombre.delete(0, 'end')
        self.entrada_monto.delete(0, 'end')
        self.var_doble_jornada.set(False)
        self.var_mantenimiento.set(False)
        self.item_actual = None
        self.boton_dar_baja.configure(state="disabled")
        self.boton_reactivar.configure(state="disabled")

    def limpiar_tabla(self):
        """Limpiar la tabla"""
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def actualizar_tabla_items(self):
        """Actualizar la tabla de items"""
        pass  # Esto será implementado en PestañaPrecios