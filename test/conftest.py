import pytest
from ATM import ATM


@pytest.fixture(scope="function")
def atm():
    atm = ATM()
    atm.insert_dummy_data()
    yield atm
