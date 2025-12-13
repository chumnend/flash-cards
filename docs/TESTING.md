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

## Test POST /logout

curl -X POST http://localhost:8080/logout \
  -H "Content-Type: application/json"

## Test GET /users/{user_id}

curl -X GET http://localhost:8080/users/{user_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"

## Test GET /explore

curl -X GET http://localhost:8080/decks/explore \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"

## Test GET /decks/feed

curl -X GET http://localhost:8080/decks/feed?token={user_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"

## Test GET /decks

curl -X GET http://localhost:8080/decks?token={user_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"

## Test POST /decks

curl -X POST http://localhost:8080/decks?token={user_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
  -d '{
    "name": "Test Deck",
    "description": "This is a test deck",
    "publishStatus": "private"
  }'

## GET /decks/{deck_id}

curl -X GET http://localhost:8080/decks/{deck_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"




curl -X GET http://localhost:8080/decks/feed?token=37bfd0d8-6e4d-4f8a-a5bd-5df396ac756a \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"

curl -X GET http://localhost:8080/decks?token=37bfd0d8-6e4d-4f8a-a5bd-5df396ac756a \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"

curl -X GET http://localhost:8080/decks/69764111-df5c-4386-8f58-c50eba027c40 \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
