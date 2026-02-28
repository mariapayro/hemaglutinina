import csv
import os

# --- CONFIGURACIÓN ---
archivo_entrada = "RESULTADOS_cribados_VinaGPU.csv"
archivo_salida = "INPUT_Swifty.csv"

# Las columnas exactas que quieres extraer (tal cual aparecen en tu CSV)
columnas_deseadas = ["Docking_Score", "SMILES"]

print(f"--- Extrayendo columnas para {archivo_salida} ---")

if not os.path.exists(archivo_entrada):
    print(f"ERROR: No encuentro el archivo {archivo_entrada}. Ejecuta el script de unión primero.")
    exit()

try:
    with open(archivo_entrada, 'r', encoding='utf-8') as f_in, \
         open(archivo_salida, 'w', newline='', encoding='utf-8') as f_out:
        
        # Leemos el archivo original como diccionario (columna: valor)
        reader = csv.DictReader(f_in)
        
        # Configuramos el escritor con solo las columnas que queremos
        writer = csv.DictWriter(f_out, fieldnames=columnas_deseadas)
        
        # Escribimos el encabezado (Docking_Score,SMILES)
        writer.writeheader()
        
        # Escribimos fila por fila, extrayendo solo lo necesario
        count = 0
        for row in reader:
            # Creamos una fila limpia solo con los datos que nos interesan
            # Esto evita errores si falta algún dato, poniendo vacío
            fila_limpia = {col: row.get(col, "") for col in columnas_deseadas}
            writer.writerow(fila_limpia)
            count += 1

    print(f"¡Hecho! Se generó '{archivo_salida}' con {count} compuestos.")

except Exception as e:
    print(f"Ocurrió un error: {e}")
