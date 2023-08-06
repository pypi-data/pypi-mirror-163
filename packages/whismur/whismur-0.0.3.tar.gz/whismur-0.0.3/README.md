# Monitor process and send to telegram

## Installation

### From source

```sh
conda create -p ./env python=3.8 -y
pip install -r requirements.txt
pip install -e .
```

### From pypi

```sh
pip install whismur
```

## Usage

```sh
whismur monitor-pid pids.txt \ 
    --config-path config/tetebot.yaml \ 
    --interval 1 # check every 1 second
```
