from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class ItemCupon:
    id_item: int
    monto: float
    id: int = None
    id_cupon: int = None

@dataclass
class CuponPago:
    id_estudiante: int
    año_academico: int
    mes: int
    nivel: str
    grado: str
    monto_total: float
    es_cargo_especial: bool = False
    porcentaje_cargo_especial: float = 0
    estado: str = 'active'
    id: int = None
    fecha_creacion: str = datetime.now().strftime("%Y-%m-%d")
    items: List[ItemCupon] = None

    def a_tupla(self):
        return (
            self.id_estudiante,
            self.año_academico,
            self.mes,
            self.nivel,
            self.grado,
            self.monto_total,
            self.es_cargo_especial,
            self.porcentaje_cargo_especial,
            self.estado,
            self.fecha_creacion
        )