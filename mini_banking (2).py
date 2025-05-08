import getpass
import datetime
import os
import random
import string

ACCOUNTS_FILE = 'AccountDetails.txt'
TRANSACTION_FILE = 'transactions.txt'
CREDENTIALS_FILE = 'credentials.txt'
ACCOUNT_NUM_FILE = 'account_numbers.txt'

accounts = {}

def load_data():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    acc_no, name, balance = parts
                    accounts[acc_no] = {'name': name, 'balance': float(balance), 'transactions': []}

    if os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, 'r') as f:
            for line in f:
                acc_no, txn = line.strip().split('|')
                if acc_no in accounts:
                    accounts[acc_no]['transactions'].append(txn)

def save_all_accounts():
    with open(ACCOUNTS_FILE, 'w') as f:
        for acc_no, details in accounts.items():
            f.write(f"{acc_no}|{details['name']}|{details['balance']}\n")

def generate_account_number():
    if not os.path.exists(ACCOUNT_NUM_FILE):
        with open(ACCOUNT_NUM_FILE, 'w') as f:
            f.write('1001')

    with open(ACCOUNT_NUM_FILE, 'r+') as f:
        current = int(f.read().strip())
        new = current + 1
        f.seek(0)
        f.write(str(new))
    return str(current)

def write_transaction(acc_no, txn):
    with open(TRANSACTION_FILE, 'a') as f:
        f.write(acc_no + '|' + txn + '\n')

def create_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def createAccount():
    name = input("Enter Your Full Name : ").strip().upper()
    if name == '':
        print("Name cannot be empty.")
        return

    try:
        balance = float(input("Enter Initial Balance: "))
        if balance < 0:
            print("Balance must be 0 or more.")
            return
    except ValueError:
        print("Invalid input.")
        return

    acc_no = generate_account_number()
    username = "user" + acc_no
    password = create_password()

    with open(CREDENTIALS_FILE, 'a') as f:
        f.write(username + ':' + password + ':user\n')

    accounts[acc_no] = {
        'name': name,
        'balance': balance,
        'transactions': [f"Account opened with Rs.{balance}"]
    }

    save_all_accounts()
    write_transaction(acc_no, f"Account opened with Rs.{balance}")
    print("Account Created Successfully.")
    print("Account Number:", acc_no)
    print("Username:", username)
    print("Password:", password)

def depositMoney():
    acc_no = input("Enter Account Number: ").strip()
    if acc_no not in accounts:
        print("Account not found.")
        return

    try:
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
    except ValueError:
        print("Invalid input.")
        return

    accounts[acc_no]['balance'] += amount
    txn = f"Deposited Rs.{amount} on {datetime.datetime.now()}"
    accounts[acc_no]['transactions'].append(txn)
    write_transaction(acc_no, txn)
    save_all_accounts()
    print("Deposit Successful.")

def withdrawMoney():
    acc_no = input("Enter Account Number: ").strip()
    if acc_no not in accounts:
        print("Account not found.")
        return

    try:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0:
            print("Invalid amount.")
            return
    except ValueError:
        print("Wrong input.")
        return

    if amount > accounts[acc_no]['balance']:
        print("Not enough balance.")
        return

    accounts[acc_no]['balance'] -= amount
    txn = f"Withdrew Rs.{amount} on {datetime.datetime.now()}"
    accounts[acc_no]['transactions'].append(txn)
    write_transaction(acc_no, txn)
    save_all_accounts()
    print("Withdraw Successful.")

def checkBalance():
    acc_no = input("Enter Account Number: ").strip()
    if acc_no not in accounts:
        print("Account not found.")
        return
    print("Your Balance is Rs.", accounts[acc_no]['balance'])

def transactionHistory():
    acc_no = input("Enter Account Number: ").strip()
    if acc_no not in accounts:
        print("Account not found.")
        return
    print("Transaction History:")
    for t in accounts[acc_no]['transactions']:
        print("-", t)

def transferMoney():
    from_acc = input("Enter your Account Number: ").strip()
    if from_acc not in accounts:
        print("Source account not found.")
        return

    to_acc = input("Enter recipient Account Number: ").strip()
    if to_acc not in accounts:
        print("Recipient account not found.")
        return

    try:
        amount = float(input("Enter amount to transfer: "))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
    except ValueError:
        print("Invalid input.")
        return

    if amount > accounts[from_acc]['balance']:
        print("Not enough balance.")
        return

    accounts[from_acc]['balance'] -= amount
    accounts[to_acc]['balance'] += amount
    from_txn = f"Transferred Rs.{amount} to {to_acc} on {datetime.datetime.now()}"
    to_txn = f"Received Rs.{amount} from {from_acc} on {datetime.datetime.now()}"
    accounts[from_acc]['transactions'].append(from_txn)
    accounts[to_acc]['transactions'].append(to_txn)
    write_transaction(from_acc, from_txn)
    write_transaction(to_acc, to_txn)
    save_all_accounts()
    print("Transfer Successful.")

def calculateInterest():
    acc_no = input("Enter Account Number: ").strip()
    if acc_no not in accounts:
        print("Account not found.")
        return

    try:
        rate = float(input("Enter annual interest rate (in %): "))
        if rate < 0:
            print("Interest rate must be non-negative.")
            return
    except ValueError:
        print("Invalid input.")
        return

    balance = accounts[acc_no]['balance']
    interest = balance * (rate / 100)
    accounts[acc_no]['balance'] += interest
    txn = f"Interest of Rs.{interest} added on {datetime.datetime.now()}"
    accounts[acc_no]['transactions'].append(txn)
    write_transaction(acc_no, txn)
    save_all_accounts()
    print(f"Interest added. New Balance: Rs.{accounts[acc_no]['balance']}")

def read_credentials():
    creds = {}
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    username, password, role = line.split(':')
                    creds[username] = {'password': password, 'role': role}
    return creds

def login(creds):
    attempt = 0
    while attempt < 3:
        username = input("Enter username: ")
        password = getpass.getpass("Enter your password: ")

        if username in creds and creds[username]['password'] == password:
            role = creds[username]['role']
            print("Login successful! You are a", role)
            if role == 'admin':
                adminMenu()
            elif role == 'user':
                userMenu()
            return
        else:
            print("Login failed. Wrong credentials.")
            attempt += 1
    print("Your attempts are finished.")

def adminMenu():
    while True:
        print("\nAdmin Menu")
        print("1. Create New Account")
        print("2. Logout")
        ch = input("Enter your choice: ")
        if ch == '1':
            createAccount()
        elif ch == '2':
            break
        else:
            print("Invalid option.")

def userMenu():
    while True:
        print("\nUser Menu")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. View Transactions")
        print("5. Transfer Money")
        print("6. Calculate Interest")
        print("7. Logout")
        ch = input("Enter your choice: ")
        if ch == '1':
            depositMoney()
        elif ch == '2':
            withdrawMoney()
        elif ch == '3':
            checkBalance()
        elif ch == '4':
            transactionHistory()
        elif ch == '5':
            transferMoney()
        elif ch == '6':
            calculateInterest()
        elif ch == '7':
            break
        else:
            print("Invalid option.")

def main():
    load_data()
    creds = read_credentials()
    login(creds)

if __name__ == "__main__":
    main()
