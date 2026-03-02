import os
import shutil
import random
import glob
import subprocess
from pathlib import Path
import time

# ==========================================
# CONFIGURACIÓN
# ==========================================
DIRECTORIO_TRABAJO = "/Users/mariapayro/Downloads/Hemaglutinina/ligandos_variados"
ARCHIVO_CURL = "ZINC22-downloader-3D-pdbqt.tgz.curl" 

CARPETA_1 = "Todos_Los_Ligandos_PDBQT"
CARPETA_2 = "Muestra_40K_Docking"
TXT_SALIDA = "Lista_40K_IDs.txt"
MUESTRA_TAMAÑO = 40000

def main():
    inicio_total = time.time()
    
    try:
        os.chdir(DIRECTORIO_TRABAJO)
        print(f"📁 Trabajando directamente en: {os.getcwd()}")
    except FileNotFoundError:
        print(f"❌ ERROR: La ruta '{DIRECTORIO_TRABAJO}' no existe.")
        return

    if not os.path.exists(ARCHIVO_CURL):
        print(f"❌ ERROR: No se encuentra el archivo '{ARCHIVO_CURL}'.")
        return
        
    # 1. DESCARGAR LOS PAQUETES .TGZ
    print("\n=================================================")
    print(" 1. DESCARGANDO PAQUETES DE ZINC22")
    print("=================================================")
    #subprocess.run(['bash', ARCHIVO_CURL])
    # la linea anterior se comenta cuando ya no se quiere descargar nada,
    # para solo trabajar con los .tgz existentes
    print("✓ Descargas completadas.")

    # 2. EXTRAER Y APLANAR EN CARPETA 1
    print("\n=================================================")
    print(" 2. EXTRAYENDO LIGANDOS A CARPETA 1")
    print("=================================================")
    os.makedirs(CARPETA_1, exist_ok=True)
    
    archivos_tgz = list(Path('.').rglob("*.tgz"))
    
    if not archivos_tgz:
        print("❌ ERROR: No se encontraron archivos .tgz después de la descarga.")
        return
        
    for tgz in archivos_tgz:
        print(f"Extrayendo {tgz.name}...")
        subprocess.run(['tar', '-xzf', str(tgz), '-C', CARPETA_1])
        
    print("\nAplanando subcarpetas internas...")
    archivos_extraidos = list(Path(CARPETA_1).rglob("*.pdbqt"))
    for archivo in archivos_extraidos:
        if archivo.parent != Path(CARPETA_1):
            destino = os.path.join(CARPETA_1, archivo.name)
            shutil.move(str(archivo), destino)
            
    print("✓ Extracción y aplanamiento terminados.")

    # 3. SELECCIÓN ALEATORIA A CARPETA 2
    print("\n=================================================")
    print(f" 3. SELECCIONANDO MUESTRA DE {MUESTRA_TAMAÑO}")
    print("=================================================")
    os.makedirs(CARPETA_2, exist_ok=True)
    
    todos_en_carpeta_1 = glob.glob(os.path.join(CARPETA_1, "*.pdbqt"))
    cantidad_a_sacar = min(MUESTRA_TAMAÑO, len(todos_en_carpeta_1))
    
    print(f"Total disponible: {len(todos_en_carpeta_1)} ligandos.")
    print(f"Moviendo {cantidad_a_sacar} ligandos aleatorios a Carpeta 2...")
    
    seleccionados = random.sample(todos_en_carpeta_1, cantidad_a_sacar)
    for ruta in seleccionados:
        destino = os.path.join(CARPETA_2, os.path.basename(ruta))
        shutil.move(ruta, destino)
        
    print("✓ Selección completada.")

	# 4. LIMPIEZA Y COMPRESIÓN (OPTIMIZADO PARA MAC)
    print("\n=================================================")
    print(" 4. COMPRIMIENDO RESPALDO Y LIMPIANDO")
    print("=================================================")
    
    nombre_archivo_final = f"{CARPETA_1}.tar.gz"
    print(f"Comprimiendo {CARPETA_1} usando el motor nativo de la Mac (súper rápido)...")
    
    # Magia pura: Le pedimos a la Mac que lo haga directamente en lugar de usar Python
    subprocess.run(['tar', '-czf', nombre_archivo_final, CARPETA_1])
    
    print("Eliminando la Carpeta 1 descomprimida...")
    shutil.rmtree(CARPETA_1)
    
    print("Eliminando los archivos .tgz originales descargados...")
    for tgz in archivos_tgz:
        try:
            os.remove(str(tgz))
        except FileNotFoundError:
            pass # Por si alguno ya se había borrado
        
    print("Borrando carpetas vacías residuales...")
    for item in os.listdir('.'):
        if os.path.isdir(item) and item not in [CARPETA_2, CARPETA_1]:
            try:
                shutil.rmtree(item)
            except Exception:
                pass
        
    print("✓ Espacio en disco recuperado y limpieza terminada.")

    # 5. GENERAR EL TXT CON IDs (SOLO DE CARPETA 2)
    print("\n=================================================")
    print(" 5. GENERANDO LISTA DE IDs")
    print("=================================================")
    # Aquí buscamos explícitamente y únicamente en la CARPETA 2
    archivos_carpeta_2 = glob.glob(os.path.join(CARPETA_2, "*.pdbqt"))
    
    print(f"Extrayendo IDs limpios de los {len(archivos_carpeta_2)} archivos seleccionados...")
    
    with open(TXT_SALIDA, 'w') as txtfile:
        for ruta in archivos_carpeta_2:
            nombre_archivo = os.path.basename(ruta)
            
            # 1. Quitamos el '.pdbqt' (ej. 'ZINC7j0000001wX9.0.O.pdbqt' -> 'ZINC7j0000001wX9.0.O')
            sin_extension = nombre_archivo.replace(".pdbqt", "")
            
            # 2. Cortamos por el punto y nos quedamos solo con la primera parte
            # (ej. 'ZINC7j0000001wX9.0.O' -> 'ZINC7j0000001wX9')
            id_limpio = sin_extension.split('.')[0]
            
            # 3. Lo escribimos en el txt
            txtfile.write(f"{id_limpio}\n")

    tiempo_total = (time.time() - inicio_total) / 60
    print("\n=================================================")
    print(f" 🚀 PIPELINE COMPLETADO EN {tiempo_total:.2f} MINUTOS! ")
    print(f" - Carpeta docking lista: {CARPETA_2}/")
    print(f" - Respaldo comprimido: {CARPETA_1}.zip")
    print(f" - Archivo de IDs generado: {TXT_SALIDA}")
    print("=================================================")

if __name__ == '__main__':
    main()