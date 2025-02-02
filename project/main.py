import customtkinter as ctk
from database.db_config import create_connection, create_tables
from database.init_db import init_database
from views.registration_tab import RegistrationTab
from views.price_tab import PriceTab
from views.payment_tab import PaymentTab
from views.collection_tab import CollectionTab

class SchoolManagementApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Instituto Incorporado San Andrés by Pablo Sánchez")
        
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Configure geometry for full screen
        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Maximize window
        self.window.state('zoomed')

        # Configure default font size
        ctk.set_widget_scaling(1.2)  # Increase widget size by 20%
        ctk.set_window_scaling(1.2)  # Increase window scaling by 20%
        
        # Initialize database
        init_database()

        # Create notebook (tabs) with larger text
        self.notebook = ctk.CTkTabview(self.window, text_color="black", segmented_button_fg_color="gray85", 
                                     segmented_button_selected_color="gray75", segmented_button_selected_hover_color="gray70",
                                     segmented_button_unselected_color="gray90", segmented_button_unselected_hover_color="gray80")
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Add tabs
        self.notebook.add("Registro de estudiantes")
        self.notebook.add("Carga de items")
        self.notebook.add("Generación de pagos")
        self.notebook.add("Cobranza")
        
        # Add content to tabs
        self.registration_tab = RegistrationTab(self.notebook.tab("Registro de estudiantes"))
        self.registration_tab.pack(expand=True, fill="both", padx=10, pady=10)

        self.price_tab = PriceTab(self.notebook.tab("Carga de items"))
        self.price_tab.pack(expand=True, fill="both", padx=10, pady=10)

        self.payment_tab = PaymentTab(self.notebook.tab("Generación de pagos"))
        self.payment_tab.pack(expand=True, fill="both", padx=10, pady=10)

        self.collection_tab = CollectionTab(self.notebook.tab("Cobranza"))
        self.collection_tab.pack(expand=True, fill="both", padx=10, pady=10)

        # Set initial tab to "Cobranza"
        self.notebook.set("Cobranza")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = SchoolManagementApp()
    app.run()