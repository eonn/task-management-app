#!/usr/bin/env python3
"""
Test script for user registration functionality

Author: Eon (Himanshu Shekhar)
Email: eonhimanshu@gmail.com

This script tests the user registration, login, and authentication functionality.
"""

import requests
import json
import sys

# Configuration
DJANGO_API_URL = "http://localhost:8000/api"
TEST_USER = {
    "username": "testuser123",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User"
}

def test_registration():
    """Test user registration endpoint"""
    print("🧪 Testing User Registration...")
    
    try:
        # Test registration
        response = requests.post(
            f"{DJANGO_API_URL}/users/register/",
            json=TEST_USER,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Registration successful!")
            print(f"User ID: {data['user']['id']}")
            print(f"Username: {data['user']['username']}")
            print(f"Email: {data['user']['email']}")
            print(f"Access Token: {data['tokens']['access'][:50]}...")
            return data['tokens']['access']
        else:
            print("❌ Registration failed!")
            print(f"Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Django API. Make sure it's running on port 8000.")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def test_login(token):
    """Test login with registered user"""
    if not token:
        return
        
    print("\n🔐 Testing Login...")
    
    try:
        response = requests.post(
            f"{DJANGO_API_URL}/users/login/",
            json={
                "username": TEST_USER["username"],
                "password": TEST_USER["password"]
            },
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
        else:
            print("❌ Login failed!")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Login error: {e}")

def test_protected_endpoint(token):
    """Test accessing protected endpoint"""
    if not token:
        return
        
    print("\n🛡️ Testing Protected Endpoint...")
    
    try:
        response = requests.get(
            f"{DJANGO_API_URL}/users/profile/",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Protected endpoint accessible!")
            print(f"User Profile: {data}")
        else:
            print("❌ Protected endpoint failed!")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Protected endpoint error: {e}")

def main():
    """Main test function"""
    print("�� User Registration Test Suite")
    print("=" * 40)
    
    # Test registration
    token = test_registration()
    
    # Test login
    test_login(token)
    
    # Test protected endpoint
    test_protected_endpoint(token)
    
    print("\n" + "=" * 40)
    print("🏁 Test suite completed!")

if __name__ == "__main__":
    main()
