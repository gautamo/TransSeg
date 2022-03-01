{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "!for i in $(seq -f \"%02g\" 1 10); do cp scripts_2d/train_${i}.sh scripts_2d/eval_${i}.sh; done"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "!for i in $(seq -f \"%02g\" 1 10); do cp scripts/train_${i}.sh scripts/eval_${i}.sh; done"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "WARNING!!!! out file for scripts_2d/eval_08.sh not found\n",
      "WARNING!!!! out file for scripts/eval_03.sh not found\n",
      "WARNING!!!! out file for scripts/eval_07.sh not found\n"
     ]
    }
   ],
   "source": [
    "import os\n",
    "import re\n",
    "from glob import glob\n",
    "\n",
    "for scripts_dir in [\"scripts_2d\", \"scripts\"]:\n",
    "    for i in range(1, 11):\n",
    "        script_path = f\"{scripts_dir}/eval_{i:02d}.sh\"\n",
    "        out_paths = list(glob(f\"task{i:02d}{('_2d' if '2d' in scripts_dir else '')}_*.out\"))\n",
    "        if \"2d\" not in script_path:\n",
    "            out_paths = [x for x in out_paths if \"2d\" not in x]\n",
    "        if len(out_paths) == 0:\n",
    "            print(f\"WARNING!!!! out file for {script_path} not found\")\n",
    "            with open(script_path, \"w\") as fout: fout.write(\"exit 0\\n\")\n",
    "            continue\n",
    "        else:\n",
    "            valid_out_paths = []\n",
    "            for out_path in out_paths:\n",
    "                out = open(out_path).read()\n",
    "                if \"Run summary:\" in out:\n",
    "                    found = re.findall(\"https://wandb.ai/yuhuiz/MedicalSegmentation/runs/(.*)\", out)\n",
    "                    if len(set(found)) == 1:\n",
    "                        run_id = found[0]\n",
    "                        ckpt_paths = list(glob(f\"MedicalSegmentation/{run_id}/checkpoints/*.ckpt\"))\n",
    "                        if len(ckpt_paths) == 1:\n",
    "                            valid_out_paths.append([out_path, ckpt_paths[0]])\n",
    "            if len(valid_out_paths) == 0:\n",
    "                print(f\"WARNING!!!! out file for {script_path} not found\")\n",
    "                with open(script_path, \"w\") as fout: fout.write(\"exit 0\\n\")\n",
    "                continue\n",
    "            elif len(valid_out_paths) > 1:\n",
    "                with open(script_path, \"w\") as fout: fout.write(\"exit 0\\n\")\n",
    "                print(f\"ERROR!!! more than 1 out file found for {script_path}: {valid_out_paths}\")\n",
    "            else:\n",
    "                out_path, ckpt_path = valid_out_paths[0]\n",
    "                eval_cmd = open(script_path).read().strip()\n",
    "                eval_cmd += f\" \\\\\\n  --evaluation 1 \\\\\\n  --model_path {ckpt_path} > eval_{('3d' if '2d' not in scripts_dir else '2d')}_task{i:02d}.log\\n\"\n",
    "                with open(script_path, \"w\") as fout:\n",
    "                    fout.write(eval_cmd)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2022-02-27 21:18:31.568147: W tensorflow/stream_executor/platform/default/dso_loader.cc:59] Could not load dynamic library 'libcudart.so.10.1'; dlerror: libcudart.so.10.1: cannot open shared object file: No such file or directory\n",
      "2022-02-27 21:18:31.568191: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.\n",
      "Global seed set to 1234\n"
     ]
    }
   ],
   "source": [
    "!for i in $(seq -f \"%02g\" 1 10); do bash scripts/eval_${i}.sh; done\n",
    "!for i in $(seq -f \"%02g\" 1 10); do bash scripts_2d/eval_${i}.sh; done"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "interpreter": {
   "hash": "c6e5723842650410bc8481dec85dfd58db508eb73f7d8d4a4ebd7f4ea28aa990"
  },
  "kernelspec": {
   "display_name": "Python 3.8.11 ('beit')",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.11"
  },
  "orig_nbformat": 4
 },
 "nbformat": 4,
 "nbformat_minor": 2
}