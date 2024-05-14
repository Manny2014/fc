# Fake Company (fc) Demo

## Documentation

- [System Arch](docs/00-Sys-Arch.md)

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

### (5) Create new account
```bash
UUID=$(uuidgen)
echo "Adding ${UUID}"
curl -i \
-H "Content-type: application/json" \
-H "Accept: application/json" \
-d "{"\"id\"": "\"${UUID}\"", "\"balance\"": ""1000""}" \
-X POST http://localhost:8080/accounts
```

### (6) Get all accounts from db (select 2 for next step)
```bash
docker exec -it c1 bash -c 'cqlsh -k payments -e "select * from accounts;"'  
```

### (7) Submit transaction
```bash
FROM_UUID="840f7006-da3a-4798-ad56-03f3486339ad"
TO_UUID="dca0418a-0af5-489f-b159-80d6a6bdb47c"

curl -i \
-H "Content-type: application/json" \
-H "Accept: application/json" \
-d "{"\"from_account_id\"": "\"${FROM_UUID}\"", "\"to_account_id\"": "\"${TO_UUID}\"","\"amount\"": "'1000'"}" \
-X POST http://localhost:8080/transactions
``` 
