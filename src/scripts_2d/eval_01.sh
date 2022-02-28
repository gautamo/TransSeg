#!/bin/bash

#SBATCH --job-name=msd_2d
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=6gb
#SBATCH --partition=pasteur
#SBATCH --gres=gpu:4
#SBATCH --time=24:00:00
#SBATCH --output=task01_2d_%A_%a.out
#SBATCH --mail-type=ALL

python main.py \
  --data_dir /sailhome/yuhuiz/develop/data/MedicalImages/msd/processed/Task01_BrainTumour/   \
  --split_json dataset_5slices.json \
  --img_size 240 240 5 \
  --clip_range -1000000 1000000 \
  --in_channels 4 \
  --out_channels 4 \
  --max_steps 25000 \
  --train_batch_size 2 \
  --eval_batch_size 2 \
  --accumulate_grad_batches 4 \
  --force_2d 1 \
  --evaluation 1 \
  --model_path MedicalSegmentation/35n7ddsm/checkpoints/epoch=12-step=24374.ckpt > eval_2d_task01.log