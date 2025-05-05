#my new testing
# To save account details
def creating_account_number():
    while true:
        acct_no=str(random.randint(1000,999))
        if acct_no not in accounts:
            return acct_no

def create_account():
    name=int(input('Enter the Cutomer name: ')).strip()
    #Nitha testing github=====================================================
    try:
        starting_balance = float(input('Enter your strting balance: '))
        if starting_balance<0:
            print("Starting balance must be greater than 0.")
            return
        except ValueError:
            print("Please input valid number")
            return

    acct_no = creating_account_number()
    accounts[acct_no]= {
        "Name":name,
        "balance":starting_balance,
        "transactions":[f"Your account is created!{starting_balance}"]
    }
    print(f"Account created successfully! Your account number is {acct_no}")

#deposite the money
def deposit_money():
    acct_no=int(input("Enter Your Account Number here: "))
    if acct_no in accounts:
        try:
            amount=float(input("Enter the deposit amount: "))
            if amount<=0:
                print("Amount must be greater than 0")
                return
            accounts[acct_no]["balance"]+=amount
            accounts[acct_no]["transaction"].append(f'Your money is deposited{amount}')
            print("Deposited Successfully!")
        except ValueError:
            print("invalid amount")
        else:
        print("account not found")

#


