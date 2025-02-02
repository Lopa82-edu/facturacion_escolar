import customtkinter as ctk
from tkinter import messagebox
from modelos.item_precio import ItemPrecio
from repositorios.repositorio_precios import RepositorioPrecios
from vistas.componentes.formulario_precio import FormularioPrecio

class PestañaPrecios(ctk.CTkFrame):
    def __init__(self, padre):
        super().__init__(padre)
        self.configurar_interfaz()
        self.vincular_eventos()
        self.actualizar_tabla_items()

    def configurar_interfaz(self):
        self.formulario_precio = FormularioPrecio(self)
        self.formulario_precio.pack(expand=True, fill="both", padx=10, pady=10)

    def vincular_eventos(self):
        # Vincular directamente al comando del combo de nivel
        self.formulario_precio.combo_nivel.configure(command=self._al_cambiar_nivel)
        self.formulario_precio.boton_guardar.configure(command=self.guardar_item_precio)
        self.formulario_precio.boton_limpiar.configure(command=self.formulario_precio.limpiar_formulario)
        self.formulario_precio.boton_dar_baja.configure(command=self.dar_baja_item_precio)
        self.formulario_precio.boton_reactivar.configure(command=self.reactivar_item_precio)
        self.formulario_precio.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar_item)

    def _al_cambiar_nivel(self, nivel):
        self.actualizar_tabla_items()
        self.formulario_precio.limpiar_formulario()

    def guardar_item_precio(self):
        try:
            nombre = self.formulario_precio.entrada_nombre.get().strip()
            monto_str = self.formulario_precio.entrada_monto.get().strip()
            nivel = self.formulario_precio.combo_nivel.get()
            solo_doble_jornada = self.formulario_precio.var_doble_jornada.get()
            item_mantenimiento = self.formulario_precio.var_mantenimiento.get()

            if not all([nombre, monto_str, nivel]):
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return

            try:
                monto = float(monto_str)
            except ValueError:
                messagebox.showerror("Error", "El monto debe ser un número válido")
                return

            item = ItemPrecio(
                nivel=nivel,
                nombre=nombre,
                monto=monto,
                id=self.formulario_precio.item_actual.id if self.formulario_precio.item_actual else None,
                solo_doble_jornada=solo_doble_jornada,
                item_mantenimiento=item_mantenimiento
            )

            if self.formulario_precio.item_actual:
                exito = RepositorioPrecios.actualizar_item_precio(item)
                mensaje = "Item actualizado correctamente"
            else:
                exito = RepositorioPrecios.guardar_item_precio(item)
                mensaje = "Item guardado correctamente"

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.formulario_precio.limpiar_formulario()
                self.actualizar_tabla_items()
            else:
                messagebox.showerror("Error", "Error al guardar el item")

        except Exception as e:
            messagebox.showerror("Error", f"Error en el registro: {str(e)}")

    def dar_baja_item_precio(self):
        if self.formulario_precio.item_actual and messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de dar de baja este item?"
        ):
            if RepositorioPrecios.dar_de_baja_item_precio(self.formulario_precio.item_actual.id):
                messagebox.showinfo("Éxito", "Item dado de baja correctamente")
                self.formulario_precio.limpiar_formulario()
                self.actualizar_tabla_items()
            else:
                messagebox.showerror("Error", "Error al dar de baja el item")

    def reactivar_item_precio(self):
        if self.formulario_precio.item_actual and messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de reactivar este item?"
        ):
            if RepositorioPrecios.reactivar_item_precio(self.formulario_precio.item_actual.id):
                messagebox.showinfo("Éxito", "Item reactivado correctamente")
                self.formulario_precio.limpiar_formulario()
                self.actualizar_tabla_items()
            else:
                messagebox.showerror("Error", "Error al reactivar el item")

    def al_seleccionar_item(self, evento):
        seleccion = self.formulario_precio.tabla.selection()
        if seleccion:
            item = self.formulario_precio.tabla.item(seleccion[0])
            id_item = item["values"][3]  # ID oculto
            items = RepositorioPrecios.obtener_items_por_nivel(
                self.formulario_precio.combo_nivel.get(),
                incluir_inactivos=True
            )
            item_seleccionado = next((i for i in items if i.id == id_item), None)
            
            if item_seleccionado:
                self.formulario_precio.item_actual = item_seleccionado
                self.formulario_precio.entrada_nombre.delete(0, 'end')
                self.formulario_precio.entrada_nombre.insert(0, item_seleccionado.nombre)
                self.formulario_precio.entrada_monto.delete(0, 'end')
                self.formulario_precio.entrada_monto.insert(0, str(item_seleccionado.monto))
                self.formulario_precio.var_doble_jornada.set(item_seleccionado.solo_doble_jornada)
                self.formulario_precio.var_mantenimiento.set(item_seleccionado.item_mantenimiento)
                
                if item_seleccionado.activo:
                    self.formulario_precio.boton_dar_baja.configure(state="normal")
                    self.formulario_precio.boton_reactivar.configure(state="disabled")
                else:
                    self.formulario_precio.boton_dar_baja.configure(state="disabled")
                    self.formulario_precio.boton_reactivar.configure(state="normal")

    def actualizar_tabla_items(self):
        nivel = self.formulario_precio.combo_nivel.get()
        items = RepositorioPrecios.obtener_items_por_nivel(nivel, incluir_inactivos=True)
        
        self.formulario_precio.limpiar_tabla()
        
        total = 0
        for item in items:
            if item.activo:
                total += item.monto
            
            self.formulario_precio.insertar_item(
                item.nombre,
                f"${item.monto:.2f}",
                "Activo" if item.activo else "Inactivo",
                item.id,
                item.solo_doble_jornada,
                item.item_mantenimiento
            )