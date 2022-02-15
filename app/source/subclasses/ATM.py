from typing import List
from types import SimpleNamespace
import json
import jwt
import time


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
        #LOG
        return json.loads(token_data, object_hook= lambda x: SimpleNamespace(**x))


class ATM(object):
    def __init__(self):
        #key
        pass
    def authorize(self, account_id: str, pin: str) -> str:
        pass

    def withdrawl(self, value: int, token: str) -> bool:
        pass

    def deposit(self, value: int, token: str) -> bool:
        pass

    def get_balance(self, token: str) -> str:
        pass

    def get_history(self, token: str) -> List[str]:
        pass

    def log_out(self, token: str) -> bool:
        pass


