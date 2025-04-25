import os
import pandas as pd

# Ruta donde buscar (ajústala a tu carpeta de Dropbox)
carpeta_busqueda = r'C:\Users\PC-DEPO\Dropbox\ADMINISTRACION\CONTROL\PENDIENTES'

# Pedir códigos de productos al usuario
print('******************')
codigos_buscar = input("Introduce los códigos de productos separados por comas: ")
print('******************')
codigos = [c.strip() for c in codigos_buscar.split(",")]

# Extensiones válidas
extensiones_excel = ['.xlsx', '.xls']

# Lista de resultados
resultados = []

# Recorrer todas las carpetas y subcarpetas
for root, dirs, files in os.walk(carpeta_busqueda):
    for archivo in files:
        if any(archivo.endswith(ext) for ext in extensiones_excel):
            ruta_archivo = os.path.join(root, archivo)
            try:
                excel = pd.ExcelFile(ruta_archivo)
                for hoja in excel.sheet_names:
                    try:
                        df = excel.parse(hoja)
                        for codigo in codigos:
                            if df.astype(str).apply(lambda x: x.str.contains(codigo, case=False, na=False)).any().any():
                                resultados.append((codigo, archivo, hoja, ruta_archivo))
                    except Exception as e:
                        print(f"⚠️ Error leyendo hoja '{hoja}' en archivo '{archivo}': {e}")
            except Exception as e:
                print(f"⚠️ No se pudo abrir el archivo '{archivo}': {e}")

# Mostrar resultados ya sea positivo o negativo
if resultados:
    print("\n🔎 Resultados encontrados:")
    for codigo, archivo, hoja, ruta in resultados:
        print(f"- Código '{codigo}' encontrado en:\n    Archivo: '{archivo}'\n    Hoja: '{hoja}'\n    Ruta: '{ruta}'\n")
else:
    print("🚫 No se encontró ningún código en los archivos Excel.")
