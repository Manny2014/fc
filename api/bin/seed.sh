
# Insert accounts
UUID=$(uuidgen)
echo "Adding ${UUID}"
#curl -i \
#-H "Content-type: application/json" \
#-H "Accept: application/json" \
#-d "{"\"id\"": "\"${UUID}\"", "\"balance\"": "\"1000\""}" \
#-X POST http://localhost:8080/accounts

# Run-twice for "Already exists msg
#curl -i \
#-H "Content-type: application/json" \
#-H "Accept: application/json" \
#-d "{"\"id\"": "\"test\"", "\"balance\"": "\"1000\""}" \
#-X POST http://localhost:8080/accounts


curl -i \
-H "Content-type: application/json" \
-H "Accept: application/json" \
-d "{"\"from_account_id\"": "\"7bbc2e06-cd88-4c44-8826-8fea7c44975f\"", "\"to_account_id\"": "\"3af9a095-b3ea-49fb-a7ad-8f5e9c20d58b\"","\"amount\"": "'1000'"}" \
-X POST http://localhost:8080/transactions