#importing required modules 
import bcrypt
import os 
USERS_DATA_FILES= "users.txt"

# implementing hashed password 

def hash_password(plain_text_password):
    password_bytes=plain_text_password.encode("utf-8")
    salt=bcrypt.gensalt()
    hashed_bytes= bcrypt.hashpw(password_bytes, salt)
    hashed_str=hashed_bytes.decode("utf-8")
    return hashed_str

# implimenting verify password 
def verify_password(plain_text_password, hashed_password): 
    password_bytes=plain_text_password.encode('utf-8')
    hashed_bytes=hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# Testing the hashing function temporary 
"""if __name__ == "__main__":
    test_password = "SecurePassword123"
# Test hashing
    hashed = hash_password(test_password)
    print(f"Original password: {test_password}")
    print(f"Hashed password: {hashed}")
    print(f"Hash length: {len(hashed)} characters")
# Test verification with correct password
    is_valid = verify_password(test_password, hashed)
    print(f"\nVerification with correct password: {is_valid}")
# Test verification with incorrect password
    is_invalid = verify_password("WrongPassword", hashed)
print(f"Verification with incorrect password: {is_invalid}")"""

def register_user(username, password): 
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    hashed_password = hash_password(password)
    with open(USERS_DATA_FILES, "a") as file:
        file.write(f"{username},{hashed_password}\n")
    print(f"Success: User '{username}' registered successfully!")
    return True

#impliment user exists 

def user_exists(username):
    if not os.path.exists(USERS_DATA_FILES):
        return False
    with open(USERS_DATA_FILES,'r') as file:
        for line in file:
            stored_username=line.strip().split(" ")[0]
            if stored_username==username:
                return True
    return False 

#impliment login user 
def login_user (username, password):
    if not os.path.exists(USERS_DATA_FILES):
        print("Error: No registered users found.")
        return False
    with open(USERS_DATA_FILES, "r") as file:
        for line in file:
            stored_username, stored_hash = line.strip().split(",")

            if stored_username == username:
                # 3. If username matches, verify the password
                if verify_password(password, stored_hash):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False
    print("Error: Username was not found ")
    return False

#validation of the username
def validate_username(username):
    if len(username) < 3 or len(username) > 20:
        return (False, "Username must be between 3 and 20 characters.")
    if not username.isalnum():
        return (False, "Username must contain only letters and digits (alphanumeric).")
    return (True, "")

#validation of the password
def validate_password(password):
    if len(password) < 6 or len(password) > 50:
        return (False, "Password must be between 6 and 50 characters.")
    return (True, "")

def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user
            register_user(username, password)

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                # In a real app, you would now show protected features

            input("\nPress Enter to return to main menu...")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()

    
