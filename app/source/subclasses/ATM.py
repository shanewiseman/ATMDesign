from datetime import datetime
from typing import List
from types import SimpleNamespace
import hashlib
import json
import jwt
import time

from Storage import StorageException, Storage

class ATMException(Exception):
    pass

class ATMToken(object):

    @staticmethod
    def create_token(account_id: str, key: str) -> str:

        token_data = {
                "account_id": account_id,
                "created": int(time.time())
        }

        return jwt.encode(token_data, key, algorithm="HS256")
    
    @staticmethod
    def decode_token(token: str, key: str) -> dict: 
        token_data = json.dumps(jwt.decode(token, key, algorithms=["HS256"]))
        return json.loads(token_data, object_hook= lambda x: SimpleNamespace(**x))


class ATM(object):
    def __init__(self):
        self.secret_key = "secret"
        self.auth_time = 120
        self.overdraft_penalty = 5
        self.cash_available = 10000
        self.cash_multiples = 20
        self.storage = Storage()
        self.logged_in = {}

        self.dummy_data = [("2859459814","7386",10.24), ("1434597300","4557",90000.55),("7089382418","0075",0.00), ("2001377812","5950",60.00)]

    def insert_dummy_data(self):
        #for time sake, just inserting dummy data, would normally parse this from file
        for account in self.dummy_data:
            self.storage.add_account(account[0], account[1], account[2])

    def is_authed(self, token: str) -> str:
        try:
            data = ATMToken.decode_token(token, self.secret_key)
            if data.account_id in self.logged_in:
                # is login expired?
                if int(time.time()) - self.logged_in[data.account_id] >= self.auth_time:
                    self.logged_in.pop(account_id, None)
                    raise ATMException("Token Expired")
               
                # refresh login time
                self.logged_in[data.account_id] = int(time.time())
                return data.account_id
            else:
                raise ATMException("Authorization failed.")

        except Exception as ex:
            raise ATMException("Invalid Token")


    def authorize(self, account_id: str, pin: str) -> str:
        try:
            if self.storage.get_account(account_id).pin == hashlib.sha256(pin.encode()).hexdigest():
                    self.logged_in[account_id] = int(time.time())
                    return True, "{} successfully authorized.".format(account_id), ATMToken.create_token(account_id, self.secret_key)
            else:
                return False, "Authorization failed."

        except StorageException:
            return False, "Authorization failed."


    def withdraw(self, value: int, token: str) -> (bool,str):
        account_id = None
        try:
            account_id = self.is_authed(token)
        except ATMException as ex:
            return False, "Authorization required."

        if value <= 0 or value % self.cash_multiples != 0:
            raise ATMException("Invalid Transaction Amount")

        balance = self.storage.get_balance(account_id)


        if balance < 0:
            return False, "Your account is overdrawn! You may not make withdrawals at this time." 

        if int(self.cash_available / self.cash_multiples) < 1:
            return False, "Unable to process your withdrawal at this time."


        # does the atm have cash?
        if self.cash_available < value:
            value = int(self.cash_available / self.cash_multiples) * self.cash_multiples

            self.storage.add_transaction(account_id, (value + self.overdraft_penalty) * -1)
            self.cash_available -= value 

            # does user have enough money?
            if balance < value:
                return False, "You have been charged an overdraft fee of ${}. Current balance: {:.2f}".format(
                    self.overdraft_penalty, self.storage.get_balance(account_id))
            else:
               return False, "Unable to dispense full amount requested at this time." 

        else:

            # does user have enough money?
            if balance < value:
                self.storage.add_transaction(account_id, (value + self.overdraft_penalty) * -1)
                self.cash_available -= (value + self.overdraft_penalty)
                return True, "You have been charged an overdraft fee of ${}. Current balance: {:.2f}".format(
                    self.overdraft_penalty, self.storage.get_balance(account_id))
            else:

                self.storage.add_transaction(account_id, value * -1)
                self.cash_available -= value
                return True, "Current balance: {:.2f}".format(self.storage.get_balance(account_id))



    def deposit(self, value: float, token: str) -> (bool, str):
        account_id = None
        try:
            account_id = self.is_authed(token)
        except ATMException:
            return False, "Authorization required."

        self.storage.add_transaction(account_id, float(value))
        return True, "Current balance: {:.2f}".format(self.storage.get_balance(account_id))



    def get_balance(self, token: str) -> str:
        account_id = None
        try:
            account_id = self.is_authed(token)
        except ATMException:
            return False, "Authorization required."

        return True, "Current balance: {:.2f}".format(self.storage.get_balance(account_id))

    def get_history(self, token: str) -> List[str]:
        account_id = None
        try:
            account_id = self.is_authed(token)
        except ATMException:
            return False, "Authorization required."
        
        transactions = [] 
        for line in self.storage.get_all_transactions(account_id):
            transactions.append([str(datetime.fromtimestamp(line[0])),line[1], line[2]])

        # wont consider account init as "history", which contains one entry
        if len(transactions) < 2:
            return False, "No History Found"

        return True, transactions

    def log_out(self, token: str) -> (bool, str):
        account_id = None
        try:
            account_id = self.is_authed(token) 
        except ATMException:
            return False, "No Account is currently authorized"


        self.logged_in.pop(account_id, None)
        return True, "Account {} logged out. ".format(account_id)
