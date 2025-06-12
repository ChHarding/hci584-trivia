import random
import json
import os

# AI disclosure: used Claude Sonet 4 to generate JSON-specific solution, 
# since my understaning is this is the typical way it would work with a web app
if os.path.exists('admin_users.json'):
    with open('admin_users.json', 'r') as file:
        admin_credentials = json.load(file)
else:
    admin_credentials = {}

def generate_id():
    """Generates unique 4-digit integer as the user ID (key value)"""
    while True:
        user_id = random.randint(1000, 9999)
        if user_id not in admin_credentials:
            return user_id
        
def validated_password():
    """Checks user-submitted password to ensure it's between 4 and 8 characters"""
    while True:
        password = input("Create a password - must be between 4 and 8 characters: ")
        if len(password) < 4 or len(password) > 8:
            print("Your password must be between 4 and 8 characters. Please try something new.")
        else:
            return password

def add_new_admin_account():
    """Creates new admin-level account with a unique ID as key, plus name, email, and password as input by the user"""
    user_id = generate_id()
    name = input("Add your name: ")
    email = input("Enter a valid email address: ")
    password = validated_password()

    admin_credentials[user_id] = {
        "name": name,
        "email": email,
        "password": password
    }
    return user_id

new_admin_account = add_new_admin_account()
print(f"User {new_admin_account} added!")
print(f"Total users: {len(admin_credentials)}")

with open('admin_users.json', 'w') as file:
    json.dump(admin_credentials, file, indent=2)

print(admin_credentials)



