from datetime import datetime

class Transaction:
    def __init__(self, narration, amount, transaction_type):
        self.date_time = datetime.now()
        self.narration = narration
        self.amount = amount
        self.transaction_type = transaction_type
    def __str__(self):
        return f"Transaction date and time: {self.date_time} | {self.narration}: {self.amount}"

class Account:
    def __init__(self, name, account_number):
        self.name = name
        self.account_number = account_number
        self.transactions = []
        self.loan = 0
        self.is_frozen = False
        self.closed_account = False
        self.min_balance = 50

    def get_balance(self):
        if self.is_frozen or self.closed_account:
            return "Account is frozen or closed. You can not transact."
        balance = 0
        for transaction in self.transactions:
            if transaction.transaction_type == "credit":
                balance += transaction.amount
            elif transaction.transaction_type == "debit":
                balance -= transaction.amount
        return balance

    def deposit(self, amount):
        if self.is_frozen or self.closed_account:
            return "Account is frozen or closed. You can not deposit."
        if amount > 0:
            self.transactions.append(Transaction("Deposit", amount, "credit"))
            balance = self.get_balance()
            return f"Your new balance is {balance} birr."
        else:
            return "Invalid deposit amount."
        
    def withdraw(self, amount):
        if self.is_frozen or self.closed_account:
            return "Account is frozen or closed. You can not withdraw."
        balance = self.get_balance()
        if balance - amount < self.min_balance:
            return f"Sorry, you need a minimum of {self.min_balance} birr in your account."
        if amount > 0:
            self.transactions.append(Transaction("Withdrawal", amount, "debit"))
            balance = self.get_balance()
            return f"Your new balance is {balance} birr."
        else:
            return "Invalid withdraw amount."

    def transfer_fund(self, amount, recipient):
        if not isinstance(recipient, Account):
            return "Incomplete recipient"
        if self.is_frozen or self.closed_account:
            return "Account is frozen or closed. You can not transfer."
        if amount < 0:
            return "Invalid transfer amount."
        balance = self.get_balance()
        if balance - amount < self.min_balance:
            return f"Sorry, you can not transfer {amount}, you only have {balance}"
        else:
            self.transactions.append(Transaction(f"Transfer to {recipient.name}", amount, "debit"))
            recipient.transactions.append(Transaction(f"Transfer from {self.name}", amount, "credit"))
            self_balance = self.get_balance()
            return f"You have successfully transferred {amount} birr to {recipient.name}. Your new balance is {self_balance} birr."

    def request_loan(self, amount):
        if self.is_frozen or self.closed_account:
            return "Account is frozen or closed. You can not request a loan."
        loan_limit = sum([transaction.amount for transaction in self.transactions if transaction.transaction_type == "credit"]) * 0.7
        if amount <= loan_limit:
            self.loan += amount
            self.transactions.append(Transaction("Loan credited", amount, "credit"))
            return f"Loan of {amount} birr approved. Your new balance is {self.get_balance()} birr, your loan balance is {self.loan} birr."
        else:
            return f"Invalid loan amount. Your request should be less than {loan_limit}."

    def repay_loan(self, amount):
        if self.is_frozen or self.closed_account:
            return "Account is frozen or closed. You can not repay loan."
        balance = self.get_balance()
        if self.loan == 0:
            return "You have no loan to repay."
        if amount > balance - self.min_balance:
            return "Insufficient balance to repay loan."
        if amount <= self.loan:
            self.loan -= amount
            self.transactions.append(Transaction("Loan repayment", amount, "debit"))
            return f"You have repaid {amount}, you are left with {self.loan} birr of loan."
        else:
            return f"You are trying to repay more than your outstanding loan."

    def account_details(self):
        balance = self.get_balance()
        return f"Name: {self.name}\nAccount Number: {self.account_number}\nCurrent Balance: {balance}"

    def account_transfer(self, new_owner):
        old_name = self.name
        self.name = new_owner
        return f"The new owner for the account {self.account_number} is {self.name} (was {old_name})."

    def account_statement(self):
        if self.is_frozen or self.closed_account:
            print("Account is frozen or closed. No statement available.")
            return
        if not self.transactions:
            print("No transactions yet.")
            return
        for trx in self.transactions:
            print(trx)
        if self.loan != 0:
            print(f"Outstanding loan: {self.loan} birr.")

    def interest(self):
        balance = self.get_balance()
        interest_rate = 0.12
        interest_amount = balance * interest_rate
        self.transactions.append(Transaction("Interest added", interest_amount, "credit"))
        return f"Your balance after interest is {self.get_balance()} birr."

    def freeze_account(self, status):
        self.is_frozen = status
        if self.is_frozen:
            return f"The account {self.account_number} is frozen."
        else:
            return f"The account {self.account_number} is not frozen."

    def close_account(self):
        self.closed_account = True
        self.transactions = []
        self.loan = 0
        self.is_frozen = False
        return "The account has been closed. All balances and transactions have been cleared."

    def min_balance_message(self):
        return f"The minimum balance is {self.min_balance} birr."