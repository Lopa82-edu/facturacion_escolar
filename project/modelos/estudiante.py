from dataclasses import dataclass
from datetime import datetime

@dataclass
class Estudiante:
    dni: str
    nombre: str
    apellido: str
    grado: str
    fecha_nacimiento: str = ""
    genero: str = ""
    direccion: str = ""
    telefono_emergencia: str = ""
    doble_jornada: bool = False
    id: int = None
    fecha_registro: str = datetime.now().strftime("%Y-%m-%d")
    activo: bool = True

    def a_tupla(self):
        return (
            self.dni, self.nombre, self.apellido,
            self.fecha_nacimiento, self.genero, self.direccion,
            self.telefono_emergencia, self.grado,
            self.fecha_registro, self.activo,
            self.doble_jornada
        )