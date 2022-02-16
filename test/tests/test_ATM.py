import pytest
import hashlib

from ATM import ATM


#@pytest.mark.parametrize(
#    [(),]

#)


def test_ATM_Login():
    atm = ATM()

    atm.insert_dummy_data()
