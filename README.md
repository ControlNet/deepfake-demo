# deepfake-demo

## Prepare environment

Requirements:

- conda
- nodejs
- GPU (CUDA >= 11.3)


```bash
npm i
bash -i ./prepare_backend_env.sh
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
python main.py
```

## Run web server

```bash
vite
```
