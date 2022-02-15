import pickle
import hashlib
import uuid

class StorageException(Exception):
    pass


class Account(object):
    def __init__(self, account_id: str, pin: str, node: TransactionNode):
        self.account_id = account_id
        self.pin = hashlib.sha256(pin.encode()).hexdigest() 
        self.transactions = [node, node] 
        
class TransactionNode(object):
    def __init__(self, before: str, amount: int, balance: int, after:str) -> str:
        self.before = before
        self.time = int(time.time())
        self.balance = balance
        self.after = after
        self.uuid = str(uuid.uuid4())
        
        return self.uuid
    

        

class Storage(object):
    def __init__(self):
        self.accounts = []
    
    def add_account(self, account_id: str, pin: str, balance: int):
        if account_id not in self.accounts:
            node = TransactionNode(None, balance, balance, None)
            account = Account(account_id, pin, node) 

            node.write()

            self.accounts.append(account)
                
        else:
            raise StorageException("Account Already Exists")

        return True

    def add_transaction(self, account_id, node):


    def get_last_transaction(self, account_id):
        pass

    def get_all_transactions(self, account_id):
        pass






