#!/bin/bash

#SBATCH --job-name=msd
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=3gb
#SBATCH --partition=pasteur
#SBATCH --gres=gpu:4
#SBATCH --time=24:00:00
#SBATCH --output=task10_%A_%a.out
#SBATCH --mail-type=ALL

python compute_macs_flops.py \
  --data_dir /sailhome/yuhuiz/develop/data/MedicalImages/msd/processed/Task10_Colon/   \
  --split_json dataset_5slices.json \
  --img_size 512 512 5 \
  --clip_range -175 250 \
  --mean_std 70.43 31.84 \
  --in_channels 1 \
  --out_channels 2 \
  --max_steps 25000 \
  --train_batch_size 2 \
  --eval_batch_size 2 \
  --accumulate_grad_batches 4 \
  --force_2d 1 