import customtkinter as ctk
from modelos.tutor import Tutor

class FormularioTutor(ctk.CTkFrame):
    def __init__(self, padre):
        super().__init__(padre)
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Título
        titulo = ctk.CTkLabel(self, text="Datos de los Tutores", font=("Arial", 16, "bold"))
        titulo.pack(pady=5)

        # Tutor 1
        self.marco_tutor1 = self.crear_marco_tutor("Tutor 1")
        self.marco_tutor1.pack(fill="x", padx=5, pady=5)

        # Tutor 2
        self.marco_tutor2 = self.crear_marco_tutor("Tutor 2")
        self.marco_tutor2.pack(fill="x", padx=5, pady=5)

    def crear_marco_tutor(self, titulo):
        marco = ctk.CTkFrame(self)
        
        # Título del tutor
        ctk.CTkLabel(marco, text=titulo, font=("Arial", 14, "bold")).pack(pady=5)
        
        # Campos del tutor
        campos = {}
        campos['dni'] = self.crear_entrada(marco, "DNI:")
        campos['nombre_completo'] = self.crear_entrada(marco, "Nombre Completo:")
        campos['telefono'] = self.crear_entrada(marco, "Teléfono:")
        campos['email'] = self.crear_entrada(marco, "Email:")
        campos['parentesco'] = self.crear_combobox(
            marco, 
            "Parentesco:", 
            ["", "Madre", "Padre", "Tutor", "Otro"]
        )
        
        if titulo == "Tutor 1":
            self.campos_tutor1 = campos
        else:
            self.campos_tutor2 = campos
            
        return marco

    def crear_entrada(self, padre, texto_etiqueta):
        marco = ctk.CTkFrame(padre)
        marco.pack(fill="x", pady=2)
        
        ctk.CTkLabel(marco, text=texto_etiqueta).pack(side="left", padx=5)
        entrada = ctk.CTkEntry(marco)
        entrada.pack(side="right", expand=True, fill="x", padx=5)
        return entrada

    def crear_combobox(self, padre, texto_etiqueta, valores):
        marco = ctk.CTkFrame(padre)
        marco.pack(fill="x", pady=2)
        
        ctk.CTkLabel(marco, text=texto_etiqueta).pack(side="left", padx=5)
        combobox = ctk.CTkComboBox(marco, values=valores)
        combobox.pack(side="right", expand=True, fill="x", padx=5)
        return combobox

    def obtener_datos_tutor(self, id_estudiante):
        tutores = []
        
        # Tutor 1
        if any(campo.get() for campo in self.campos_tutor1.values()):
            tutores.append(Tutor(
                id_estudiante=id_estudiante,
                tipo_tutor="tutor1",
                dni=self.campos_tutor1['dni'].get(),
                nombre_completo=self.campos_tutor1['nombre_completo'].get(),
                telefono=self.campos_tutor1['telefono'].get(),
                email=self.campos_tutor1['email'].get(),
                parentesco=self.campos_tutor1['parentesco'].get()
            ))
        
        # Tutor 2
        if any(campo.get() for campo in self.campos_tutor2.values()):
            tutores.append(Tutor(
                id_estudiante=id_estudiante,
                tipo_tutor="tutor2",
                dni=self.campos_tutor2['dni'].get(),
                nombre_completo=self.campos_tutor2['nombre_completo'].get(),
                telefono=self.campos_tutor2['telefono'].get(),
                email=self.campos_tutor2['email'].get(),
                parentesco=self.campos_tutor2['parentesco'].get()
            ))
            
        return tutores

    def limpiar_formulario(self):
        for campos in [self.campos_tutor1, self.campos_tutor2]:
            for campo in campos.values():
                if isinstance(campo, ctk.CTkEntry):
                    campo.delete(0, 'end')
                elif isinstance(campo, ctk.CTkComboBox):
                    campo.set("")

    def establecer_datos_tutor(self, tutores):
        self.limpiar_formulario()
        for tutor in tutores:
            campos = self.campos_tutor1 if tutor.tipo_tutor == "tutor1" else self.campos_tutor2
            campos['dni'].insert(0, tutor.dni)
            campos['nombre_completo'].insert(0, tutor.nombre_completo)
            campos['telefono'].insert(0, tutor.telefono)
            campos['email'].insert(0, tutor.email)
            campos['parentesco'].set(tutor.parentesco)