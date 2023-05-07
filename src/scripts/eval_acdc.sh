echo 'GB: Evaluating Transfer Learning + Depth (TD) Centering Inflation (ACDC dataset)'

python main.py \
  --data_dir data/acdc/processed/ \
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
  --model_path data/bcv/processed/checkpoint/ours/centering/acdc/epoch=20-step=7811.ckpt

echo 'GB: Completed Transfer Learning + Depth (TD) Centering Inflation (ACDC dataset)'
echo 'GB: Evaluating No Depth (No D) Centering Inflation (ACDC dataset)'

python main.py \
  --data_dir data/acdc/processed/ \
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
  --model_path data/bcv/processed/checkpoint/ourswod/centering/acdc/epoch=20-step=7811.ckpt

echo 'GB: Completed No Depth (No D) Centering Inflation (ACDC dataset)'