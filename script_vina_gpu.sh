#!/bin/bash

# --- RUTAS Y EJECUTABLE ---
VINA_GPU_EXEC="./Vina-GPU"  # Asegúrate de que esta sea la ruta correcta a tu ejecutable
LIGAND_FOLDER="25_ligandos_prueba"
OUTPUT_FOLDER="25_RESULTADOS_DOCKING_prueba"
LOG_FOLDER="25_LOGS_prueba"

# --- DATOS DEL RECEPTOR Y LA CAJA (Copiados de tu config) ---
RECEPTOR="receptor_Hemaglutinina.pdbqt"
CENTER_X="-10.718"
CENTER_Y="-3.35"
CENTER_Z="-5.871"
SIZE_X="155"
SIZE_Y="100"
SIZE_Z="105"

# --- PARÁMETROS VINA-GPU ---
# Vina-GPU usa 'thread' en lugar de exhaustiveness a veces, 
# pero si tu version soporta exhaustiveness, úsalo.
THREAD=8000  # Valor típico para GPU (equivalente a exhaustiveness alto)
SEARCH_DEPTH=40 # A veces usado en versiones nuevas

# Crear carpetas
mkdir -p $OUTPUT_FOLDER
mkdir -p $LOG_FOLDER

# Verificación
if [ ! -f "$VINA_GPU_EXEC" ]; then
    echo "ERROR: No encuentro el ejecutable $VINA_GPU_EXEC"
    exit 1
fi

echo "============================================="
echo " INICIANDO CRIBADO CON VINA-GPU"
echo "============================================="
start_time=$(date +%s)

count=0
total=$(find $LIGAND_FOLDER -name "*.pdbqt" | wc -l)

# BUCLE
for ligand in $LIGAND_FOLDER/*.pdbqt; do
    
    # Nombres
    filename=$(basename "$ligand")
    base_name="${filename%.*}"
    
    ((count++))
    printf "\rProcesando $count de $total: $base_name"

    # 1. DEFINIMOS RUTAS DE SALIDA
    output_file="$OUTPUT_FOLDER/${base_name}_out.pdbqt"
    config_temp="temp_${base_name}.txt"

    # 2. CREAMOS EL ARCHIVO DE CONFIGURACIÓN DINÁMICO
    # Vina-GPU necesita leer el ligando y el output DESDE el archivo de texto
    cat > $config_temp <<EOF
receptor = $RECEPTOR
ligand = $ligand
out = $output_file

center_x = $CENTER_X
center_y = $CENTER_Y
center_z = $CENTER_Z

size_x = $SIZE_X
size_y = $SIZE_Y
size_z = $SIZE_Z

thread = $THREAD
num_modes = 20
energy_range = 3
EOF

    # 3. EJECUTAMOS VINA-GPU
    # La salida estándar la mandamos al log
    $VINA_GPU_EXEC --config $config_temp > "$LOG_FOLDER/${base_name}.log"

    # 4. LIMPIEZA
    # Borramos el archivo de configuración temporal para no llenar la carpeta de basura
    rm $config_temp

done

end_time=$(date +%s)
elapsed=$(( end_time - start_time ))

echo ""
echo "============================================="
echo " ¡CRIBADO GPU COMPLETADO!"
echo " Tiempo total: $((elapsed / 60)) minutos."
echo "============================================="
