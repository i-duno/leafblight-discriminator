# leafblight-descriminator
A CNN built with keras to discriminate against the dirty diseased leaves and the healthy ones.

> [!NOTE]
> This repository is a fork of [this repo](https://github.com/Atharva-Shakargayen/Potato-Leaf-Disease-Detection-using-CNN-/blob/main/imgGen.ipynb), with a new model that is trained on rice leaves instead of potato leaves.

# run instructions
- Navigate to `src`
- Run `main.py`
- Static files are hosted at port `8080` by default

# overview

**MODEL FITNESS (v5)**

| train_acc | train_loss | val_acc | val_loss |
|---|---|---|---|
| 0.87 | 0.36 | 0.85 | 0.39 |

layers: [32, 64, 128, 256]

> using the mini Xception framework with reduced layer count
