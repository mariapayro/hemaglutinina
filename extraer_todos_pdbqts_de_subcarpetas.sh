#!/bin/bash

# --- CONFIGURACIÓN DE RUTAS ---
# Usamos rutas absolutas para mayor seguridad
CARPETA_ORIGEN="/Users/mariapayro/Downloads/Hemaglutinina/TEMPORAL"
CARPETA_DESTINO="/Users/mariapayro/Downloads/Hemaglutinina/37_mil_ligandos_grandes"

# --- PREPARACIÓN ---
# Crear carpeta destino si no existe
mkdir -p "$CARPETA_DESTINO"

echo "============================================="
echo " 1. INICIANDO MIGRACIÓN MASIVA"
echo "============================================="
echo "Origen:  $CARPETA_ORIGEN"
echo "Destino: $CARPETA_DESTINO"

# Nos aseguramos de entrar a la carpeta de origen
cd "$CARPETA_ORIGEN" || { echo "Error: No existe la carpeta origen"; exit 1; }

echo "============================================="
echo " 2. BUSCANDO TODOS LOS ARCHIVOS .pdbqt"
echo "============================================="

# Buscamos recursivamente en todas las subcarpetas
# -type f asegura que solo listemos archivos, no carpetas
find . -type f -name "*.pdbqt" > lista_completa.txt

total=$(wc -l < lista_completa.txt)
echo "¡Encontrados $total archivos dispersos!"
echo "Comenzando a mover (esto puede tardar un poco)..."

echo "============================================="
echo " 3. MOVIENDO A CARPETA ÚNICA"
echo "============================================="

count=0
while IFS= read -r ruta_archivo; do
    # Movemos el archivo a la carpeta destino final
    # Al poner "$CARPETA_DESTINO/" nos aseguramos que caigan ahí
    mv "$ruta_archivo" "$CARPETA_DESTINO/"
    
    ((count++))
    
    # Barra de progreso simple cada 1000 archivos
    if ((count % 1000 == 0)); then
        echo "Movidos: $count de $total..."
    fi

done < lista_completa.txt

# Limpieza de la lista temporal
rm lista_completa.txt

# Opcional: Si quieres borrar las carpetas vacías que quedaron en TEMPORAL
# rm -rf "$CARPETA_ORIGEN"/* echo "============================================="
echo " PROCESO TERMINADO CON ÉXITO"
echo " Total final en destino: $(ls "$CARPETA_DESTINO" | wc -l)"
echo "============================================="