import hashlib
import pickle
import time
import uuid

from typing import List

class StorageException(Exception):
    pass


class TransactionNode(object):
    def __init__(self, before: str, amount: int, balance: float, after:str) -> str:

        if amount is None or balance is None:
            raise StorageException("ArgumentValueError")

        self.before = before
        self.time = int(time.time())
        self.amount = amount
        self.balance = balance
        self.after = after
        self.uuid = str(uuid.uuid4())
 
class Account(object):
    def __init__(self, account_id: str, pin: str, node: str):

        if account_id is None or pin is None or node is None:
            raise StorageException("ArgumentValueError")

        self.account_id = account_id
        self.pin = hashlib.sha256(pin.encode()).hexdigest() 
        self.trx = [node, node] 
               

class Storage(object):

    def __init__(self):
        self.accounts = {}


    def add_account(self, account_id: str, pin: str, balance: float) -> bool:

        if account_id not in self.accounts:
            node = TransactionNode(None, balance, balance, None)
            account = Account(account_id, pin, node.uuid) 

            self.write_nodes([node])

            self.accounts[account_id] = account
                
        else:
            raise StorageException("Account Already Exists")

        return True


    def get_account(self, account_id: str) -> Account:

        if account_id in self.accounts:
            return self.accounts[account_id]
        else:
            raise StorageException("Account Does Not Exist")


    def get_balance(self, account_id: str) -> float:

        if account_id in self.accounts:
            return self.get_last_transaction(account_id).balance


    def add_transaction(self, account_id, value):

        if account_id in self.accounts:

            last_trx = self.get_last_transaction(account_id)
            new_trx = TransactionNode(last_trx.uuid, value, (last_trx.balance + value), None)
            last_trx.after = new_trx.uuid

            self.write_nodes([new_trx, last_trx])

            self.accounts[account_id].trx[1] = new_trx.uuid

        else:
            raise StorageException("Account Does Not Exist")


    def get_last_transaction(self, account_id):
        if account_id in self.accounts:
            return self.read_node(self.accounts[account_id].trx[1])
        else:
            raise StorageException("Account Does Not Exist")

    def get_all_transactions(self, account_id):
        if account_id in self.accounts:

            transactions = []
            node = self.read_node(self.accounts[account_id].trx[0])

            while node.after != None:
                transactions.append((node.time, node.amount, node.balance))
                node = self.read_node(node.next)

            transactions.append((node.time, node.amount, node.balance))
            return transactions
            
        else:
            raise StorageException("Account Does Not Exist")
    



    def write_nodes(self, nodes: List[TransactionNode]) -> None:
        for node in nodes:
            try:
                with open("{}.transaction".format(node.uuid), "wb") as fh:
                    pickle.dump(node, fh)
            except Exception as ex:
                raise StorageException(ex)

    def read_node(self, node_uuid: str) -> TransactionNode:
        try:
            with open("{}.transaction".format(node_uuid), "rb") as fh:
                return pickle.load(fh)
        except Exception as ex:
            raise StorageException(ex)






