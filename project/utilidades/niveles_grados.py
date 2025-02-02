class NivelesGrados:
    @staticmethod
    def obtener_niveles():
        return ["Inicial", "Primario", "Secundario"]

    @staticmethod
    def obtener_grados_por_nivel(nivel: str) -> list:
        grados = {
            "Inicial": [
                "Sala 3 TM", "Sala 3 TT", 
                "Sala 4 TM", "Sala 4 TT", 
                "Sala 5 TM", "Sala 5 TT"
            ],
            "Primario": [
                "1ºA", "1ºB", "1ºC",
                "2ºA", "2ºB", "2ºC",
                "3ºA", "3ºB", "3ºC",
                "4ºA", "4ºB",
                "5ºA", "5ºB",
                "6ºA", "6ºB"
            ],
            "Secundario": [
                "1ºA", "1ºB",
                "2ºA", "2ºB",
                "3ºA", "3ºB",
                "4º Economía", "4º Sociales",
                "5º Economía", "5º Sociales",
                "6º Economía", "6º Sociales"
            ]
        }
        return grados.get(nivel, [])