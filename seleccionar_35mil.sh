#!/bin/bash

# --- CONFIGURACIÓN ---
CARPETA_TRABAJO="procesamiento_temporal"
CARPETA_FINAL="LIGANDOS_35K_LISTOS"

echo "============================================="
echo " PASO 1: PREPARANDO EL ENTORNO"
echo "============================================="
mkdir -p $CARPETA_TRABAJO
mkdir -p $CARPETA_FINAL

echo "Descomprimiendo archivos (esto puede tardar un poco)..."
# Descomprimimos los .gz que descargaste
gunzip -k *.gz  
# (-k mantiene el original por si algo sale mal, si tienes poco espacio 
quita el -k)

echo "============================================="
echo " PASO 2: SEPARANDO MOLÉCULAS INDIVIDUALES"
echo "============================================="
echo "Este paso es intenso. Estamos 'cortando' los archivos grandes en 
miles pequeños..."

# Unimos todos los pdbqt en un flujo y AWK los separa cada vez que ve 
"MODEL"
# Esto creará miles de archivitos en la carpeta temporal
cat *.pdbqt | awk '/^MODEL/{i++} {print > ("procesamiento_temporal/lig_" i 
".pdbqt")}'

# Contamos cuántos salieron
TOTAL_DISPONIBLES=$(ls $CARPETA_TRABAJO | wc -l)
echo "¡Separación terminada!"
echo "Total de moléculas encontradas en tus descargas: $TOTAL_DISPONIBLES"

echo "============================================="
echo " PASO 3: SELECCIÓN ALEATORIA DE 35,000"
echo "============================================="

if [ "$TOTAL_DISPONIBLES" -lt 35000 ]; then
    echo "ALERTA: Descargaste menos de 35,000 moléculas 
($TOTAL_DISPONIBLES)."
    echo "Se moverán TODAS a la carpeta final."
    mv $CARPETA_TRABAJO/* $CARPETA_FINAL/
else
    echo "Seleccionando 35,000 ganadores al azar..."
    
    # Entramos a la carpeta temporal
    cd $CARPETA_TRABAJO
    
    # 1. Listamos todos
    # 2. Revolvemos (shuf)
    # 3. Tomamos los primeros 35,000
    # 4. Los movemos a la carpeta final (../ significa "una carpeta 
atrás")
    ls | shuf -n 35000 | xargs -I {} mv {} ../$CARPETA_FINAL/
    
    cd ..
    echo "Limpiando archivos temporales sobrantes..."
    rm -rf $CARPETA_TRABAJO
fi

echo "============================================="
echo " ¡LISTO! PROCESO COMPLETADO"
echo "============================================="
echo "Tus 35,000 compuestos están en la carpeta: $CARPETA_FINAL"
echo "Ya puedes borrar los archivos .pdbqt y .gz sueltos si quieres 
ahorrar espacio."
