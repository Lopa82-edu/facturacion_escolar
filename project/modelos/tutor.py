from dataclasses import dataclass

@dataclass
class Tutor:
    id_estudiante: int
    tipo_tutor: str  # "tutor1" o "tutor2"
    dni: str = ""
    nombre_completo: str = ""
    telefono: str = ""
    email: str = ""
    parentesco: str = ""
    id: int = None

    def a_tupla(self):
        return (
            self.id_estudiante, self.tipo_tutor,
            self.dni, self.nombre_completo, self.telefono,
            self.email, self.parentesco
        )