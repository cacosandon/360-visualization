#!/bin/bash
#SBATCH --job-name=360-visualization
#SBATCH --ntasks=1                  # Run only one task
#SBATCH --output=slurm/jupyter.log    # Output name (%j is replaced by job ID)
#SBATCH --error=slurm/jupyter.log     # Output errors (optional)
#SBATCH --partition=all
#SBATCH --nodelist=scylla
#SBATCH --workdir=/home/jiossandon   # Where to run the job
#SBATCH --gres=gpu # Request one GPU

pwd; hostname; date

source /home/jiossandon/repos/360-visualization/r2r/bin/activate

echo "Starting notebook requesting one GPU"
jupyter notebook --no-browser --port=9995 --ip="0.0.0.0" && jupyter notebook --no-browser --port=9995
