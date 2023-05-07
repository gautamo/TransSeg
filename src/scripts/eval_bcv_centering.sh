echo 'GB: Evaluating Transfer Learning + Depth (TD) Centering Inflation'

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
  --evaluation 1 \
  --model_path data/bcv/processed/checkpoint/ours/centering/epoch=10-step=12154.ckpt

echo 'GB: Completed Transfer Learning + Depth (TD) Centering Inflation'
echo 'GB: Evaluating No Depth (No D) Centering Inflation'

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
  --evaluation 1 \
  --model_path data/bcv/processed/checkpoint/ourswod/centering/epoch=11-step=13259.ckpt

echo 'GB: Completed No Depth (No D) Centering Inflation'
echo 'GB: Evaluating No Transfer Learning (No T) Centering Inflation'

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
  --evaluation 1 \
  --model_path data/bcv/processed/checkpoint/ourswot/centering/epoch=12-step=14364.ckpt

echo 'GB: Completed No Transfer Learning (No T) Centering Inflation'
echo 'GB: Evaluating No Transfer Learning + Depth (No TD) Centering Inflation'

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
  --evaluation 1 \
  --model_path data/bcv/processed/checkpoint/ourswotd/centering/epoch=11-step=13259.ckpt

echo 'GB: Completed No Transfer Learning + Depth (No TD) Centering Inflation'