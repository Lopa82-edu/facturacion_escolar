import customtkinter as ctk

def crear_entrada(padre, texto_etiqueta):
    marco = ctk.CTkFrame(padre)
    marco.pack(fill="x", pady=2)
    
    ctk.CTkLabel(marco, text=texto_etiqueta).pack(side="left", padx=5)
    entrada = ctk.CTkEntry(marco)
    entrada.pack(side="right", expand=True, fill="x", padx=5)
    return entrada

def crear_combobox(padre, texto_etiqueta, valores, command=None):
    marco = ctk.CTkFrame(padre)
    marco.pack(fill="x", pady=2)
    
    ctk.CTkLabel(marco, text=texto_etiqueta).pack(side="left", padx=5)
    combobox = ctk.CTkComboBox(marco, values=valores, command=command)
    combobox.pack(side="right", expand=True, fill="x", padx=5)
    return combobox