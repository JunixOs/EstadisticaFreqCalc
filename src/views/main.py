# === Archivo: src/main.py ===

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from path_manager import Get_Resource_Path
from calcs.manager_calcs import gestionar_datos
from views.results import VentanaProcesamiento
from imports.import_excel import Load_Excel , Change_Sheet_In_Loaded_Excel

import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import PhotoImage
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from excception_handler import WarningException
from PIL import Image, ImageTk
import pandas as pd

class mainWindow:
    def __init__(self):
        self.root = ttkb.Window(themename="flatly")
        self.root.title("TabuladorPy")
        self.root.iconbitmap("assets/icono.ico")
        width, height = 700, 550

        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.configure(bg="#F5ECD5")
        self.root.protocol("WM_DELETE_WINDOW" , self.Exit)

        self.excel_path = tk.StringVar(self.root)
        self.decimals_precision = tk.IntVar(self.root)
        self.sheet_number = tk.IntVar(self.root)

        self.estilos_personalizados()
        self.crear_botones()
        self.crear_entradas()
        self.texto()

    def estilos_personalizados(self):
        style = ttkb.Style()
        style.configure("Custom.TLabel", foreground="#222831", background="#F5ECD5", font=("Franklin Gothic Demi", 13))
        style.configure("Custom.TButton", foreground="#F5ECD5", background="#626F47", font=("Franklin Gothic Demi", 13))
        style.configure("Custom.TEntry", fieldbackground="#FFFFFF", foreground="#222831", font=("Aptos", 12))

    def texto(self):
        ttkb.Label(self.root, text="Cargue la tabla de excel:", style="Custom.TLabel").place(x=110, y=30)
        ttkb.Label(self.root, text="Nombre de la columna:", style="Custom.TLabel").place(x=110, y=130)
        ttkb.Label(self.root, text="Numero de hoja", style="Custom.TLabel").place(x=110, y=215)
        ttkb.Label(self.root, text="Tipo de variable:", style="Custom.TLabel").place(x=110, y=295)
        ttkb.Label(self.root, text="Presición:", style="Custom.TLabel").place(x=110, y=390)

    def crear_botones(self):
        iconoExcel_pil = Image.open("assets/icono-excel.png").resize((24, 24), Image.LANCZOS)
        self.iconoExcel = ImageTk.PhotoImage(iconoExcel_pil)

        btncargarexcel = ttkb.Button(self.root, image=self.iconoExcel, compound=tk.LEFT, text="Cargar Excel",
                                    style="Custom.TButton",
                                    command= lambda: Load_Excel(self.excel_path , self.columns_name , self.combobox_columns_name , self.sheet_number))
        btncargarexcel.place(x=110, y=70)

        btnprocesar = ttkb.Button(self.root, text="Procesar", style="Custom.TButton", command=self.Process_Data)
        btnprocesar.place(x=300, y=470)

    def crear_entradas(self):
        self.columns_name = []
        self.combobox_columns_name = ttkb.Combobox(self.root, values=self.columns_name, state="readonly",
                                                    font=("Franklin Gothic Demi", 12), width=30)
        self.combobox_columns_name.place(x=110, y=170)

        spinbox_sheet_number = ttkb.Spinbox(self.root, from_=1, to=100, font=("Aptos", 10), width=10,
                                            textvariable=self.sheet_number, state="readonly",
                                            command= lambda: Change_Sheet_In_Loaded_Excel(self.excel_path , self.columns_name , self.combobox_columns_name , self.sheet_number))
        spinbox_sheet_number.place(x=110, y=255)
        spinbox_sheet_number.set(1)

        opciones = ["Discreta", "Continua"]
        self.type_variable = ttkb.Combobox(self.root, values=opciones, state="readonly",
                                            font=("Franklin Gothic Demi", 12), width=22)
        self.type_variable.set("Seleccionar tipo de variable")
        self.type_variable.place(x=110, y=330)

        spinbox_precision = ttkb.Spinbox(self.root, from_=0, to=5, font=("Aptos", 10), width=10,
                                            textvariable=self.decimals_precision, state="readonly")
        spinbox_precision.place(x=110, y=430)

    def Validate_Data(self):
        if not self.excel_path.get():
            raise WarningException("No se ha ingresado el excel a exportar.")

        if not self.combobox_columns_name.get():
            raise WarningException("No se ha seleccionado una columna del Excel.")

        if self.decimals_precision.get() < 0:
            raise WarningException("Valor no válido para la precisión.")

        if not self.type_variable.get() or self.type_variable.get() == "Seleccionar tipo de variable":
            raise WarningException("Por favor, seleccione el tipo de variable.")

    def Process_Data(self):
        try:
            self.Validate_Data()

            Dictionary_Results = gestionar_datos(
                self.excel_path.get(),
                self.combobox_columns_name.get(),
                self.type_variable.get(),
                self.decimals_precision.get()
            )

            self.root.state(newstate="withdraw")
            VentanaProcesamiento(self.root , Dictionary_Results , self.decimals_precision.get())

        except (WarningException, FileNotFoundError) as e:
            messagebox.showwarning("Advertencia", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def Exit(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.destroy()


if __name__ == "__main__":
    app = mainWindow()
    app.root.mainloop()
