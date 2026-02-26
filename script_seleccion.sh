#!/bin/bash

# --- CONFIGURACIÓN ---
#CARPETA_TEMP="TEMPORAL"
CARPETA_FINAL="../LIGANDOS_FINALES"

# Limpieza inicial
#rm -rf "$CARPETA_FINAL"
#mkdir -p "$CARPETA_TEMP" "$CARPETA_FINAL"

#echo "============================================="
#echo " 1. DESCOMPRIMIENDO PAQUETES .TGZ"
#echo "============================================="

#for archivo in *.tgz; do
#    echo "Procesando $archivo..."
#    tar -xzf "$archivo" -C "$CARPETA_TEMP/"
#done

echo "============================================="
echo " 2. RECOPILANDO Y SELECCIONANDO (Mac Version)"
echo "============================================="

#cd "$CARPETA_TEMP"

find . -name "*.pdbqt" > lista_todos.txt

echo "Revolviendo aleatoriamente y seleccionando 5,000..."

sort -R lista_todos.txt | head -n 5000 > 5mil_aleatorios_seleccionados.txt

echo "============================================="
echo " 3. MOVIENDO A CARPETA FINAL"
echo "============================================="

count=0
while IFS= read -r ruta_archivo; do
    mv "$ruta_archivo" "../$CARPETA_FINAL/"
    ((count++))
done > seleccionados.txt

#cd ..
#rm -rf "$CARPETA_TEMP"

echo "PROCESO TERMINADO."
echo "Se han movido $count compuestos a '$CARPETA_FINAL'."

