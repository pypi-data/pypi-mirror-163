# Fuego

## Getting Started

```
pip install fuego
```

#### Running the examples

Clone the repo and put your `config.json` file associated with your AzureML resource in the `examples/` folder...

```
git clone https://github.com/nateraw/fuego.git
cd fuego
```

Then, run the following:

```
fuego run \
    --requirements-file examples/lightning_mnist_example/requirements.txt \
    examples/lightning_mnist_example/train.py \
    --accelerator gpu \
    --devices 1 \
    --max_epochs 4 \
    --default_root_dir ./logs
```
