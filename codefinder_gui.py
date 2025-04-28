# codefinder_gui.py

import tkinter as tk
from tkinter import messagebox, filedialog
from codefinder_base import buscar_codigos_en_archivos  # Importa la función

# Variable global para guardar la ruta seleccionada
ruta_base = "C:\Users\PC-DEPO\Dropbox\ADMINISTRACION\CONTROL\PENDIENTES"

def seleccionar_carpeta():
    global ruta_base
    carpeta_seleccionada = filedialog.askdirectory()
    if carpeta_seleccionada:
        ruta_base = carpeta_seleccionada
        etiqueta_ruta.config(text=f"Carpeta seleccionada:\n{ruta_base}")
    else:
        messagebox.showinfo("Información", "No se seleccionó ninguna carpeta.")

def buscar_codigos():
    global ruta_base

    if not ruta_base:
        messagebox.showwarning("Advertencia", "Por favor seleccioná una carpeta primero.")
        return

    codigos = entrada_codigos.get().split(",")
    codigos = [codigo.strip() for codigo in codigos if codigo.strip()]

    if not codigos:
        messagebox.showwarning("Advertencia", "Por favor ingresá al menos un código.")
        return

    resultados.delete(0, tk.END)  # Limpiar resultados anteriores

    resultados_encontrados = buscar_codigos_en_archivos(ruta_base, codigos)

    if resultados_encontrados:
        for resultado in resultados_encontrados:
            resultados.insert(tk.END, f"Código '{resultado['codigo']}' encontrado en archivo {resultado['archivo']} - Hoja {resultado['hoja']}")
            resultados.insert(tk.END, f"Ruta: {resultado['ruta']}")
            resultados.insert(tk.END, "----------------------------------------")
    else:
        resultados.insert(tk.END, "No se encontraron códigos.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("CodeFinder GUI")
ventana.geometry("700x500")

# Botón para seleccionar carpeta
boton_carpeta = tk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
boton_carpeta.pack(pady=10)

# Etiqueta para mostrar la ruta
etiqueta_ruta = tk.Label(ventana, text="No se seleccionó carpeta", wraplength=600, justify="center")
etiqueta_ruta.pack(pady=5)

# Entrada de códigos
entrada_codigos = tk.Entry(ventana, width=80)
entrada_codigos.pack(pady=10)

# Botón para buscar
boton_buscar = tk.Button(ventana, text="Buscar Códigos", command=buscar_codigos)
boton_buscar.pack(pady=10)

# Lista para mostrar resultados
resultados = tk.Listbox(ventana, width=100, height=20)
resultados.pack(pady=20)

# Iniciar la ventana
ventana.mainloop()
