import os
import glob
import csv
import subprocess

# --- CONFIGURACIÓN ---
# Carpeta donde están tus archivos .pdbqt YA DOCKEADOS (resultados)
carpeta_resultados = "RESULTADOS_2_t1000_c30_ligandos_grandes" 
archivo_salida = "Tabla_Resultados_VinaGPU_10mil_ligandos_grandes.csv" 

# ¿Quieres calcular SMILES? (Pon False si quieres que sea ultra-rápido)
# Para 35,000 archivos, calcular SMILES tardará unas horas.
CALCULAR_SMILES = True 

print(f"--- Iniciando Análisis de Resultados en {carpeta_resultados} ---")

datos = []
# Buscamos todos los pdbqt en la carpeta de resultados
archivos_dockeados = glob.glob(os.path.join(carpeta_resultados, "*.pdbqt"))
total = len(archivos_dockeados)
print(f"Se encontraron {total} estructuras dockeadas. Procesando...")

for i, ruta_archivo in enumerate(archivos_dockeados):
    # 1. Obtener ID Limpio
    nombre_archivo = os.path.basename(ruta_archivo)
    # Quitamos la extensión
    id_compuesto = nombre_archivo.replace(".pdbqt", "")
    # Opcional: Si quieres quitar los sufijos _out, _HEAD, _STEM para tener solo el ZINC ID
    # id_zinc = id_compuesto.replace("_out", "").replace("_HEAD", "").replace("_STEM", "")
    # Pero por ahora dejamos el nombre completo para saber si es HEAD o STEM
    
    # 2. Extraer Docking Score (Energía) desde dentro del archivo
    best_score = None
    try:
        with open(ruta_archivo, 'r') as f:
            for linea in f:
                # Vina escribe esto: "REMARK VINA RESULT:    -9.5      0.000      0.000"
                if "REMARK VINA RESULT:" in linea:
                    partes = linea.split()
                    # El score suele ser el elemento indice 3 (REMARK=0, VINA=1, RESULT:=2, SCORE=3)
                    # A veces puede variar si hay espacios extra, buscamosel primer numero
                    best_score = float(partes[3])
                    break # Solo nos interesa el primer modelo (el mejor)
    except Exception as e:
        print(f"Error leyendo {nombre_archivo}: {e}")

    # 3. CALCULAR SMILES CON OPENBABEL (Usando el archivo dockeado)
    smiles = "N/A"
    if CALCULAR_SMILES:
        try:
            # -ipdbqt: entrada, -osmi: salida smiles
            resultado = subprocess.check_output(
                ['obabel', '-ipdbqt', ruta_archivo, '-osmi'], 
                stderr=subprocess.DEVNULL
            )
            # Limpiamos el output
            smiles = resultado.decode('utf-8').split()[0]
        except Exception:
            smiles = "Fallo_OpenBabel"

    # 4. Generar Link de ZINC
    # Intentamos limpiar el ID para el link (quitamos _HEAD, _STEM, _out para buscar en ZINC)
    zinc_id_clean = id_compuesto.split('_')[0] # Asume que el ID es lo primero antes del guion bajo
    if "ZINC" not in zinc_id_clean and "ZINC" in id_compuesto:
         # Si el split falló, intentamos buscar el string ZINC
         import re
         match = re.search(r'ZINC\w+', id_compuesto)
         if match: zinc_id_clean = match.group(0)

    link_zinc = f"https://cartblanche22.docking.org/search/zincid:{zinc_id_clean}"

    # Guardamos si encontramos score
    if best_score is not None:
        datos.append([id_compuesto, best_score, smiles, link_zinc])

    # Mostrar progreso cada 1000 archivos
    if i % 1000 == 0:
        print(f"Procesados: {i}/{total}")

# --- ORDENAR Y GUARDAR ---
print("Ordenando por mejor energía (más negativa)...")
datos.sort(key=lambda x: x[1])

print(f"Guardando en {archivo_salida}...")
with open(archivo_salida, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ID_Archivo", "Docking_Score", "SMILES", "Link_ZINC"])
    writer.writerows(datos)

print("¡Listo! Tabla generada exitosamente.")
