#######
# Task09_Spleen dataset
#######

echo 'GB: Evaluating Transfer Learning + Depth (TD) Centering Inflation (Task09_Spleen dataset)'

python main.py \
  --data_dir data/msd/processed/Task09_Spleen/ \
  --split_json dataset_5slices.json \
  --img_size 512 512 5 \
  --clip_range -175 250 \
  --in_channels 1 \
  --out_channels 14 \
  --max_steps 25000 \
  --train_batch_size 2 \
  --eval_batch_size 2 \
  --accumulate_grad_batches 1 \
  --evaluation 1 \
  --model_path data/bcv/processed/checkpoint/ours/centering/msd09/epoch=11-step=8747.ckpt

echo 'GB: Completed Transfer Learning + Depth (TD) Centering Inflation (Task09_Spleen dataset)'
echo 'GB: Evaluating No Depth (No D) Centering Inflation (Task09_Spleen dataset)'

python main.py \
  --data_dir data/msd/processed/Task09_Spleen/ \
  --split_json dataset_5slices.json \
  --img_size 512 512 5 \
  --clip_range -175 250 \
  --in_channels 1 \
  --out_channels 14 \
  --max_steps 25000 \
  --train_batch_size 2 \
  --eval_batch_size 2 \
  --accumulate_grad_batches 1 \
  --evaluation 1 \
  --model_path data/bcv/processed/checkpoint/ourswod/centering/msd09/tba.ckpt

echo 'GB: Completed No Depth (No D) Centering Inflation (Task09_Spleen dataset)'