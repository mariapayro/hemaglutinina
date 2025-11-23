#!/bin/bash
# Script por Gemini:
# Paso 2 para la descarga de 35,000 compuestos:
# Este script extrae y descarga las 35,000 moléculas individuales listas para el docking 
# tras la descarga de 5 paquetes desde script "1-descarga_aleatoria.sh"

echo "--- Procesando paquetes descargados ---"

# 1. Descomprimir los archivos .gz que bajamos
gunzip *.gz

# 2. Crear carpeta final
mkdir -p biblioteca_final_35k

# 3. ZINC en formato AutoDock suele venir en archivos grandes que contienen muchas moléculas.
#    Necesitamos dividirlos o leerlos.
#    PERO, el formato pdbqt de ZINC a veces viene todo junto.

echo "Consolidando todo en un archivo gigante temporal..."
cat *.pdbqt > todo_junto.tmp

# El separador de moléculas en PDBQT es "MODEL" y "ENDMDL"
# Vamos a usar 'csplit' o una lógica más simple para no complicarte con comandos oscuros.
# La forma más segura en bioinformática básica sin scripts de Python complejos:

echo "Dividiendo en archivos individuales (esto puede tardar unos minutos)..."
# Usamos awk para separar el archivo gigante en pequeñitos basado en la etiqueta "MODEL"
awk '/^MODEL/{i++} {print > ("biblioteca_final_35k/ligando_" i ".pdbqt")}' todo_junto.tmp

echo "--- Seleccionando 35,000 al azar ---"
cd biblioteca_final_35k

# Contamos cuántos salieron
TOTAL=$(ls -1 | wc -l)
echo "Se extrajeron $TOTAL moléculas en total."

# Si hay más de 35,000, borramos el exceso aleatoriamente
if [ $TOTAL -gt 35000 ]; then
    NUM_A_BORRAR=$((TOTAL - 35000))
    echo "Borrando $NUM_A_BORRAR moléculas sobrantes para dejar exactamente 35,000..."
    ls | shuf -n $NUM_A_BORRAR | xargs rm
fi

echo "¡PROCESO TERMINADO!"
echo "Tu carpeta 'biblioteca_final_35k' tiene exactamente $(ls | wc -l) compuestos listos para Vina."

# Limpieza
cd ..
rm todo_junto.tmp
