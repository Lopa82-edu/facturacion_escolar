from dataclasses import dataclass
from datetime import datetime

@dataclass
class Pago:
    id_cupon: int
    fecha_pago: str = datetime.now().strftime("%Y-%m-%d")
    numero_recibo: int = None
    id: int = None

    def a_tupla(self):
        return (
            self.id_cupon,
            self.fecha_pago,
            self.numero_recibo
        )