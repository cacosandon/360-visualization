# 360-visualization
IA LAB PUC Research on VLN task, visualization fo 360° indoor environments on Matterport simulator

# Use

For local forwarding on remote server use

`ssh -L localhost:8889:scylla:9995 <user>@<host>`

If you are connection to IA LAB Cluster, use:

`sbatch /home/jiossandon/repos/360-visualization/jupyter_on_slurm.sh`

and cancel after not use

`scancel <process ID SLURM>` (you can review the ID with `sq`)
