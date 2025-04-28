import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

# Función simulada de búsqueda (después la vas a reemplazar por tu lógica real)
def buscar_codigos():
    codigos = entrada_codigos.get().split(",")
    codigos = [codigo.strip() for codigo in codigos if codigo.strip()]

    if not codigos:
        messagebox.showwarning("Advertencia", "Por favor ingrese al menos un código.")
        return

    resultados.delete(0, tk.END)  # Limpia resultados anteriores

    # Acá va la lógica real. De momento, simulamos resultados
    for codigo in codigos:
        resultados.insert(tk.END, f"Código '{codigo}' encontrado en archivo_simulado.xlsx - Hoja1")
        resultados.insert(tk.END, "Ruta: C:/ruta/ficticia/archivo_simulado.xlsx")
        resultados.insert(tk.END, "----------------------------------------")

# Crear ventana principal
root = tk.Tk()
root.title("CodeFinder")
root.geometry("600x500")
root.resizable(False, False)

# Widgets
label_codigos = tk.Label(root, text="Código/s a buscar:", font=("Arial", 12))
label_codigos.pack(pady=10)

entrada_codigos = tk.Entry(root, width=60, font=("Arial", 11))
entrada_codigos.pack(pady=5)

boton_buscar = tk.Button(root, text="Buscar", command=buscar_codigos, width=20, bg="#4CAF50", fg="white", font=("Arial", 11))
boton_buscar.pack(pady=10)

label_resultados = tk.Label(root, text="Resultados:", font=("Arial", 12))
label_resultados.pack(pady=10)

resultados = tk.Listbox(root, width=80, height=15, font=("Courier", 10))
resultados.pack(pady=5)

# Ejecutar aplicación
root.mainloop()
