import os
from cryptography.fernet import Fernet

def generate_and_save_key():
    """Generates a secure encryption key and saves it locally."""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("🔑 A new secret encryption key has been generated and saved!")

def load_key():
    """Loads the secret key from the local directory."""
    if not os.path.exists("secret.key"):
        generate_and_save_key()
    with open("secret.key", "rb") as key_file:
        return key_file.read()

def encrypt_password(password, cipher_suite):
    """Encrypts a plain-text password into secure ciphertext."""
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password, cipher_suite):
    """Decrypts secure ciphertext back into a plain-text password."""
    try:
        return cipher_suite.decrypt(encrypted_password.encode()).decode()
    except Exception:
        return "❌ Decryption failed. Key corrupted or invalid."

def save_credentials(account, username, password, cipher_suite):
    """Encrypts and appends the credentials to a local storage file."""
    encrypted_pass = encrypt_password(password, cipher_suite)
    with open("passwords.txt", "a") as file:
        file.write(f"{account} | {username} | {encrypted_pass}\n")
    print(f"✅ Credentials for '{account}' saved securely!")

def view_credentials(cipher_suite):
    """Reads, decrypts, and prints all saved credentials cleanly."""
    if not os.path.exists("passwords.txt") or os.stat("passwords.txt").st_size == 0:
        print("\n📭 No passwords stored yet.")
        return

    print("\n==========================================")
    print("         🔒 STORED CREDENTIALS            ")
    print("==========================================")
    with open("passwords.txt", "r") as file:
        for line in file:
            parts = line.strip().split(" | ")
            if len(parts) == 3:
                account, user, encrypted_p = parts
                decrypted_p = decrypt_password(encrypted_p, cipher_suite)
                print(f"🌐 Account  : {account}")
                print(f"👤 Username : {user}")
                print(f"🔑 Password : {decrypted_p}")
                print("-" * 42)
    print("==========================================\n")

def main():
    # Initialize the key and cryptography suite
    key = load_key()
    cipher_suite = Fernet(key)
    
    print("--- Welcome to your Secure Password Vault ---")
    
    while True:
        print("\n1. Add a new password")
        print("2. View saved passwords")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()
        
        if choice == "1":
            account = input("Enter Account/Website name: ").strip()
            username = input("Enter Username/Email: ").strip()
            password = input("Enter Password: ").strip()
            if account and username and password:
                save_credentials(account, username, password, cipher_suite)
            else:
                print("❌ Fields cannot be empty.")
        elif choice == "2":
            view_credentials(cipher_suite)
        elif choice == "3":
            print("Locking vault. Stay safe!")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
