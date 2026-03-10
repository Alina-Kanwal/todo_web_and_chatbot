import requests
import json

BASE_URL = "http://localhost:8000"

# Step 1: Sign up
print("=== Signing up ===")
signup_response = requests.post(f"{BASE_URL}/api/auth/signup", json={
    "email": "chatbotuser@test.com",
    "password": "testpass123"
})
print(f"Signup: {signup_response.status_code}")
print(signup_response.json())

# Step 2: Sign in to get token
print("\n=== Signing in ===")
signin_response = requests.post(f"{BASE_URL}/api/auth/signin", json={
    "email": "chatbotuser@test.com",
    "password": "testpass123"
})
print(f"Signin: {signin_response.status_code}")
token_data = signin_response.json()
access_token = token_data.get("access_token")
print(f"Token received: {access_token[:50]}...")

# Step 3: Test chatbot
print("\n=== Testing Chatbot ===")
chat_response = requests.post(
    f"{BASE_URL}/api/chat",
    json={
        "message": "Create a task to buy milk",
        "conversation_id": None
    },
    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
)
print(f"Chat response: {chat_response.status_code}")
print(json.dumps(chat_response.json(), indent=2, ensure_ascii=False))

# Step 4: Another chat message
print("\n=== Testing Chatbot - Show Tasks ===")
chat_response2 = requests.post(
    f"{BASE_URL}/api/chat",
    json={
        "message": "Show my tasks",
        "conversation_id": None
    },
    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
)
print(f"Chat response: {chat_response2.status_code}")
print(json.dumps(chat_response2.json(), indent=2, ensure_ascii=False))
