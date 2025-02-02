import customtkinter as ctk
from datetime import datetime

class UtilidadesMeses:
    @staticmethod
    def obtener_meses():
        return [
            "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre",
            "Octubre", "Noviembre", "Diciembre"
        ]
    
    @staticmethod
    def obtener_numero_mes(nombre_mes: str) -> int:
        meses = {
            "Marzo": 3, "Abril": 4, "Mayo": 5,
            "Junio": 6, "Julio": 7, "Agosto": 8,
            "Septiembre": 9, "Octubre": 10,
            "Noviembre": 11, "Diciembre": 12
        }
        return meses.get(nombre_mes, 0)
    
    @staticmethod
    def obtener_nombre_mes(numero_mes: int) -> str:
        meses = {
            3: "Marzo", 4: "Abril", 5: "Mayo",
            6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre",
            11: "Noviembre", 12: "Diciembre"
        }
        return meses.get(numero_mes, "")

    @staticmethod
    def es_mes_mantenimiento(numero_mes: int) -> bool:
        """Verifica si el mes requiere cuota de mantenimiento"""
        return numero_mes in [6, 11]  # Junio y Noviembre

    @staticmethod
    def obtener_año_actual() -> int:
        """Obtiene el año actual"""
        return datetime.now().year