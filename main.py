import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd

class ExcelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Selectare Magazin")

        self.file_paths = {}

        self.selected_store = tk.StringVar()

        self.complete_button = None

        self.create_widgets()

    def check_completion(self):
        all_checked = all(var.get() == 1 for var in self.check_vars)

        if all_checked:
            self.message_label.config(text="Ați completat lista de cumpărături!")
        else:
            self.message_label.config(text="")

    def create_widgets(self):
        # Buton pentru încărcarea datelor din magazinul selectat
        self.load_button = tk.Button(self.root, text="Încarcă Date", command=self.load_data)
        self.load_button.pack(pady=10)

        # Dropdown pentru selecția magazinului
        self.store_dropdown = tk.OptionMenu(self.root, self.selected_store, "")
        self.store_dropdown.pack(pady=10)

        # Frame pentru afișarea datelor
        self.data_frame = tk.Frame(self.root)
        self.data_frame.pack(pady=10)

        # Label pentru mesaj
        self.message_label = tk.Label(self.root, text="")
        self.message_label.pack(pady=10)

        # Inițializează calea pentru fiecare magazin
        self.initialize_store_paths()

    def initialize_store_paths(self):
        # Adaugare cale pt magazin
        self.file_paths["Profi"] = r"D:\python\project\Profi.xlsx"
        self.file_paths["Mega Image"] = r"D:\python\project\MegaImage.xlsx"
        self.file_paths["Kaufland"] = r"D:\python\project\kaufland.xlsx"
        self.file_paths["Lidl"] = r"D:\python\project\Lidl.xlsx"

        # Actualizează opțiunile din dropdown
        self.update_store_options()

    def update_store_options(self):
        self.store_options = list(self.file_paths.keys())
        self.store_dropdown.destroy()
        self.store_dropdown = tk.OptionMenu(self.root, self.selected_store, *self.store_options)
        self.store_dropdown.pack(pady=10)

    def load_data(self):
        # Distrugerea butonului de finalizare anterior (dacă există)
        if self.complete_button:
            self.complete_button.destroy()

        # Verifică dacă a fost selectat un magazin
        selected_store = self.selected_store.get()
        if not selected_store:
            self.message_label.config(text="Vă rugăm să selectați un magazin.")
            return

        file_path = self.file_paths.get(selected_store, "")

        if not file_path:
            self.message_label.config(text="Calea pentru magazin nu a fost găsită.")
            return

        # Afișează mesajul cu magazinul selectat
        self.message_label.config(text=f"Magazin selectat: {selected_store}")

        # Încarcă datele din fișierul Excel al magazinului selectat
        self.data = pd.read_excel(file_path)

        # Afișează datele în Frame
        self.display_data()

    def display_data(self):
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        self.check_vars = []

        if hasattr(self, 'data'):
            for index, row in self.data.iterrows():
                food_name = str(row['Lista'])

                entry_text = f"{food_name}"

                entry = tk.Entry(self.data_frame, width=40)
                entry.insert(tk.END, entry_text)
                entry.grid(row=index, column=0, pady=5)

                check_var = tk.IntVar()
                check_button = tk.Checkbutton(self.data_frame, text="", variable=check_var)
                check_button.grid(row=index, column=1, pady=5)

                self.check_vars.append(check_var)

        # Crearea butonului finalizează cumpărăturile doar dacă nu a fost creat anterior
        self.complete_button = tk.Button(self.root, text="Finalizează Cumpărăturile", command=self.check_completion)
        self.complete_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelGUI(root)
    root.mainloop()
