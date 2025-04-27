import os
import pandas as pd

# Ruta base donde están todos los proveedores
dropbox_base = r'Ruta donde se encuentran los proveedores'

# Extensiones válidas
extensiones_excel = ['.xlsx', '.xls']

def seleccionar_proveedor():
    proveedores = [nombre for nombre in os.listdir(dropbox_base) if os.path.isdir(os.path.join(dropbox_base, nombre))]

    if not proveedores:
        print("\n==============================")
        print("🚫 No se encontraron carpetas de proveedores.")
        return None

    print("\n📦 Proveedores disponibles:")
    for i, proveedor in enumerate(proveedores, 1):
        print(f"{i}. {proveedor}")

    entrada = input("📝 Ingresá el número o nombre del proveedor (o 'salir'): ").strip()

    if entrada.lower() in ['salir', 'q']:
        return 'salir'

    if entrada.isdigit():
        indice = int(entrada) - 1
        if 0 <= indice < len(proveedores):
            return proveedores[indice]
    elif entrada in proveedores:
        return entrada

    print("❌ Proveedor no válido.")
    return None

def buscar_codigos(carpeta_busqueda, codigos):
    resultados = []
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
                                if df.astype(str).apply(lambda x: x.str.strip() == codigo).any().any():
                                    resultados.append((codigo, archivo, hoja, ruta_archivo))
                        except Exception as e:
                            print(f"⚠️ Error leyendo hoja '{hoja}' en archivo '{archivo}': {e}")
                except Exception as e:
                    print(f"⚠️ No se pudo abrir el archivo '{archivo}': {e}")
    return resultados

def mostrar_resultados(resultados):
    if resultados:
        print("\n🔎 Resultados encontrados:")
        resultados_por_codigo = {}
        for codigo, archivo, hoja, ruta in resultados:
            if codigo not in resultados_por_codigo:
                resultados_por_codigo[codigo] = []
            resultados_por_codigo[codigo].append((archivo, hoja, ruta))

        for codigo, detalles in resultados_por_codigo.items():
            print(f"\nResultados para el código '{codigo}':")
            for archivo, hoja, ruta in detalles:
                print(f"  - Archivo: '{archivo}'")
                print(f"    Hoja:    '{hoja}'")
                print(f"    Ruta:    '{ruta}'")
    else:
        print("\n==============================")
        print("🚫 No se encontró ningún código en los archivos Excel.")

# Bucle principal
while True:
    print("\n==============================")
    print("🔁 Nueva búsqueda de productos")
    print("==============================")

    proveedor = seleccionar_proveedor()
    if proveedor == 'salir':
        print("👋 Cerrando el buscador...")
        break
    if not proveedor:
        continue

    carpeta_busqueda = os.path.join(dropbox_base, proveedor)
    if not os.path.exists(carpeta_busqueda):
        print("❌ Carpeta del proveedor no encontrada.")
        continue
    
    print("\n==============================")
    codigos_input = input("🔍 Introducí los códigos separados por comas (o 'salir' para terminar): ").strip()
    if codigos_input.lower() in ['salir', 'q']:
        print("👋 Cerrando el buscador...")
        break

    codigos = [c.strip() for c in codigos_input.split(",")]
    resultados = buscar_codigos(carpeta_busqueda, codigos)
    mostrar_resultados(resultados)
