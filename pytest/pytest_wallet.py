import pytest, json
from wallet import Wallet, InsufficientAmount 

# Getting Input File Name
@pytest.fixture()
def centralinfo(pytestconfig):
    return pytestconfig.getoption("centralinfo")

def test_print_centralinfo(centralinfo):
    print("command line param (filename):" + str(centralinfo))
    with open(centralinfo, "r") as fp:
        input_args = json.loads(fp.read())

    central = input_args["central_info"]
    base_url = central["central_base_url"]
    print(base_url)

@pytest.fixture
def my_wallet():
    '''Returns a Wallet instance with a zero balance'''
    return Wallet()

@pytest.mark.parametrize("earned,spent,expected", [
    (30, 10, 20),
    (20, 2, 18),
])

def test_transactions(my_wallet, earned, spent, expected):
    my_wallet.add_cash(earned)
    my_wallet.spend_cash(spent)
    assert my_wallet.balance == expected

