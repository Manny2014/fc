# Fake Company (fc) Demo

## Quickstart

### (1) Install application
```bash
# Move to api dir
cd api

# Setup v-env
python3 -m venv venv

# activate v-env
source .venv/bin/activate

# install app
pip install -e 
```

### (2) Start middle-ware

```bash
docker compose up
```

### (3) Start API
```bash
fc-payments-api
```

### (4) Start Processor
```bash
fc-payments-consumer 
```