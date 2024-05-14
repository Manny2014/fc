UUID=$(uuidgen)
echo "Adding ${UUID}"

curl -i \
-H "Content-type: application/json" \
-H "Accept: application/json" \
-d "{"\"from_account_id\"": "\"21e07006-a1e5-431a-b5cc-e5bd887e95ee\"", "\"to_account_id\"": "\"1ed6ebfa-be7c-4d1e-8184-b1fd140f4ea0\"","\"amount\"": "'1000'"}" \
-X POST http://localhost:8080/transactions