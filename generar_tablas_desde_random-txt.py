import csv

# --- CONFIGURACIÓN ---
ARCHIVO_ENTRADA = "zinc22-random-output.txt"  # <--- CAMBIA ESTO POR EL NOMBRE REAL DE TU TXT
ARCHIVO_SALIDA_1 = "input_id_smiles.csv"
ARCHIVO_SALIDA_2 = "input_numeros_smiles.csv"

print(f"--- Procesando {ARCHIVO_ENTRADA} ---")

try:
    with open(ARCHIVO_ENTRADA, 'r') as f_in, \
         open(ARCHIVO_SALIDA_1, 'w', newline='') as f_out1, \
         open(ARCHIVO_SALIDA_2, 'w', newline='') as f_out2:
        
        # Detectamos automáticamente si el archivo usa pestañas o espacios
        primera_linea = f_in.readline()
        f_in.seek(0) # Regresamos al inicio
        
        delimitador = '\t' if '\t' in primera_linea else ' '
        lector = csv.reader(f_in, delimiter=delimitador)
        
        # Preparamos los escritores
        escritor1 = csv.writer(f_out1)
        escritor2 = csv.writer(f_out2)
        
        # --- ESCRIBIR ENCABEZADOS ---
        # Archivo 1: ID, SMILES
        escritor1.writerow(["ID", "SMILES"])
        
        # Archivo 2: (Vacio), smiles
        # El usuario pidió: 1ra col sin nombre, 2da "smiles"
        escritor2.writerow(["", "smiles"])
        
        contador = 0
        
        # Saltamos el encabezado del TXT original si lo tiene
        # Verificamos si la primera linea tiene palabras como "Tranche" o "SMILES"
        encabezado_original = next(lector)
        if "smiles" not in encabezado_original[0].lower() and "zinc" not in encabezado_original[0].lower():
             # Si no parece encabezado, regresamos la linea (caso raro)
             # Pero asumo que ZINC siempre trae encabezado, así que lo omitimos seguro.
             pass
        else:
             # Si la primera linea ERA encabezado, ya la consumimos con next(), seguimos.
             pass

        # --- PROCESAMIENTO ---
        for linea in lector:
            # El archivo tiene 3 columnas. El usuario dice: Tranche, ID, SMILES
            # A veces ZINC viene: SMILES, ID, Tranche. 
            # Vamos a identificar dinámicamente qué es el SMILES (el texto largo) y qué es el ID (ZINC...)
            
            partes = [x for x in linea if x.strip()] # Limpiar espacios vacios
            
            if len(partes) < 2: continue
            
            smiles = ""
            zinc_id = ""
            
            # Lógica simple para identificar columnas:
            for p in partes:
                if p.startswith("ZINC"):
                    zinc_id = p
                elif len(p) > 5 and not p.startswith("ZINC") and not p.startswith("H"): 
                    # Los SMILES suelen ser largos y no empiezan con HxxPxx (eso es el tranche)
                    smiles = p
            
            # Si falló la detección automática, usamos posiciones fijas (ajusta si es necesario)
            if not smiles: smiles = partes[-1] # Asumimos SMILES al final
            if not zinc_id: zinc_id = partes[1] # Asumimos ID en medio
            
            # --- GUARDAR ---
            
            # Archivo 1: ID, SMILES
            escritor1.writerow([zinc_id, smiles])
            
            # Archivo 2: Numero, smiles
            escritor2.writerow([contador, smiles])
            
            contador += 1
            
            if contador % 100000 == 0:
                print(f"Procesados: {contador}...", end='\r')

    print(f"\n¡LISTO! Se generaron 2 archivos con {contador} compuestos.")
    print(f"1. {ARCHIVO_SALIDA_1} (ID, SMILES)")
    print(f"2. {ARCHIVO_SALIDA_2} (Índice, smiles)")

except FileNotFoundError:
    print(f"ERROR: No encuentro el archivo '{ARCHIVO_ENTRADA}'. Revisa el nombre.")