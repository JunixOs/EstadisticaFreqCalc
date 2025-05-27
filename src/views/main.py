# === Archivo: src/main.py ===

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from path_manager import Get_Resource_Path
from calcs.manager_calcs import gestionar_datos
from views.results import VentanaProcesamiento

import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import PhotoImage
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from excception_handler import WarningException
from PIL import Image, ImageTk
import pandas as pd

from python_calamine import CalamineWorkbook
import polars as pl

class mainWindow:
    def __init__(self):
        self.root = ttkb.Window(themename="flatly")
        self.root.title("TabuladorPy")
        self.root.iconbitmap(Get_Resource_Path("assets/icono.ico"))
        width, height = 700, 550

        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.configure(bg="#F5ECD5")

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
        iconoExcel_pil = Image.open(Get_Resource_Path("assets/icono-excel.png")).resize((24, 24), Image.LANCZOS)
        self.iconoExcel = ImageTk.PhotoImage(iconoExcel_pil)

        btncargarexcel = ttkb.Button(self.root, image=self.iconoExcel, compound=tk.LEFT, text="Cargar Excel",
                                     style="Custom.TButton",
                                     command=self.cargar_excel)
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
                                            command=self.actualizar_columnas)
        spinbox_sheet_number.place(x=110, y=255)
        spinbox_sheet_number.set(1)

        opciones = ["Discreta", "Continua"]
        self.type_variable = ttkb.Combobox(self.root, values=opciones, state="readonly",
                                           font=("Franklin Gothic Demi", 12), width=22)
        self.type_variable.set("Seleccionar tipo de variable")
        self.type_variable.place(x=110, y=330)

        spinbox_precision = ttkb.Spinbox(self.root, from_=1, to=10, font=("Aptos", 10), width=10,
                                         textvariable=self.decimals_precision, state="readonly")
        spinbox_precision.place(x=110, y=430)

    def cargar_excel(self):
        ruta = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if ruta:
            self.excel_path.set(ruta)
            self.actualizar_columnas()
            self.mostrar_preview_archivo(ruta)  # <- Aquí está la llamada clave


            
    def mostrar_preview_archivo(self, ruta):
        # Eliminar previsualización anterior si existe oñoo
        if hasattr(self, 'frame_preview') and self.frame_preview:
            self.frame_preview.destroy()

        self.frame_preview = tk.Frame(self.root, bg="#F5ECD5", bd=1, relief="solid")
        self.frame_preview.place(x=300, y=70)

        try:
            icono_preview = Image.open(Get_Resource_Path("assets/icono-excel-previsualizacion.png")).resize((20, 20), Image.LANCZOS)
        except:
            icono_preview = Image.new("RGB", (20, 20), "gray")  # En caso de error, icono gris saa

        self.icono_preview = ImageTk.PhotoImage(icono_preview)

        tk.Label(self.frame_preview, image=self.icono_preview, bg="#F5ECD5").pack(side=tk.LEFT, padx=5, pady=5)

        nombre = os.path.basename(ruta)
        nombre_corto = nombre[:20] + "..." if len(nombre) > 23 else nombre
        tk.Label(self.frame_preview, text=nombre_corto, bg="#F5ECD5",
                font=("Aptos", 9), fg="#222831").pack(side=tk.LEFT, padx=2)

        tk.Button(self.frame_preview, text="✕", bg="#F5ECD5", borderwidth=0, fg="gray",
                command=self.eliminar_preview).pack(side=tk.RIGHT, padx=5)

    def eliminar_preview(self):
        self.excel_path.set("")
        if hasattr(self, 'frame_preview') and self.frame_preview:
            self.frame_preview.destroy()

    def actualizar_columnas(self):
        try:
            sheet = self.sheet_number.get()
            Excel = CalamineWorkbook.from_path(self.excel_path.get()).get_sheet_by_index(sheet - 1).to_python(skip_empty_area=False)
            self.columns_name = [col_name for col_name in Excel[0] if col_name]
            self.combobox_columns_name.config(values=self.columns_name)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar columnas: {e}")

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
                self.decimals_precision.get(),
                self.sheet_number.get(),
            )

            self.root.destroy()
            VentanaProcesamiento(Dictionary_Results , self.decimals_precision.get())

        except (WarningException, FileNotFoundError) as e:
            messagebox.showwarning("Advertencia", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = mainWindow()
    app.root.mainloop()
