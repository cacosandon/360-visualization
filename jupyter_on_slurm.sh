#!/bin/bash
#SBATCH --job-name=caco-jupyter
#SBATCH --ntasks=1                  # Correr una sola tarea
#SBATCH --output=slurm/jupyter.log    # Nombre del output (%j se reemplaza por el ID del trabajo)
#SBATCH --error=slurm/jupyter.log     # Output de errores (opcional)
#SBATCH --partition=all
#SBATCH --nodelist=scylla
#SBATCH --workdir=/home/jiossandon   # Direccion donde correr el trabajo

pwd; hostname; date

source virtualenv/r2r/bin/activate

jupyter notebook --no-browser --port=9995 --ip="0.0.0.0" && jupyter notebook --no-browser --port=9995
