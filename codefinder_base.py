import os
import pandas as pd

def buscar_codigos_en_archivos(ruta_base, codigos):
    resultados = []
    for carpeta, subcarpetas, archivos in os.walk(ruta_base):
        for archivo in archivos:
            if archivo.endswith(('.xls', '.xlsx')):
                ruta_archivo = os.path.join(carpeta, archivo)
                try:
                    xls = pd.ExcelFile(ruta_archivo)
                    for hoja in xls.sheet_names:
                        df = pd.read_excel(ruta_archivo, sheet_name=hoja, dtype=str)
                        for codigo in codigos:
                            if codigo in df.values:
                                mensaje = (
                                    f"🔎 Código encontrado: {codigo}\n\n"
                                    f"📄 Archivo: {archivo}\n"
                                    f"📄 Hoja: {hoja}\n"
                                    f"📂 Ruta: {ruta_archivo}\n"
                                    f"{'─'*40}\n"
                                )
                                resultados.append(mensaje)
                except Exception as e:
                    print(f"Error al procesar el archivo {ruta_archivo}: {e}")
    return resultados
