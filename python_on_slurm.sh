#!/bin/bash
#SBATCH --job-name=mrearle-metadata-parser
#SBATCH --ntasks=1                  # Correr una sola tarea
#SBATCH --output=logs/metadata-parser.log    # Nombre del output (%j se reemplaza por el ID del trabajo)
#SBATCH --error=logs/metadata-parser.log     # Output de errores (opcional)
#SBATCH --partition=all
#SBATCH --workdir=/home/mrearle/repos/360-visualization   # Direccion donde correr el trabajo

pwd; hostname; date

source /home/mrearle/repos/360-visualization/r2r/bin/activate

python metadata_parser/parse_house_segmentations.py
