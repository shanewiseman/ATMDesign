import pytest
import hashlib

from Storage import StorageException, TransactionNode, Account, Storage


@pytest.mark.parametrize(
    "before, amount, balance, after, exception, v_before, v_amount, v_balance, v_after", 
    [(None, 10, 10, None, False, None, 10, 10, None),
    (None, 10, 10, "abcd", False, None, 10, 10, "abcd"),
    ("1234", 10, 10, "abcd", False, "1234", 10, 10, "abcd"),
    (None, None, None, None, True, None, None, None, None )]

)
def test_TransactionNode(before, amount, balance, after, exception, v_before, v_amount, v_balance, v_after):
    try:
        node = TransactionNode(before,amount, balance, after)
        assert node.before == v_before and node.amount == v_amount and node.balance == v_balance and node.after == v_after
    except StorageException:
        assert exception 


@pytest.mark.parametrize(
        "account_id, pin, node, exception, v_account_id, v_pin, v_node",
        [("1234", "5678", "9", False, "1234", hashlib.sha256("5678".encode()).hexdigest(), "9"),
        (None, "1234", "1234", True, None, None, None),
        ("1234", None, "1234", True, None, None, None),
        ("1234", "1234", None, True, None, None, None)]
)
def test_Account(account_id, pin, node, exception, v_account_id, v_pin, v_node):
    try:
        account = Account(account_id, pin, node)
        assert account.account_id == v_account_id and account.pin == v_pin and account.trx[0] == v_node and account.trx[1] == v_node
    except StorageException:
        assert exception



@pytest.mark.parametrize(
        "account_id, pin, balance, exception",
        [("1234", "5678", 0, False)]
)
def test_Storage(account_id, pin, balance, exception, mocker):
    
    fake_node = TransactionNode(None, balance, balance, None)
    mocker.patch('Storage.Storage.write_nodes', return_value=None)
    mocker.patch('Storage.Storage.get_last_transaction', return_value=fake_node)
    try:
        storage = Storage()
        storage.add_account(account_id, pin, balance)
        storage.add_transaction(account_id, 10)

        assert fake_node.uuid != storage.accounts[account_id].trx[1]
    except StorageException:
        assert exception





