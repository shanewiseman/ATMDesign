import pytest
import hashlib

dummy_data = [("2859459814","7386",10.24), ("1434597300","4557",90000.55),("7089382418","0075",0.00), ("2001377812","5950",60.00)]

def test_ATM_dummy(atm):


    assert atm.storage.get_account(atm.dummy_data[0][0]).pin == hashlib.sha256(atm.dummy_data[0][1].encode()).hexdigest()
    assert atm.storage.get_balance(atm.dummy_data[0][0]) == atm.dummy_data[0][2]

    assert atm.storage.get_account(atm.dummy_data[1][0]).pin == hashlib.sha256(atm.dummy_data[1][1].encode()).hexdigest()
    assert atm.storage.get_balance(atm.dummy_data[1][0]) == atm.dummy_data[1][2]
    
    assert atm.storage.get_account(atm.dummy_data[2][0]).pin == hashlib.sha256(atm.dummy_data[2][1].encode()).hexdigest()
    assert atm.storage.get_balance(atm.dummy_data[2][0]) == atm.dummy_data[2][2]


@pytest.mark.parametrize(
    "account_id, pin, result, message",
    [(dummy_data[0][0], dummy_data[0][1], True, "{} successfully authorized.".format(dummy_data[0][0])),
    (dummy_data[0][0], "wrong_pin", False, "Authorization failed."),
    ("wrong_id", "wrong_pin", False, "Authorization failed.")]
)
def test_ATM_Login(atm, account_id, pin, result, message):

    response = atm.authorize(account_id, pin)

    assert  response[0] == result and response[1] == message


@pytest.mark.parametrize(
    "account_id, pin, amount, result, message",
    [(dummy_data[3][0], dummy_data[3][1], 20, True, "Current balance: {}".format(dummy_data[3][2] - 20)),
    (dummy_data[3][0], dummy_data[3][1], 80, True, "You have been charged an overdraft fee of $5. Current balance: {}".format(dummy_data[3][2] - 85)),
    (dummy_data[1][0], dummy_data[1][1], 10020, True, "Unable to dispense full amount requested at this time.".format(dummy_data[1][2] - 10000)),
    (dummy_data[3][0], "bad_pin", 20, False, "Authorization required.")]
)
def test_ATM_Withdrawl(atm, account_id, pin, amount, result, message): 
    token = atm.authorize(account_id, pin)[-1]
    print(token)
    response = atm.withdraw(amount, token)
    print(response)
    
    assert  response[0] == result and response[1] == message

@pytest.mark.parametrize(
    "account_id, pin, amount, result, message",
    [(dummy_data[1][0], dummy_data[1][1], 10000, False, "Unable to process your withdrawal at this time." ),
    (dummy_data[3][0], dummy_data[3][1], 80, False, "Your account is overdrawn! You may not make withdrawals at this time.")]
)
def test_ATM_Double_Withdrawl(atm, account_id, pin, amount, result, message):
    token = atm.authorize(account_id, pin)[-1]
    atm.withdraw(amount, token)
    response = atm.withdraw(20, token)

    assert  response[0] == result and response[1] == message


@pytest.mark.parametrize(
    "account_id, pin, amount, result, message",
    [(dummy_data[1][0], dummy_data[1][1], 20, True, "Current balance: {}".format(dummy_data[1][2] + 20))]
)
def test_ATM_Deposit(atm, account_id, pin, amount, result, message):
    token = atm.authorize(account_id, pin)[-1]
    response = atm.deposit(amount, token)
    
    assert  response[0] == result and response[1] == message

@pytest.mark.parametrize(
    "account_id, pin, result, message",
    [(dummy_data[1][0], dummy_data[1][1], True, "Current balance: {}".format(dummy_data[1][2]))]
)
def test_ATM_Balance(atm, account_id, pin, result, message):
    token = atm.authorize(account_id, pin)[-1]
    response = atm.get_balance(token)
    
    assert  response[0] == result and response[1] == message


@pytest.mark.parametrize(
    "account_id, pin, result, message",
    [(dummy_data[1][0], dummy_data[1][1], False, "No history found")]
)
def test_ATM_history(atm, account_id, pin, result, message):

    token = atm.authorize(account_id, pin)[-1]
    response = atm.get_history(token)

    assert  response[0] == result #and response[1] == message
