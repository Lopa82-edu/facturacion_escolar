import customtkinter as ctk
from tkinter import messagebox
from vistas.componentes.marco_generacion_cupones import MarcoGeneracionCupones
from vistas.componentes.marco_lista_cupones import MarcoListaCupones
from repositorios.repositorio_cupones_pago import RepositorioCuponesPago

class PestañaPagos(ctk.CTkFrame):
    def __init__(self, padre):
        super().__init__(padre)
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Marco para generación de cupones (parte superior)
        self.marco_generacion = MarcoGeneracionCupones(
            self,
            al_actualizar_cupones=self.actualizar_lista_cupones
        )
        self.marco_generacion.pack(fill="x", padx=10, pady=5)

        # Marco para lista de cupones (parte inferior)
        self.marco_lista = MarcoListaCupones(self)
        self.marco_lista.pack(fill="both", expand=True, padx=10, pady=5)

        # Configurar eventos después de crear los marcos
        self.vincular_eventos()

    def vincular_eventos(self):
        self.marco_lista.boton_anular.configure(command=self.anular_cupon)
        self.marco_lista.boton_reactivar.configure(command=self.reactivar_cupon)
        self.marco_lista.boton_eliminar.configure(command=self.eliminar_cupon)
        self.marco_lista.tabla.bind("<<TreeviewSelect>>", self.marco_lista.al_seleccionar)

    def actualizar_lista_cupones(self, cupones):
        """Actualiza la lista de cupones"""
        if cupones is not None:
            self.marco_lista.actualizar_lista(cupones)

    def anular_cupon(self):
        """Anula el cupón seleccionado"""
        seleccion = self.marco_lista.tabla.selection()
        if seleccion:
            item = self.marco_lista.tabla.item(seleccion[0])
            id_cupon = item["values"][0]
            
            if messagebox.askyesno("Confirmar", "¿Está seguro de anular este cupón?"):
                if RepositorioCuponesPago.anular_cupon(id_cupon):
                    messagebox.showinfo("Éxito", "Cupón anulado correctamente")
                    # Actualizar lista
                    self.marco_generacion._al_cambiar_filtro(None)
                else:
                    messagebox.showerror("Error", "Error al anular el cupón")

    def reactivar_cupon(self):
        """Reactiva un cupón anulado"""
        seleccion = self.marco_lista.tabla.selection()
        if seleccion:
            item = self.marco_lista.tabla.item(seleccion[0])
            id_cupon = item["values"][0]
            
            if messagebox.askyesno("Confirmar", "¿Está seguro de reactivar este cupón?"):
                if RepositorioCuponesPago.reactivar_cupon(id_cupon):
                    messagebox.showinfo("Éxito", "Cupón reactivado correctamente")
                    # Actualizar lista
                    self.marco_generacion._al_cambiar_filtro(None)
                else:
                    messagebox.showerror("Error", "Error al reactivar el cupón")

    def eliminar_cupon(self):
        """Elimina un cupón permanentemente"""
        seleccion = self.marco_lista.tabla.selection()
        if seleccion:
            item = self.marco_lista.tabla.item(seleccion[0])
            id_cupon = item["values"][0]
            
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cupón? Esta acción no se puede deshacer."):
                if RepositorioCuponesPago.eliminar_cupon(id_cupon):
                    messagebox.showinfo("Éxito", "Cupón eliminado correctamente")
                    # Actualizar lista
                    self.marco_generacion._al_cambiar_filtro(None)
                else:
                    messagebox.showerror("Error", "Error al eliminar el cupón")