from dataclasses import dataclass

@dataclass
class ItemPrecio:
    nivel: str
    nombre: str
    monto: float
    id: int = None
    activo: bool = True
    solo_doble_jornada: bool = False
    item_mantenimiento: bool = False

    def a_tupla(self):
        return (
            self.nivel,
            self.nombre,
            self.monto,
            self.activo,
            self.solo_doble_jornada,
            self.item_mantenimiento
        )