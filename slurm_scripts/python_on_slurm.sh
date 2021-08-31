#!/bin/bash
#SBATCH --job-name=metadata-parser
#SBATCH --ntasks=1                  # Run only one task
#SBATCH --output=logs/metadata-parser-%j.out    # Output name (%j is replaced by job ID)
#SBATCH --error=logs/metadata-parser-%j.err     # Output errors (optional)
#SBATCH --partition=all
#SBATCH --workdir=/home/mrearle/repos/360-visualization   # Where to run the job

pwd; hostname; date

source /home/mrearle/repos/360-visualization/r2r/bin/activate

echo "Beginnig parsing"
python metadata_parser/parse_house_segmentations.py
echo "Job done"
