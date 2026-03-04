import os
import csv

# ==========================================
# CONFIGURACIÓN DE RUTAS (Linux Server)
# ==========================================
DIR_OUTPUTS = "/home/bioinfo/Vina-GPU/CRIBADO_40k_ligandos_aleatorios/Outputs"
CSV_ZINC = "/home/bioinfo/Vina-GPU/CRIBADO_40k_ligandos_aleatorios/tabla_zinc_id_smiles.csv"

# Nombres de los archivos que se van a generar
CSV_FINAL_COMPLETO = "40k_dockscore_id_smiles.csv"     # Columnas: docking_score, zinc_id, smiles
CSV_FINAL_CORTO = "40k_swifty_dockscore_smiles.csv"    # Columnas: docking_score, smiles

def main():
    print("1. Cargando la base de datos confiable de ZINC22...")
    diccionario_zinc = {}
    
    # Leemos el CSV oficial y lo convertimos en un diccionario súper rápido para buscar
    try:
        with open(CSV_ZINC, 'r') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                # Quitamos espacios en blanco por si acaso
                zinc_id = fila['zinc_id'].strip()
                smiles = fila['smiles'].strip()
                diccionario_zinc[zinc_id] = smiles
        print(f"   ✓ {len(diccionario_zinc)} IDs confiables cargados en memoria.")
    except FileNotFoundError:
        print(f"❌ ERROR: No se encontró el archivo confiable en {CSV_ZINC}")
        return

    print("\n2. Extrayendo los mejores scores de los resultados de Vina-GPU...")
    resultados = []
    archivos_procesados = 0
    archivos_no_encontrados = 0

    # os.scandir lee el disco duro sin colapsar la RAM
    for entrada in os.scandir(DIR_OUTPUTS):
        if entrada.is_file() and entrada.name.endswith('.pdbqt'):
            # Limpiamos el nombre: ZINCmv00000bUkDK.2.O_out.pdbqt -> ZINCmv00000bUkDK
            id_limpio = entrada.name.split('.')[0]

            # Verificamos si ese ID existe en nuestra tabla oficial
            if id_limpio in diccionario_zinc:
                smiles_oficial = diccionario_zinc[id_limpio]
                mejor_score = None

                # Abrimos el archivo .pdbqt y buscamos el score
                with open(entrada.path, 'r') as f_pdbqt:
                    for linea in f_pdbqt:
                        # Vina siempre pone el score en esta línea
                        if linea.startswith("REMARK VINA RESULT:"):
                            partes = linea.split()
                            # El score siempre es el primer número después de "RESULT:"
                            if len(partes) >= 4:
                                mejor_score = partes[3]
                            break # Rompemos el ciclo porque solo queremos el primer score (el mejor)

                if mejor_score is not None:
                    resultados.append((mejor_score, id_limpio, smiles_oficial))
                    archivos_procesados += 1
            else:
                archivos_no_encontrados += 1

    print(f"   ✓ Scores extraídos de {archivos_procesados} ligandos.")
    if archivos_no_encontrados > 0:
        print(f"  Nota: {archivos_no_encontrados} archivos no hicieron match con el CSV oficial.")

    print("\n3. Ordenando de mejor a peor afinidad...")
    # Ordenamos de menor a mayor (los números más negativos son mejores en Vina)
    resultados.sort(key=lambda x: float(x[0]))

    print("\n4. Generando los archivos CSV finales...")
    
    # Generar Archivo 1 (docking_score, zinc_id, smiles)
    with open(CSV_FINAL_COMPLETO, 'w', newline='') as f1:
        escritor = csv.writer(f1)
        escritor.writerow(['docking_score', 'zinc_id', 'smiles'])
        escritor.writerows(resultados)

    # Generar Archivo 2 (docking_score, smiles)
    with open(CSV_FINAL_CORTO, 'w', newline='') as f2:
        escritor = csv.writer(f2)
        escritor.writerow(['docking_score', 'smiles'])
        # Escribimos solo la primera y tercera columna
        for res in resultados:
            escritor.writerow([res[0], res[2]])

    print(f"¡Listo! Archivos creados exitosamente:")
    print(f"   - {CSV_FINAL_COMPLETO}")
    print(f"   - {CSV_FINAL_CORTO}")

if __name__ == '__main__':
    main()
