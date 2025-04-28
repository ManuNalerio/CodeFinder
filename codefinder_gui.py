import os
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog
import pandas as pd

# Ruta base donde están las carpetas de proveedores
ruta_base = "Tu ruta de acceso a la carpeta con archivos excel"

# Crear ventana principal
app = ttk.Window(themename="superhero")  # Dark mode con bordes suaves
app.title("CodeFinder - Buscador de Códigos")
app.geometry("800x600")
app.resizable(False, False)

# Variables
proveedor_var = tk.StringVar()
codigos_var = tk.StringVar()

# Funciones
def cargar_proveedores():
    proveedores = []
    for carpeta in os.listdir(ruta_base):
        if os.path.isdir(os.path.join(ruta_base, carpeta)):
            proveedores.append(carpeta)
    return sorted(proveedores)

def buscar_codigos():
    proveedor = proveedor_var.get()
    codigos_buscar = codigos_var.get().split(",")
    codigos_buscar = [codigo.strip() for codigo in codigos_buscar]

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)

    total_encontrados = 0

    for carpeta_proveedor in os.listdir(ruta_base):
        if proveedor.lower() in carpeta_proveedor.lower():
            carpeta_path = os.path.join(ruta_base, carpeta_proveedor)

            for archivo in os.listdir(carpeta_path):
                if archivo.endswith(".xlsx"):
                    archivo_path = os.path.join(carpeta_path, archivo)
                    try:
                        xls = pd.ExcelFile(archivo_path)
                        for hoja in xls.sheet_names:
                            df = pd.read_excel(archivo_path, sheet_name=hoja, dtype=str)
                            for codigo in codigos_buscar:
                                if df.apply(lambda x: x.astype(str).str.contains(codigo, case=False).any(), axis=1).any():
                                    total_encontrados += 1
                                    output_text.insert(tk.END, f"\n✅ Código '{codigo}' encontrado en:\n", "bold")
                                    output_text.insert(tk.END, f"📄 Archivo: {archivo}\n", "regular")
                                    output_text.insert(tk.END, f"📄 Hoja: {hoja}\n", "regular")
                                    output_text.insert(tk.END, f"📂 Ruta: {archivo_path}\n", "regular")
                                    output_text.insert(tk.END, "-"*40 + "\n", "separator")
                    except Exception as e:
                        print(f"Error al procesar {archivo_path}: {e}")

    if total_encontrados == 0:
        output_text.insert(tk.END, "\n🚫 No se encontraron coincidencias.\n", "no_results")

    output_text.config(state="disabled")

def limpiar_resultados():
    proveedor_var.set("")
    codigos_var.set("")
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.config(state="disabled")

def cambiar_tema():
    tema_actual = app.style.theme.name
    if tema_actual == "superhero":
        app.style.theme_use("flatly")
    else:
        app.style.theme_use("superhero")

# Widgets
frame_input = ttk.Frame(app, padding=10)
frame_input.pack(fill="x")

label_proveedor = ttk.Label(frame_input, text="Proveedor:")
label_proveedor.pack(side="left", padx=(0, 5))

proveedores = cargar_proveedores()
proveedor_dropdown = ttk.Combobox(frame_input, textvariable=proveedor_var, values=proveedores, width=40)
proveedor_dropdown.pack(side="left", padx=(0, 15))

label_codigos = ttk.Label(frame_input, text="Códigos (separados por coma):")
label_codigos.pack(side="left", padx=(0, 5))

entry_codigos = ttk.Entry(frame_input, textvariable=codigos_var, width=40)
entry_codigos.pack(side="left", padx=(0, 5))

frame_buttons = ttk.Frame(app, padding=10)
frame_buttons.pack(fill="x")

buscar_button = ttk.Button(frame_buttons, text="Buscar", command=buscar_codigos, bootstyle="success")
buscar_button.pack(side="left", padx=(0, 10))

limpiar_button = ttk.Button(frame_buttons, text="Limpiar Resultados", command=limpiar_resultados, bootstyle="danger")
limpiar_button.pack(side="left", padx=(0, 10))

tema_button = ttk.Button(frame_buttons, text="Cambiar Tema", command=cambiar_tema, bootstyle="info")
tema_button.pack(side="left", padx=(0, 10))

frame_output = ttk.Frame(app, padding=10)
frame_output.pack(fill="both", expand=True)

output_text = tk.Text(frame_output, wrap="word", state="disabled", bg="#2b2b2b", fg="white", insertbackground="white", relief="flat")
output_text.pack(fill="both", expand=True)

# Configuración de estilos para el output
output_text.tag_configure("bold", foreground="#00ff99", font=("Helvetica", 11, "bold"))
output_text.tag_configure("regular", foreground="#cccccc", font=("Helvetica", 10))
output_text.tag_configure("separator", foreground="#666666", font=("Helvetica", 8))
output_text.tag_configure("no_results", foreground="#ff5555", font=("Helvetica", 11, "bold"))

# Ejecutar aplicación
app.mainloop()
