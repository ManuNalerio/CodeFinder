import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import ttkbootstrap as ttkb
import time

# Ruta base de tus carpetas
ruta_base = r"Tu ruta de acceso a la carpeta contenedora de archivos excel"

# Inicializar ventana principal con tema oscuro
app = ttkb.Window(themename="darkly")
app.title("CodeFinder GUI")
app.geometry("800x600")
app.resizable(False, False)

# Crear estilo
style = ttkb.Style()

# Variable para proveedor seleccionado
proveedor_var = tk.StringVar()

# Frame para seleccionar proveedor
proveedor_frame = ttkb.Frame(app, padding=10)
proveedor_frame.pack(fill="x")

proveedor_label = ttkb.Label(proveedor_frame, text="Seleccionar proveedor:", font=("Segoe UI", 12))
proveedor_label.pack(side="left")

# Cargar lista de carpetas (proveedores)
proveedores = [d for d in os.listdir(ruta_base) if os.path.isdir(os.path.join(ruta_base, d))]

proveedor_dropdown = ttkb.Combobox(proveedor_frame, textvariable=proveedor_var, values=proveedores, width=50, font=("Segoe UI", 11))
proveedor_dropdown.pack(side="left", padx=10)

# Frame para ingresar códigos
input_frame = ttkb.Frame(app, padding=10)
input_frame.pack(fill="x")

entry_label = ttkb.Label(input_frame, text="Ingresar códigos (separados por coma):", font=("Segoe UI", 12))
entry_label.pack(anchor="w")

entry = ttkb.Entry(input_frame, font=("Segoe UI", 11))
entry.pack(fill="x", pady=5)

# Frame para botones
button_frame = ttkb.Frame(app, padding=10)
button_frame.pack(fill="x")

buscar_button = ttkb.Button(button_frame, text="Buscar Códigos", command=lambda: buscar_codigos())
buscar_button.pack(side="left", padx=5)

limpiar_button = ttkb.Button(button_frame, text="Limpiar resultados", command=lambda: limpiar_resultados())
limpiar_button.pack(side="left", padx=5)

cambiar_tema_button = ttkb.Button(button_frame, text="Cambiar Tema", command=lambda: cambiar_tema())
cambiar_tema_button.pack(side="left", padx=5)

# Barra de progreso
progreso = ttkb.Progressbar(app, orient="horizontal", length=400, mode="determinate", bootstyle="success-striped")
progreso.pack(pady=10)

# Área de salida
output_text = tk.Text(app, height=20, font=("Consolas", 10), wrap="word", borderwidth=2, relief="ridge")
output_text.pack(padx=10, pady=10, fill="both", expand=True)

# Funciones principales

def buscar_codigos():
    proveedor = proveedor_var.get()
    codigos = entry.get().replace(" ", "").split(',')

    if not proveedor:
        messagebox.showwarning("Advertencia", "Por favor seleccioná un proveedor.")
        return

    if not codigos or codigos == ['']:
        messagebox.showwarning("Advertencia", "Por favor ingresá al menos un código.")
        return

    carpeta_proveedor = os.path.join(ruta_base, proveedor)

    if not os.path.exists(carpeta_proveedor):
        messagebox.showerror("Error", f"No se encontró la carpeta del proveedor: {proveedor}")
        return

    archivos_excel = [f for f in os.listdir(carpeta_proveedor) if f.endswith((".xls", ".xlsx"))]

    if not archivos_excel:
        messagebox.showinfo("Información", "No hay archivos Excel para este proveedor.")
        return

    progreso["maximum"] = len(archivos_excel)
    progreso["value"] = 0
    output_text.delete('1.0', tk.END)

    for idx, archivo in enumerate(archivos_excel):
        ruta_archivo = os.path.join(carpeta_proveedor, archivo)
        try:
            xls = pd.ExcelFile(ruta_archivo)
            for hoja in xls.sheet_names:
                df = pd.read_excel(ruta_archivo, sheet_name=hoja)
                for codigo in codigos:
                    if df.astype(str).apply(lambda x: x.str.contains(codigo, na=False)).any().any():
                        output_text.insert(tk.END, f"✅ Código '{codigo}' encontrado en:\n")
                        output_text.insert(tk.END, f"   📄 Archivo: {archivo}\n")
                        output_text.insert(tk.END, f"   📄 Hoja: {hoja}\n")
                        output_text.insert(tk.END, f"   📂 Ruta: {ruta_archivo}\n\n")
        except Exception as e:
            output_text.insert(tk.END, f"⚠️ Error procesando {archivo}: {str(e)}\n\n")
        progreso["value"] = idx + 1
        app.update_idletasks()

    messagebox.showinfo("Búsqueda finalizada", "La búsqueda de códigos finalizó.")

def limpiar_resultados():
    output_text.delete('1.0', tk.END)
    progreso["value"] = 0
    entry.delete(0, tk.END)
    proveedor_var.set('')

def cambiar_tema():
    current_theme = style.theme.name
    # Pequeño "efecto de transición"
    app.configure(cursor="watch")
    app.update()
    time.sleep(0.2)
    if current_theme == "darkly":
        style.theme_use("flatly")   # Tema claro
    else:
        style.theme_use("darkly")   # Tema oscuro
    app.configure(cursor="")  # Volver al cursor normal

# Ejecutar la aplicación
app.mainloop()
