#!/bin/bash

# Nombre del archivo de salida
OUTPUT="Inventario_Moléculas.csv"

# Escribimos los encabezados del Excel
echo "Nombre_Archivo,ZINC_ID,SMILES,Link_Busqueda" > $OUTPUT

echo "Generando lista... (Esto puede tardar unos minutos para 35k archivos)"

# Iteramos sobre cada archivo
for f in *.pdbqt; do
    
    # 1. Extraer el ID (Busca la línea "Name =" y toma la segunda parte)
    # ZINC22 a veces usa "Name =" o simplemente es el nombre del archivo
    id_interno=$(grep "Name =" "$f" | awk -F "=" '{print $2}' | tr -d ' ')
    
    # Si no encuentra ID dentro, usamos el nombre del archivo sin .pdbqt
    if [ -z "$id_interno" ]; then
        id_interno=$(basename "$f" .pdbqt)
    fi

    # 2. Extraer SMILES (Busca "SMILES =" o similar)
    smiles=$(grep "SMILES =" "$f" | awk -F "=" '{print $2}' | tr -d ' ')
    if [ -z "$smiles" ]; then
        smiles="No_reportado_en_archivo"
    fi

    # 3. Generar Link (Para ZINC15/20 es directo, para ZINC22 es búsqueda)
    # Usamos el link genérico de búsqueda por sustancia
    link="https://zinc15.docking.org/substances/$id_interno/"

    # Guardar en el CSV
    echo "$f,$id_interno,$smiles,$link" >> $OUTPUT

done

echo "¡Listo! Abre el archivo '$OUTPUT' en Excel."
