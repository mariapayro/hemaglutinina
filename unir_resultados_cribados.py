import os
import glob
import csv

# --- CONFIGURACIÓN ---
# Nombre del archivo gigante que vamos a crear
archivo_salida = "RESULTADOS_cribados_VinaGPU.csv"
patron_busqueda = "**/*.csv"  # Busca en subcarpetas

print("--- Iniciando Fusión de Tablas CSV ---")

archivos_encontrados = glob.glob(patron_busqueda, recursive=True)

# Filtramos para que no se intente unir a sí mismo si ya existe el archivo de salida
archivos_csv = [f for f in archivos_encontrados if os.path.basename(f) != archivo_salida]

print(f"Se encontraron {len(archivos_csv)} archivos CSV. Uniendo...")

with open(archivo_salida, 'w', newline='', encoding='utf-8') as f_out:
    writer = None
    
    for i, ruta_csv in enumerate(archivos_csv):
        try:
            with open(ruta_csv, 'r', encoding='utf-8') as f_in:
                reader = csv.reader(f_in)
                header = next(reader, None) # Leemos el encabezado
                
                if header:
                    # Si es el primer archivo, escribimos el encabezado en el archivo maestro
                    if writer is None:
                        writer = csv.writer(f_out)
                        writer.writerow(header)
                    
                    # Escribimos el resto de las filas (contenido)
                    for fila in reader:
                        writer.writerow(fila)
                        
        except Exception as e:
            print(f"Error leyendo {ruta_csv}: {e}")

print(f"¡Listo! Todos los datos están en: {archivo_salida}")
