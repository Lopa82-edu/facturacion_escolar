import customtkinter as ctk
from tkinter import ttk
from utilidades.utilidades_meses import UtilidadesMeses

class MarcoListaCupones(ctk.CTkFrame):
    def __init__(self, padre):
        super().__init__(padre)
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Título
        titulo = ctk.CTkLabel(self, text="Lista de Cupones", font=("Arial", 16, "bold"))
        titulo.pack(pady=5)

        # Marco para la tabla
        marco_tabla = ttk.Frame(self)
        marco_tabla.pack(fill="both", expand=True, padx=5, pady=5)

        # Crear Treeview
        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=(
                "ID", "Estudiante", "DNI", "Grado",
                "Mes", "Monto", "Cargo Especial", "Estado"
            ),
            show="headings"
        )

        # Configurar columnas
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Estudiante", text="Estudiante")
        self.tabla.heading("DNI", text="DNI")
        self.tabla.heading("Grado", text="Grado")
        self.tabla.heading("Mes", text="Mes")
        self.tabla.heading("Monto", text="Monto")
        self.tabla.heading("Cargo Especial", text="Cargo Especial")
        self.tabla.heading("Estado", text="Estado")

        self.tabla.column("ID", width=50)
        self.tabla.column("Estudiante", width=200)
        self.tabla.column("DNI", width=100)
        self.tabla.column("Grado", width=100)
        self.tabla.column("Mes", width=100)
        self.tabla.column("Monto", width=100)
        self.tabla.column("Cargo Especial", width=100)
        self.tabla.column("Estado", width=100)

        # Barra de desplazamiento
        barra_desplazamiento = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra_desplazamiento.set)

        # Empaquetar elementos
        self.tabla.pack(side="left", fill="both", expand=True)
        barra_desplazamiento.pack(side="right", fill="y")

        # Marco para botones
        marco_botones = ctk.CTkFrame(self)
        marco_botones.pack(fill="x", padx=5, pady=5)

        self.boton_anular = ctk.CTkButton(
            marco_botones,
            text="Anular Cupón",
            fg_color="red",
            state="disabled"
        )
        self.boton_anular.pack(side="left", padx=5)

        self.boton_reactivar = ctk.CTkButton(
            marco_botones,
            text="Reactivar Cupón",
            fg_color="green",
            state="disabled"
        )
        self.boton_reactivar.pack(side="left", padx=5)

        self.boton_eliminar = ctk.CTkButton(
            marco_botones,
            text="Eliminar Cupón",
            fg_color="red",
            state="disabled"
        )
        self.boton_eliminar.pack(side="left", padx=5)

        # Vincular evento de selección
        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar)

    def actualizar_lista(self, cupones):
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Insertar cupones
        for cupon in cupones:
            self.tabla.insert("", "end", values=(
                cupon.id,
                cupon.nombre_estudiante,
                cupon.dni_estudiante,
                cupon.grado,
                UtilidadesMeses.obtener_nombre_mes(cupon.mes),
                f"${cupon.monto_total:.2f}",
                "Sí (50%)" if cupon.es_cargo_especial else "No",
                cupon.estado.capitalize()
            ))

    def al_seleccionar(self, evento):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            estado = item["values"][7]  # Columna de estado
            
            # Habilitar/deshabilitar botones según estado
            if estado == "Activo":
                self.boton_anular.configure(state="normal")
                self.boton_reactivar.configure(state="disabled")
            else:  # Anulado
                self.boton_anular.configure(state="disabled")
                self.boton_reactivar.configure(state="normal")
            
            self.boton_eliminar.configure(state="normal")
        else:
            self.boton_anular.configure(state="disabled")
            self.boton_reactivar.configure(state="disabled")
            self.boton_eliminar.configure(state="disabled")