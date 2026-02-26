import os
import glob
import csv
import subprocess

# --- CONFIGURACIÓN ---
carpeta_logs = "LOGS"
carpeta_ligandos = "500_ligandos_prueba"
archivo_salida = "Tabla_Resultados_Final.csv" 

print("--- Iniciando Análisis y Cálculo de SMILES ---")

datos = []
archivos_log = glob.glob(os.path.join(carpeta_logs, "*.log"))
total = len(archivos_log)
print(f"Se encontraron {total} reportes. Procesando...")

for i, log_path in enumerate(archivos_log):
    # 1. Obtener ID
    nombre_archivo = os.path.basename(log_path)
    id_compuesto = nombre_archivo.replace(".log", "") 
    
    # 2. Extraer Docking Score (Energía)
    best_score = None
    try:
        with open(log_path, 'r') as f:
            for linea in f:
                if linea.strip().startswith("1 "):
                    best_score = float(linea.split()[1])
                    break
    except:
        pass

    # 3. CALCULAR SMILES CON OPENBABEL
    # Buscamos el archivo original .pdbqt
    ruta_ligando = os.path.join(carpeta_ligandos, id_compuesto + ".pdbqt")
    smiles = "Error_Calculo"
    
    if os.path.exists(ruta_ligando):
        try:
            # Ejecutamos el comando 'obabel' desde Python
            # -ipdbqt: formato de entrada
            # -osmi: formato de salida (SMILES)
            resultado = subprocess.check_output(
                ['obabel', '-ipdbqt', ruta_ligando, '-osmi'], 
                stderr=subprocess.DEVNULL # Ocultamos avisos técnicos de babel
            )
            
            # OpenBabel devuelve algo como: "C1CCCCC1\tNombreArchivo\n"
            # Limpiamos el texto para quedarnos solo con la fórmula
            smiles = resultado.decode('utf-8').split()[0]
            
        except Exception as e:
            smiles = "Fallo_OpenBabel"
    else:
        smiles = "Archivo_PDBQT_No_Encontrado"

    # 4. Generar Link de ZINC (útil para búsqueda manual)
    # ZINC22 usa URLs tipo search, pero la búsqueda por ID en CartBlanche es segura
    link_zinc = f"https://cartblanche22.docking.org/search/zincid:{id_compuesto}"

    # Guardamos todo
    if best_score is not None:
        datos.append([id_compuesto, best_score, smiles, link_zinc])

    # Mostrar progreso cada 500 archivos
    if i % 500 == 0:
        print(f"Procesados: {i}/{total}")

# --- ORDENAR Y GUARDAR ---
print("Ordenando por mejor energía (más negativa)...")
datos.sort(key=lambda x: x[1])

print(f"Guardando en {archivo_salida}...")
with open(archivo_salida, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ID", "Docking_Score", "SMILES_Calculado", "Link_ZINC"])
    writer.writerows(datos)

print("¡Listo! Tabla generada exitosamente.")
