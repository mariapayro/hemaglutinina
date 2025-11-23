#!/bin/bash
# Script por Gemini:
# Paso 1 para la descarga de 35,000 compuestos:
# Este script extrae solo 5 líneas aleatorias que permitirá la obtención de 
# ~100,000 compuestos brutos para luego filtrar tus 35,000 finales.

# NOMBRE DE TU ARCHIVO ORIGINAL (cámbialo si es necesario)
ARCHIVO_ORIGINAL="ZINC22-downloader-3D-pdbqt.tgz.wget" 

echo "--- Seleccionando 5 paquetes al azar del script de descarga ---"

# 1. Filtramos solo las líneas que contienen la instrucción de descarga (wget o curl)
# 2. Revolvemos (shuf)
# 3. Nos quedamos con las primeras 5 líneas (-n 5)
# 4. Guardamos en un nuevo script temporal

grep "http" $ARCHIVO_ORIGINAL | shuf -n 5 > descargar_mini.sh

echo "--- Descargando los paquetes seleccionados ---"
# Damos permisos y ejecutamos la descarga pequeña
chmod +x descargar_mini.sh
bash descargar_mini.sh

echo "Descarga terminada. Ahora tienes los archivos .gz necesarios."
