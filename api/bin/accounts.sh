
# Insert accounts
UUID=$(uuidgen)
echo "Adding ${UUID}"
curl -i \
-H "Content-type: application/json" \
-H "Accept: application/json" \
-d "{"\"id\"": "\"${UUID}\"", "\"balance\"": ""1000""}" \
-X POST http://localhost:8080/accounts

# Run-twice for "Already exists msg
#curl -i \
#-H "Content-type: application/json" \
#-H "Accept: application/json" \
#-d "{"\"id\"": "\"test\"", "\"balance\"": "\"1000\""}" \
#-X POST http://localhost:8080/accounts
