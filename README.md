# deepfake-demo

## Prepare environment

Requirements:

- conda
- nodejs


```bash
npm i
conda init bash
# build with CUDA (>= 11.3)
bash -i ./prepare_env_cuda113.sh
# build with CPU
bash -i ./prepare_env_cpu.sh
```

## Run backend services

```bash
conda activate deepfake_demo
cd services/rtvc
python main.py
```

```bash
conda activate deepfake_demo
cd services/wav2lip
python main.py
```

```bash
conda activate deepfake_demo
cd services/efficient-vit
# run with CUDA (>= 11.3)
python main.py --cuda
# run with CPU
python main.py
```

## Run web server

```bash
npm run dev
```
