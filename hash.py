import hashlib
users = []
banks = ['SBI', 'PNB', 'Kotak', 'Union']
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
def verify_password(hashed_password, password):
    return hashed_password == hash_password(password)
def register():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)
    bank_name = input("Enter your bank name (SBI, PNB, Kotak, Union): ")
    if bank_name not in banks:
        print("Invalid bank name. Try again.")
        return
    for user in users:
        if user['username'] == username and user['bank_name'] == bank_name:
            print("Username already exists for this bank.")
            return
    new_user = {
        'username': username,
        'password': hashed_password,
        'bank_name': bank_name,
        'balance': 0.0
    }
    users.append(new_user)
    print("Registration successful!")
def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    bank_name = input("Enter your bank name (SBI, PNB, Kotak, Union): ")   
    if bank_name not in banks:
        print("Invalid bank name. Try again.")
        return None
    for user in users:
        if user['username'] == username and user['bank_name'] == bank_name:
            if verify_password(user['password'], password):
                print("Login successful!")
                return user
            else:
                print("Invalid password!")
                return None
    print("User not found!")
    return None
def deposit(user):
    try:
        amount = float(input("Enter the amount to deposit: "))
        user['balance'] += amount
        print(f"Deposited {amount}. Your new balance is {user['balance']}.")
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
def withdraw(user):
    try:
        amount = float(input("Enter the amount to withdraw: "))
        if amount > user['balance']:
            print("Insufficient balance!")
        else:
            user['balance'] -= amount
            print(f"Withdrew {amount}. Your new balance is {user['balance']}.")
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
def check_balance(user):
    print(f"Your current balance is {user['balance']}.")
def close_account(user):
    users.remove(user)
    print(f"Account for {user['username']} has been closed.")
def display_account_details(user):
    print(f"Username: {user['username']}")
    print(f"Bank Name: {user['bank_name']}")
    print(f"Current Balance: {user['balance']}")
def main():
    while True:
        print("\n--- Bank Management System ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")        
        choice = input("Choose an option: ")        
        if choice == '1':
            register()
        elif choice == '2':
            user = login()
            if user:
                while True:
                    print("\n--- Account Dashboard ---")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Account Details")
                    print("5. Close Account")
                    print("6. Logout")                    
                    option = input("Choose an option: ")                    
                    if option == '1':
                        deposit(user)
                    elif option == '2':
                        withdraw(user)
                    elif option == '3':
                        check_balance(user)
                    elif option == '4':
                        display_account_details(user)
                    elif option == '5':
                        close_account(user)
                        break  
                    elif option == '6':
                        print("Logged out successfully!")
                        break  
                    else:
                        print("Invalid option. Try again.")
        elif choice == '3':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
if __name__ == "__main__":
    main()
