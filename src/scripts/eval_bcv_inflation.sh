echo 'GB: Evaluating Transfer Learning + Depth (TD) Average Inflation'

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
  --model_path data/bcv/processed/checkpoint/ours/inflation/epoch=13-step=15469.ckpt

echo 'GB: Completed Transfer Learning + Depth (TD) Average Inflation'
echo 'GB: Evaluating No Depth (No D) Average Inflation'

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
  --model_path data/bcv/processed/checkpoint/ourswod/inflation/epoch=12-step=14364.ckpt

echo 'GB: Completed No Depth (No D) Average Inflation'
echo 'GB: Evaluating No Transfer Learning (No T) Average Inflation'

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
  --model_path data/bcv/processed/checkpoint/ourswot/inflation/epoch=11-step=13259.ckpt

echo 'GB: Completed No Transfer Learning (No T) Average Inflation'
echo 'GB: Evaluating No Transfer Learning + Depth (No TD) Average Inflation'

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
  --model_path data/bcv/processed/checkpoint/ourswotd/inflation/epoch=11-step=13259.ckpt

echo 'GB: Completed No Transfer Learning + Depth (No TD) Average Inflation'