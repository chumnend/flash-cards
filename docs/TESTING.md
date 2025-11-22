# cURL Command for testing

## Test POST /register

curl -X POST http://localhost:8080/register \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "username": "jdoe",
    "email": "john.doe@example.com",
    "password": "password123"
  }'

## Test POST /login

curl -X POST http://localhost:8080/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "password123"
  }'

## Test POST /logut

curl -X POST http://localhost:8080/logout \
  -H "Content-Type: application/json"

## Test GET /explore

curl -X GET http://localhost:8080/decks/explore \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
