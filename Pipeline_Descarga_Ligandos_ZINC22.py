import os
import random
import subprocess
from pathlib import Path
import time
import re

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
        
    # 1. OPTIMIZAR CURL Y DESCARGAR
    print("\n=================================================")
    print(" 1. DESCARGANDO PAQUETES DE ZINC22 (MODO TURBO)")
    print("=================================================")
    
    with open(ARCHIVO_CURL, 'r') as f:
        script_curl = f.read()
        
    # A) Quitamos los reintentos infinitos
    script_curl = re.sub(r'--retry\s+\d+', '--retry 0', script_curl)
    
    # B) ¡NUEVO! Le inyectamos los límites de tiempo estrictos a cada línea de descarga.
    # Si el servidor no responde en 15 seg, o la descarga dura más de 60 seg, la aborta y sigue.
    script_curl = script_curl.replace('curl ', 'curl --connect-timeout 15 --max-time 60 ')
    
    archivo_temporal = "descarga_rapida.curl"
    with open(archivo_temporal, 'w') as f:
        f.write(script_curl)
        
    subprocess.run(['bash', archivo_temporal])
    if os.path.exists(archivo_temporal):
        os.remove(archivo_temporal)
    print("✓ Descargas completadas (archivos lentos o trabados fueron ignorados).")

    # 2. EXTRAER Y APLANAR (CON BASH)
    print("\n=================================================")
    print(" 2. EXTRAYENDO Y APLANANDO (MODO TURBO)")
    print("=================================================")
    os.makedirs(CARPETA_1, exist_ok=True)
    
    archivos_tgz = list(Path('.').rglob("*.tgz"))
    if not archivos_tgz:
        print("❌ ERROR: No se encontraron archivos .tgz después de la descarga.")
        return
        
    for tgz in archivos_tgz:
        print(f"Extrayendo {tgz.name}...")
        subprocess.run(['tar', '-xzf', str(tgz), '-C', CARPETA_1])
        
    print("\nAplanando subcarpetas usando Bash nativo...")
    # Ejecutamos comando UNIX find+mv para sacar todo de las subcarpetas a la raíz de CARPETA_1
    comando_aplanar = f'find "{CARPETA_1}" -mindepth 2 -type f -name "*.pdbqt" -exec mv {{}} "{CARPETA_1}/" \;'
    subprocess.run(comando_aplanar, shell=True)
    
    # Borrar las subcarpetas que quedaron vacías dentro de CARPETA_1
    subprocess.run(f'find "{CARPETA_1}" -type d -empty -delete', shell=True)
            
    print("✓ Extracción y aplanamiento terminados.")

    # 3. SELECCIÓN ALEATORIA (MEMORIA OPTIMIZADA)
    print("\n=================================================")
    print(f" 3. SELECCIONANDO MUESTRA DE {MUESTRA_TAMAÑO}")
    print("=================================================")
    os.makedirs(CARPETA_2, exist_ok=True)
    
    print("Escaneando archivos (sin colapsar la RAM)...")
    # os.scandir es muchísimo más rápido y consume menos RAM que glob.glob
    todos_archivos = [f.path for f in os.scandir(CARPETA_1) if f.name.endswith('.pdbqt')]
    
    cantidad_a_sacar = min(MUESTRA_TAMAÑO, len(todos_archivos))
    print(f"Total disponible: {len(todos_archivos)} ligandos.")
    print(f"Moviendo {cantidad_a_sacar} ligandos aleatorios a Carpeta 2...")
    
    # Movemos usando Bash mv para mayor velocidad
    seleccionados = random.sample(todos_archivos, cantidad_a_sacar)
    for ruta in seleccionados:
        subprocess.run(['mv', ruta, f'{CARPETA_2}/'])
        
    print("✓ Selección completada.")

    # 4. LIMPIEZA Y COMPRESIÓN (COMANDOS UNIX)
    print("\n=================================================")
    print(" 4. COMPRIMIENDO RESPALDO Y LIMPIANDO (MODO DIOS)")
    print("=================================================")
    
    nombre_archivo_final = f"{CARPETA_1}.tar.gz"
    print(f"Comprimiendo {CARPETA_1} a formato nativo Mac...")
    subprocess.run(['tar', '-czf', nombre_archivo_final, CARPETA_1])
    
    print("Fulminando la Carpeta 1 original y archivos temporales con 'rm -rf'...")
    # Magia de terminal: borramos carpeta pesada y todos los .tgz en un segundo
    subprocess.run(f'rm -rf "{CARPETA_1}"', shell=True)
    subprocess.run('rm -f *.tgz', shell=True)
    
    # Borrar cualquier carpeta basura en la raíz (ej. carpetas H10, P140 que dejó curl)
    # Protegiendo explícitamente nuestra Carpeta 2
    comando_limpieza_carpetas = f'find . -maxdepth 1 -type d ! -name "." ! -name "{CARPETA_2}" -exec rm -rf {{}} +'
    subprocess.run(comando_limpieza_carpetas, shell=True)
        
    print("✓ Espacio en disco recuperado y limpieza terminada.")

    # 5. GENERAR EL TXT CON IDs
    print("\n=================================================")
    print(" 5. GENERANDO LISTA DE IDs")
    print("=================================================")
    
    archivos_carpeta_2 = [f.name for f in os.scandir(CARPETA_2) if f.name.endswith('.pdbqt')]
    print(f"Extrayendo IDs limpios de los {len(archivos_carpeta_2)} archivos seleccionados...")
    
    with open(TXT_SALIDA, 'w') as txtfile:
        for nombre_archivo in archivos_carpeta_2:
            sin_extension = nombre_archivo.replace(".pdbqt", "")
            id_limpio = sin_extension.split('.')[0]
            txtfile.write(f"{id_limpio}\n")

    tiempo_total = (time.time() - inicio_total) / 60
    print("\n=================================================")
    print(f" 🚀 PIPELINE COMPLETADO EN {tiempo_total:.2f} MINUTOS! ")
    print(f" - Carpeta docking lista: {CARPETA_2}/")
    print(f" - Respaldo comprimido: {nombre_archivo_final}")
    print(f" - Archivo de IDs generado: {TXT_SALIDA}")
    print("=================================================")

if __name__ == '__main__':
    main()