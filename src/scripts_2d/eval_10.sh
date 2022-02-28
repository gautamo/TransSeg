#!/bin/bash

#SBATCH --job-name=msd_2d
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=6gb
#SBATCH --partition=pasteur
#SBATCH --gres=gpu:4
#SBATCH --time=24:00:00
#SBATCH --output=task10_2d_%A_%a.out
#SBATCH --mail-type=ALL

python main.py \
  --data_dir /sailhome/yuhuiz/develop/data/MedicalImages/msd/processed/Task10_Colon/   \
  --split_json dataset_5slices.json \
  --img_size 512 512 5 \
  --clip_range -28 158 \
  --mean_std 70.43 31.84 \
  --in_channels 1 \
  --out_channels 2 \
  --max_steps 25000 \
  --train_batch_size 2 \
  --eval_batch_size 2 \
  --accumulate_grad_batches 4 \
  --force_2d 1 \
  --evaluation 1 \
  --model_path MedicalSegmentation/2it9a8jv/checkpoints/epoch=60-step=21044.ckpt > eval_2d_task10.log
