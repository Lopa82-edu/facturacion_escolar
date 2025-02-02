import customtkinter as ctk
from tkinter import messagebox
from utilidades.niveles_grados import NivelesGrados
from utilidades.utilidades_meses import UtilidadesMeses
from datetime import datetime
from modelos.cupon_pago import CuponPago, ItemCupon
from repositorios.repositorio_estudiantes import RepositorioEstudiantes
from repositorios.repositorio_precios import RepositorioPrecios
from repositorios.repositorio_cupones_pago import RepositorioCuponesPago

class MarcoGeneracionCupones(ctk.CTkFrame):
    def __init__(self, padre, al_actualizar_cupones=None):
        super().__init__(padre)
        self._al_actualizar_cupones = al_actualizar_cupones
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Marco de control
        marco_control = ctk.CTkFrame(self)
        marco_control.pack(fill="x", padx=5, pady=5)

        # Selección de nivel
        marco_nivel = ctk.CTkFrame(marco_control)
        marco_nivel.pack(side="left", padx=5)
        ctk.CTkLabel(marco_nivel, text="Nivel:").pack(side="left", padx=5)
        self.combo_nivel = ctk.CTkComboBox(
            marco_nivel,
            values=NivelesGrados.obtener_niveles(),
            command=self._al_cambiar_filtro,
            width=120
        )
        self.combo_nivel.pack(side="left", padx=5)
        self.combo_nivel.set("")

        # Selección de mes
        marco_mes = ctk.CTkFrame(marco_control)
        marco_mes.pack(side="left", padx=5)
        ctk.CTkLabel(marco_mes, text="Mes:").pack(side="left", padx=5)
        self.combo_mes = ctk.CTkComboBox(
            marco_mes,
            values=UtilidadesMeses.obtener_meses(),
            command=self._al_cambiar_filtro,
            width=120
        )
        self.combo_mes.pack(side="left", padx=5)
        self.combo_mes.set("")

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
        self.combo_año.set(str(año_actual))
        self.combo_año.pack(side="left", padx=5)

        # Casilla de cargo especial
        self.var_cargo_especial = ctk.BooleanVar(value=False)
        self.casilla_cargo_especial = ctk.CTkCheckBox(
            marco_control,
            text="Cargo Especial (50%)",
            variable=self.var_cargo_especial
        )
        self.casilla_cargo_especial.pack(side="left", padx=5)

        # Botón de generar
        self.boton_generar = ctk.CTkButton(
            marco_control,
            text="Generar Cupones",
            command=self.generar_cupones
        )
        self.boton_generar.pack(side="left", padx=5)

    def _al_cambiar_filtro(self, _):
        """Maneja cambios en los filtros"""
        if self._al_actualizar_cupones:
            nivel = self.combo_nivel.get()
            nombre_mes = self.combo_mes.get()
            año = self.combo_año.get()
            
            if all([nivel, nombre_mes, año]):
                numero_mes = UtilidadesMeses.obtener_numero_mes(nombre_mes)
                cupones = RepositorioCuponesPago.obtener_cupones_por_filtros(
                    nivel, numero_mes, int(año)
                )
                self._al_actualizar_cupones(cupones)

    def generar_cupones(self):
        try:
            nivel = self.combo_nivel.get()
            nombre_mes = self.combo_mes.get()
            año = int(self.combo_año.get())
            numero_mes = UtilidadesMeses.obtener_numero_mes(nombre_mes)
            es_especial = self.var_cargo_especial.get()
            es_mantenimiento = UtilidadesMeses.es_mes_mantenimiento(numero_mes)

            if not all([nivel, nombre_mes]):
                messagebox.showerror("Error", "Por favor seleccione nivel y mes")
                return

            # Obtener estudiantes activos del nivel
            estudiantes = RepositorioEstudiantes.obtener_estudiantes_activos_por_nivel(nivel)
            if not estudiantes:
                messagebox.showinfo("Aviso", "No hay estudiantes activos en este nivel")
                return

            # Obtener items de precio del nivel
            items_precio = RepositorioPrecios.obtener_items_por_nivel(nivel)
            if not items_precio:
                messagebox.showerror("Error", "No hay items de precio configurados para este nivel")
                return

            # Generar cupones
            exitos = 0
            errores = 0
            omitidos = 0

            for estudiante in estudiantes:
                # Verificar si ya existe el cupón
                cupon_existente = RepositorioCuponesPago.obtener_cupon_por_estudiante_mes_año(
                    estudiante.id, numero_mes, año
                )
                if cupon_existente:
                    omitidos += 1
                    continue

                # Filtrar items según condiciones
                items_aplicables = [
                    item for item in items_precio 
                    if (not item.solo_doble_jornada or 
                        (item.solo_doble_jornada and estudiante.doble_jornada))
                    and (not es_mantenimiento or 
                         (es_mantenimiento and item.item_mantenimiento))
                ]

                # Calcular monto total
                monto_total = sum(item.monto for item in items_aplicables)
                if es_especial or es_mantenimiento:
                    monto_total *= 0.5

                # Crear cupón
                cupon = CuponPago(
                    id_estudiante=estudiante.id,
                    año_academico=año,
                    mes=numero_mes,
                    nivel=nivel,
                    grado=estudiante.grado,
                    monto_total=monto_total,
                    es_cargo_especial=es_especial or es_mantenimiento,
                    porcentaje_cargo_especial=50 if (es_especial or es_mantenimiento) else 0
                )

                # Agregar items
                cupon.items = []
                for item in items_aplicables:
                    monto = item.monto * 0.5 if (es_especial or es_mantenimiento) else item.monto
                    cupon.items.append(ItemCupon(
                        id_item=item.id,
                        monto=monto
                    ))

                if RepositorioCuponesPago.guardar_cupon(cupon):
                    exitos += 1
                else:
                    errores += 1

            # Mostrar resultado
            mensaje = f"""Proceso completado:
            - {exitos} cupones generados exitosamente
            - {omitidos} cupones omitidos (ya existentes)
            - {errores} errores"""
            
            if errores > 0:
                messagebox.showwarning("Resultado", mensaje)
            else:
                messagebox.showinfo("Éxito", mensaje)
                
            # Actualizar lista de cupones
            self._al_cambiar_filtro(None)

        except Exception as e:
            messagebox.showerror("Error", f"Error en la generación de cupones: {str(e)}")