#!/bin/bash

# --- DIRECTORIOS ---
# Definir dónde está instalado Vina-GPU (donde están las carpetas 'OpenCL', 'src', etc.)
VINA_HOME="/home/bioinfo/Vina-GPU" 
VINA_BIN="./Vina-GPU"  # Ejecutable relativo al home

# Rutas de datos
LIGAND_FOLDER="/home/bioinfo/Vina-GPU/docking_35000/35000_ligandos/35000_pdbqt_1"
OUTPUT_FOLDER="/home/bioinfo/Vina-GPU/docking_35000/35000_ligandos/RESULTADOS_1_t1000_c30"
# El config se creará temporalmente
CONFIG_FILE="config_temp.txt"

# Crear carpeta de salida
mkdir -p "$OUTPUT_FOLDER"

echo "============================================="
echo " CORRIGIENDO ENTORNO DE EJECUCIÓN"
echo "============================================="

# 1. Moverse al directorio de Vina-GPU
cd "$VINA_HOME" || { echo "No se encuentra el directorio $VINA_HOME"; exit 1; }

echo "Directorio actual: $(pwd)"

# 2. Archivo CONFIG 
# He reducido la caja a 30x30x30 para evitar el crash por memoria y la advertencia.
cat << EOF > "$CONFIG_FILE"
receptor = /home/bioinfo/Vina-GPU/PRUEBAS/receptor_Hemaglutinina.pdbqt

center_x = -22.069
center_y = -18.249
center_z = -2.015

size_x = 30
size_y = 30
size_z = 30

thread = 1000
search_depth = 10
EOF

# 3. BUCLE DE EJECUCIÓN
# Iterar sobre los ligandos usando rutas absolutas para input/output
count=0
for ligand_path in $LIGAND_FOLDER/*.pdbqt; do

    filename=$(basename "$ligand_path")
    base_name="${filename%.*}"
    
    ((count++))
    echo "Procesando: $base_name"

    # EJECUTAR VINA-GPU
    $VINA_BIN \
        --config "$CONFIG_FILE" \
        --ligand "$ligand_path" \
        --out "$OUTPUT_FOLDER/${base_name}_out.pdbqt"

done

echo "============================================="
echo " ¡PROCESO TERMINADO!"
echo "============================================="
