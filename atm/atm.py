from __future__ import annotations
from abc import ABC, abstractmethod
from threading import Lock
import datetime

# The ATM system should support basic operations such as balance inquiry, cash withdrawal, and cash deposit.
# Users should be able to authenticate themselves using a card and a PIN (Personal Identification Number).
# The system should interact with a bank's backend system to validate user accounts and perform transactions.
# The ATM should have a cash dispenser to dispense cash to users.
# The system should handle concurrent access and ensure data consistency.
# The ATM should have a user-friendly interface for users to interact with.

class Card:
    def __init__(self, card_number, pin):
        self.card_number = card_number
        self.pin = pin
    
    def get_card_number(self):
        return self.card_number
    
    def get_pin(self):
        return self.pin
    

class Account:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def get_account_number(self):
        return self.account_number
    
    def get_balance(self):
        return self.balance
    
    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount


class BankingService:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number, init_balance):
        self.accounts[account_number] = Account(account_number, init_balance)

    def get_account(self, account_number):
        return self.accounts[account_number]

    def process_transaction(self, transaction):
        transaction.execute()


class Transaction(ABC):
    def __init__(self, transaction_id, account, amount):
        self.transaction_id = transaction_id
        self.account = account
        self.amount = amount

    @abstractmethod
    def execute(self):
        pass


class DepositTransaction(Transaction):
    def __init__(self, transaction_id, account, amount):
        super().__init__(transaction_id, account, amount)

    def execute(self):
        self.account.deposit(self.amount)


class WithdrawTransaction(Transaction):
    def __init__(self, transaction_id, account, amount):
        super().__init__(transaction_id, account, amount)

    def execute(self):
        if self.account.get_balance() < self.amount:
            raise Exception("Insufficient funds in this account")
        self.account.withdraw(self.amount)


class CashDispenser:
    def __init__(self, initial_cash):
        self.cash_available = initial_cash
        self.lock = Lock()

    def dispense_cash(self, amount):
        with self.lock:
            if self.cash_available < amount:
                raise RuntimeError("Insufficient cash available in the ATM")
            self.cash_available -= amount
            print("Cash dispensed: ", amount)


class ATM:
    def __init__(self, banking_service, cash_dispenser):
        self.banking_service = banking_service
        self.cash_dispenser = cash_dispenser
        self.transaction_counter = 0
        self.transaction_lock = Lock()

    def authenticate_user(self, card):
        # Use card and pin to authenticate
        pass

    def check_balance(self, account_number):
        account = self.banking_service.get_account(account_number)
        return account.get_balance()
    
    def withdraw_cash(self, account_number, amount):
        account = self.banking_service.get_account(account_number)
        transaction = WithdrawTransaction(self.get_transaction_id, account, amount)
        self.banking_service.process_transaction(transaction)
        self.cash_dispenser.dispense_cash(int(amount))

    def deposit_cash(self, account_number, amount):
        account = self.banking_service.get_account(account_number)
        transaction = DepositTransaction(self.get_transaction_id, account, amount)
        self.banking_service.process_transaction(transaction)

    def get_transaction_id(self):
        with self.transaction_lock:
            self.transaction_counter += 1
            timestamp = datetime.datetime.now().strftime("%Y%m%D%H%M%S")
            return f"TXN{timestamp}{self.transaction_counter:010d}"
        

class ATMDemo:
    @staticmethod
    def run():
        banking_service = BankingService()
        cash_dispenser = CashDispenser(10000)
        atm = ATM(banking_service, cash_dispenser)

        account_number_1 = "1234567890"
        pin_1 = "1234"
        account_number_2 = "9876543210"
        pin_2 = "5678"

        banking_service.create_account(account_number_1, 1000.0)
        banking_service.create_account(account_number_2, 500.0)

        card1 = Card(account_number_1, pin_1)
        atm.authenticate_user(card1)
        card2 = Card(account_number_2, pin_2)
        atm.authenticate_user(card2)

        balance_1 = atm.check_balance(account_number_1)
        print("Account Number 1 Balance: ", balance_1)
        balance_2 = atm.check_balance(account_number_2)
        print("Account Number 2 Balance: ", balance_2)

        atm.withdraw_cash(account_number_1, 500.0)
        atm.withdraw_cash(account_number_2, 100.0)

        balance_1 = atm.check_balance(account_number_1)
        print("Account Number 1 Balance After Withdraw: ", balance_1)
        balance_2 = atm.check_balance(account_number_2)
        print("Account Number 2 Balance After Withdraw: ", balance_2)

if __name__ == "__main__":
    ATMDemo.run()