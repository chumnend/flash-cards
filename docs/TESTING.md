# cURL Command for testing

## ====================== USERS ====================================

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

## Test PUT /users/{user_id}

curl -X PUT http://localhost:8080/users/{user_id}?token={user_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "firstName": "Updated John",
    "lastName": "Updated Doe",
    "username": "updated_jdoe",
    "email": "updated.john.doe@example.com",
    "aboutMe": "Updated about me section"
  }'

## Test PUT /change_password

curl -X PUT http://localhost:8080/change_password?token={user_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "currentPassword": "password123",
    "newPassword": "newpassword456"
  }'

## Test POST /users/{user_id}/follow

curl -X POST http://localhost:8080/users/{user_to_follow_id}/follow?token={current_user_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"

## Test DELETE /users/{user_id}/unfollow

curl -X DELETE http://localhost:8080/users/{user_to_unfollow_id}/unfollow?token={current_user_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"

## Test GET /users/{user_id}/followers

curl -X GET http://localhost:8080/users/{user_id}/followers \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"

## Test GET /users/{user_id}/following

curl -X GET http://localhost:8080/users/{user_id}/following \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"

## ====================== DECKS ====================================

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

## Test PUT /decks/{deck_id}

curl -X PUT http://localhost:8080/decks/{deck_id}?token={user_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "Updated Deck Name",
    "description": "Updated description",
    "publishStatus": "public"
  }'

## Test DELETE /decks/{deck_id}

curl -X DELETE http://localhost:8080/decks/{deck_id}?token={user_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"

## ====================== CARDS ====================================

## Test GET /decks/{deck_id}/cards (public deck)

curl -X GET http://localhost:8080/decks/{deck_id}/cards \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"

## Test GET /decks/{deck_id}/cards (private deck - with token)

curl -X GET http://localhost:8080/decks/{deck_id}/cards?token={user_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"

## Test POST /decks/{deck_id}/cards

curl -X POST http://localhost:8080/decks/{deck_id}/cards?token={user_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "frontText": "What is the capital of France?",
    "backText": "Paris"
  }'

## Test GET /decks/{deck_id}/cards/{card_id}

curl -X GET http://localhost:8080/decks/{deck_id}/cards/{card_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"

## Test PUT /decks/{deck_id}/cards/{card_id}

curl -X PUT http://localhost:8080/decks/{deck_id}/cards/{card_id}?token={user_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "frontText": "What is the capital of France?",
    "backText": "Paris, France"
  }'

## Test DELETE /decks/{deck_id}/cards/{card_id}

curl -X DELETE http://localhost:8080/decks/{deck_id}/cards/{card_id}?token={user_id} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
