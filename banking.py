import random
import os

#login 
customername = "customer1" 
password = "cus123@" 
input_customer = input("Enter customer name: ") 
input_pass = input("Enter the password: ") 
if input_customer == customername and input_pass == password: 
 print("Welcome Login successful!\n") 
else: 
 print("Login failed. Exitng program.")
 exit() 
 
# Global dictionary to store account details
accounts = {}

# Function to generate unique account number
def generate_account_number():
    while True:
        acc_no6 = str(random.randint(10000, 99999))
        if acc_no not in accounts:
            return acc_no

# Function to create account
def create_account():
    name = input("Enter account holder name: ").strip()
    try:
        initial_balance = float(input("Enter initial balance: "))
        if initial_balance < 0:
            print("Initial balance must be non-negative.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    acc_no = generate_account_number()
    accounts[acc_no] = {
        "name": name,
        "balance": initial_balance,
        "transactions": [f"Account created with balance {initial_balance}"]
    }
    print(f"Account created successfully! Your account number is {acc_no}")

# Function to deposit money
def deposit_money():
    acc_no = input("Enter account number: ")
    if acc_no in accounts:
        try:
            amount = float(input("Enter amount to deposit: "))
            if amount <= 0:
                print("Amount must be positive.")
                return
            accounts[acc_no]["balance"] += amount
            accounts[acc_no]["transactions"].append(f"Deposited {amount}")
            print("Deposit successful.")
        except ValueError:
            print("Invalid amount.")
    else:
        print("Account not found.")

# Function to withdraw money
def withdraw_money():
    acc_no = input("Enter account number: ")
    if acc_no in accounts:
        try:
            amount = float(input("Enter amount to withdraw: "))
            if amount <= 0:
                print("Amount must be positive.")
                return
            if accounts[acc_no]["balance"] >= amount:
                accounts[acc_no]["balance"] -= amount
                accounts[acc_no]["transactions"].append(f"Withdrew {amount}")
                print("Withdrawal successful.")
            else:
                print("Insufficient balance.")
        except ValueError:
            print("Invalid amount.")
    else:
        print("Account not found.")

# Function to check balance
def check_balance():
    acc_no = input("Enter account number: ")
    if acc_no in accounts:
        print(f"Account Holder: {accounts[acc_no]['name']}")
        print(f"Current Balance: {accounts[acc_no]['balance']}")
    else:
        print("Account not found.")

# Function to show transaction history
def transaction_history():
    acc_no = input("Enter account number: ")
    if acc_no in accounts:
        print("Transaction History:")
        for txn in accounts[acc_no]["transactions"]:
            print("-", txn)
    else:
        print("Account not found.")

# Optional: Save to file
def save_to_file(filename="accounts.txt"):
    with open(filename, "w") as f:
        for acc_no, info in accounts.items():
            f.write(f"{acc_no}|{info['name']}|{info['balance']}|{'#'.join(info['transactions'])}\n")
    print("Data saved to file.")

# Optional: Load from file
def load_from_file(filename="accounts.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                acc_no, name, balance, txn_str = line.strip().split("|")
                accounts[acc_no] = {
                    "name": name,
                    "balance": float(balance),
                    "transactions": txn_str.split("#")
                }

# Main menu-driven function
def main():
    load_from_file()
    while True:
        print("\n=== Mini Banking System ===")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            deposit_money()
        elif choice == "3":
            withdraw_money()
        elif choice == "4":
            check_balance()
        elif choice == "5":
            transaction_history()
        elif choice == "6":
            save_to_file()
            print("Thank you for using the Mini Banking App.")
            break
        else:
            print("Invalid choice. Please select from 1 to 6.")

main()