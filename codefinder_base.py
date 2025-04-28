def buscar_codigos_en_archivos(ruta_base, codigos_a_buscar):
    resultados = []
    
    for carpeta, subcarpetas, archivos in os.walk(ruta_base):
        for archivo in archivos:
            if archivo.endswith('.xlsx'):
                ruta_completa = os.path.join(carpeta, archivo)
                try:
                    excel_file = pd.ExcelFile(ruta_completa)
                    for hoja in excel_file.sheet_names:
                        df = pd.read_excel(ruta_completa, sheet_name=hoja)
                        for codigo in codigos_a_buscar:
                            if codigo in df.to_string():
                                resultados.append({
                                    'archivo': archivo,
                                    'hoja': hoja,
                                    'ruta': ruta_completa,
                                    'codigo': codigo
                                })
                except Exception as e:
                    print(f"Error leyendo {ruta_completa}: {e}")

    return resultados