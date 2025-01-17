#!/bin/bash

#SBATCH --job-name=bcv
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=3gb
#SBATCH --partition=pasteur
#SBATCH --gres=gpu:8
#SBATCH --time=24:00:00
#SBATCH --output=bcv_%A_%a.out
#SBATCH --mail-type=ALL

# GB: original --max_steps 25000

python main.py \
  --data_dir data/bcv/processed/ \
  --split_json dataset_5slices.json \
  --img_size 512 512 5 \
  --clip_range -175 250 \
  --in_channels 1 \
  --out_channels 14 \
  --max_steps 25000 \
  --train_batch_size 2 \
  --eval_batch_size 2 \
  --accumulate_grad_batches 1 \
  --force_2d 1 \
  --use_pretrained 0 \
  --checkpoint_dir data/bcv/processed/checkpoint/ourswotd/linear \
  --bootstrap_method "linear"
