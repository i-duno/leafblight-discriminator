# leafblight-descriminator
A CNN built with keras to discriminate against the dirty diseased leaves (yuck) and the healthy ones.

> [!NOTE]
> This repository is a fork of [this repo](https://github.com/Atharva-Shakargayen/Potato-Leaf-Disease-Detection-using-CNN-/blob/main/imgGen.ipynb), with a new model that is trained on rice leaves instead of potato leaves.

# api usage
This project is currently hosted on [a heroku eco dyno](https://bacterial-leaf-blight-dad8b70bf174.herokuapp.com)[^1], you can access it through cURL or a get request.

You may ping the API like:
`curl https://bacterial-leaf-blight-dad8b70bf174.herokuapp.com/ping`

And you can get predictions like:
`curl -F "file=@image.jpg" https://bacterial-leaf-blight-dad8b70bf174.herokuapp.com/predict`

# run instructions
- Install dependencies first `pip3 install -r requirements.txt`

> [!NOTE]
> Currently the dependencies list `tensorflow-cpu` in substitute for `tensorflow` for hosting reasons.

- Run `python -m uvicorn src.main:app --port=8000 --host=0.0.0.0` or pass your own arguments

# train instructions
- Install additional dependencies `pip3 install -r train-requirements.txt`

- (Optional) Switch out `tensorflow-cpu` with `tensorflow` if you have a gpu that has CUDA

- Run `python train.py <epochs (default=30)>`

- (Optional) Run `python plot.py <train_history.json>` to plot model train history

# current model results:
Training / Validation Accuracy:


![Training v. Validation accuracy](https://github.com/i-duno/leafblight-discriminator/blob/main/Training-vs-Validation%20accuracy.png "Training vs. Validation accuracy")


Training / Validation loss:


![Training v. Validation loss](https://github.com/i-duno/leafblight-discriminator/blob/main/Training-vs-Validation%20loss.png "Training vs. Validation loss")

[^1]: kudos to university email
