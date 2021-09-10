#!/bin/bash

#SBATCH --job-name=sseg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=20GB
#SBATCH --time=47:59:59
#SBATCH --gres=gpu

#GREENE GREENE_GPU_MPS=yes

module purge
module load anaconda3/2020.07

cp -r /scratch/$USER/dataset/nyud_tmp/ $SLURM_TMPDIR
cd /scratch/$USER/SSeg/

source activate dl
for arg
do python train.py $arg $SLURM_TMPDIR > $arg.log 2>&1 &
done

wait