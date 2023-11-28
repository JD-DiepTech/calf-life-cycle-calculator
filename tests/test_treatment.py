from models.treatment import *
import pytest
import datetime as dt
import sys
import os

# This code snippet does the following:
#     1. It adjusts the Python path to include the parent directory
#        (which contains models and other packages).
#        This allows Python to locate and import modules from these directories.
#     2. Then, it imports the necessary modules from the models package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(scope="function")
def setup_birth():
    return Birth(dt.date(2023, 11, 20))


@pytest.fixture(scope="function")
def setup_bovalto1(setup_birth):
    return Bovalto1(setup_birth)


@pytest.fixture(scope="function")
def setup_dehorn(setup_bovalto1):
    return Dehorn(setup_bovalto1)


@pytest.fixture(scope="function")
def setup_restall(setup_dehorn):
    return Restall(setup_dehorn)


@pytest.fixture(scope="function")
def setup_sell(setup_birth):
    return Sell(setup_birth)


@pytest.fixture(scope="function")
def setup_bovalto2(setup_bovalto1):
    return Bovalto2(setup_bovalto1)


@pytest.fixture(scope="function")
def setup_ringworm1(setup_bovalto2):
    return Ringworm1(setup_bovalto2)


@pytest.fixture(scope="function")
def setup_ringworm2(setup_ringworm1):
    return Ringworm2(setup_ringworm1)


class TestTreatmentOperations:
    def test_birth_creation(self, setup_birth):
        assert setup_birth.actual_date is None
        assert setup_birth.name == "birth"
        assert setup_birth.display_name == "Birth"
        assert setup_birth.rest_days == 0
        assert setup_birth.expected_date == dt.date(2023, 11, 20)

    def test_bovalto1_creation(self, setup_bovalto1):
        assert setup_bovalto1.actual_date is None
        assert setup_bovalto1.name == "bovalto1"
        assert setup_bovalto1.display_name == "Bovalto1"
        assert setup_bovalto1.rest_days == 10
        assert setup_bovalto1.expected_date == dt.date(2023, 11, 30)

    def test_dehorn_creation(self, setup_dehorn):
        assert setup_dehorn.actual_date is None
        assert setup_dehorn.name == "dehorn"
        assert setup_dehorn.display_name == "Dehorn"
        assert setup_dehorn.rest_days == 5
        assert setup_dehorn.expected_date == dt.date(2023, 12, 5)

    def test_restall_creation(self, setup_restall):
        assert setup_restall.actual_date is None
        assert setup_restall.name == "restall"
        assert setup_restall.display_name == "Restall"
        assert setup_restall.rest_days == 5
        assert setup_restall.expected_date == dt.date(2023, 12, 11)

    def test_sell_creation(self, setup_sell):
        assert setup_sell.actual_date is None
        assert setup_sell.name == "sell"
        assert setup_sell.display_name == "Sell"
        assert setup_sell.rest_days == 28
        assert setup_sell.expected_date == dt.date(2023, 12, 19)

    def test_bovalto2_creation(self, setup_bovalto2):
        assert setup_bovalto2.actual_date is None
        assert setup_bovalto2.name == "bovalto2"
        assert setup_bovalto2.display_name == "Bovalto2"
        assert setup_bovalto2.rest_days == 21
        assert setup_bovalto2.expected_date == dt.date(2023, 12, 21)

    def test_ringworm1_creation(self, setup_ringworm1):
        assert setup_ringworm1.actual_date is None
        assert setup_ringworm1.name == "ringworm1"
        assert setup_ringworm1.display_name == "Ringworm1"
        assert setup_ringworm1.rest_days == 5
        assert setup_ringworm1.expected_date == dt.date(2023, 12, 26)

    def test_ringworm2_creation(self, setup_ringworm2):
        assert setup_ringworm2.actual_date is None
        assert setup_ringworm2.name == "ringworm2"
        assert setup_ringworm2.display_name == "Ringworm2"
        assert setup_ringworm2.rest_days == 14
        assert setup_ringworm2.expected_date == dt.date(2024, 1, 9)

    def test_birth_modification(self, setup_birth):
        setup_birth.actual_date = dt.date(2023, 11, 21)
        assert setup_birth.expected_date == dt.date(2023, 11, 20)
        assert setup_birth.actual_date == dt.date(2023, 11, 21)

    def test_bovalto1_modification(self, setup_bovalto1):
        setup_bovalto1.actual_date = dt.date(2023, 12, 1)
        assert setup_bovalto1.expected_date == dt.date(2023, 11, 30)
        assert setup_bovalto1.actual_date == dt.date(2023, 12, 1)

    def test_bovalto1_reference_modification(self, setup_birth):
        setup_birth.actual_date = dt.date(2023, 11, 21)
        bovalto1 = Bovalto1(setup_birth)
        assert bovalto1.expected_date == dt.date(2023, 12, 1)

    def test_dehorn_modification(self, setup_dehorn):
        setup_dehorn.actual_date = dt.date(2023, 12, 6)
        assert setup_dehorn.expected_date == dt.date(2023, 12, 5)
        assert setup_dehorn.actual_date == dt.date(2023, 12, 6)

    def test_dehorn_reference_modification(self, setup_bovalto1):
        setup_bovalto1.actual_date = dt.date(2023, 12, 1)
        dehorn = Dehorn(setup_bovalto1)
        assert dehorn.expected_date == dt.date(2023, 12, 6)

    def test_restall_modification(self, setup_restall):
        setup_restall.actual_date = dt.date(2023, 12, 12)
        assert setup_restall.expected_date == dt.date(2023, 12, 11)
        assert setup_restall.actual_date == dt.date(2023, 12, 12)

    def test_restall_reference_modification(self, setup_dehorn):
        setup_dehorn.actual_date = dt.date(2023, 12, 6)
        restall = Restall(setup_dehorn)
        assert restall.expected_date == dt.date(2023, 12, 11)

    def test_sell_modification(self, setup_sell):
        setup_sell.actual_date = dt.date(2023, 12, 20)
        assert setup_sell.expected_date == dt.date(2023, 12, 19)
        assert setup_sell.actual_date == dt.date(2023, 12, 20)

    def test_sell_reference_modification(self, setup_birth):
        setup_birth.actual_date = dt.date(2023, 11, 21)
        sell = Sell(setup_birth)
        assert sell.expected_date == dt.date(2023, 12, 19)

    def test_bovalto2_modification(self, setup_bovalto2):
        setup_bovalto2.actual_date = dt.date(2023, 12, 22)
        assert setup_bovalto2.expected_date == dt.date(2023, 12, 21)
        assert setup_bovalto2.actual_date == dt.date(2023, 12, 22)

    def test_bovalto2_reference_modification(self, setup_bovalto1):
        setup_bovalto1.actual_date = dt.date(2023, 12, 1)
        bovalto2 = Bovalto2(setup_bovalto1)
        assert bovalto2.expected_date == dt.date(2023, 12, 22)

    def test_ringworm1_modification(self, setup_ringworm1):
        setup_ringworm1.actual_date = dt.date(2023, 12, 27)
        assert setup_ringworm1.expected_date == dt.date(2023, 12, 26)
        assert setup_ringworm1.actual_date == dt.date(2023, 12, 27)

    def test_ringworm1_reference_modification(self, setup_bovalto2):
        setup_bovalto2.actual_date = dt.date(2023, 12, 22)
        ringworm1 = Ringworm1(setup_bovalto2)
        assert ringworm1.expected_date == dt.date(2023, 12, 27)

    def test_ringworm2_modification(self, setup_ringworm2):
        setup_ringworm2.actual_date = dt.date(2024, 1, 10)
        assert setup_ringworm2.expected_date == dt.date(2024, 1, 9)
        assert setup_ringworm2.actual_date == dt.date(2024, 1, 10)

    def test_ringworm2_reference_modification(self, setup_ringworm1):
        setup_ringworm1.actual_date = dt.date(2023, 12, 27)
        ringworm2 = Ringworm2(setup_ringworm1)
        assert ringworm2.expected_date == dt.date(2024, 1, 10)

    def test_compare_by_order_id(
        self,
        setup_birth,
        setup_bovalto1,
        setup_dehorn,
        setup_restall,
        setup_sell,
        setup_bovalto2,
        setup_ringworm1,
        setup_ringworm2,
    ):
        assert setup_birth < setup_bovalto1
        assert setup_bovalto1 < setup_dehorn
        assert setup_dehorn < setup_restall
        assert setup_restall < setup_sell
        # assert setup_sell < setup_bovalto2 # They have the same order id
        assert setup_bovalto2 < setup_ringworm1
        assert setup_ringworm1 < setup_ringworm2
        assert setup_birth <= setup_bovalto1
        assert setup_bovalto1 <= setup_dehorn
        assert setup_dehorn <= setup_restall
        assert setup_restall <= setup_sell
        # assert setup_sell <= setup_bovalto2 # They have the same order id
        assert setup_bovalto2 <= setup_ringworm1
        assert setup_ringworm1 <= setup_ringworm2
        assert setup_bovalto1 > setup_birth
        assert setup_dehorn > setup_bovalto1
        assert setup_restall > setup_dehorn
        assert setup_sell > setup_restall
        # assert setup_bovalto2 > setup_sell # They have the same order id
        assert setup_ringworm1 > setup_bovalto2
        assert setup_ringworm2 > setup_ringworm1
        assert setup_bovalto1 >= setup_birth
        assert setup_dehorn >= setup_bovalto1
        assert setup_restall >= setup_dehorn
        # assert setup_sell >= setup_restall # They have the same order id
        assert setup_bovalto2 >= setup_sell
        assert setup_ringworm1 >= setup_bovalto2
        assert setup_ringworm2 >= setup_ringworm1

    def test_compare_by_expected_dates(self, setup_birth, setup_bovalto1):
        assert setup_birth == setup_birth
        assert setup_bovalto1 == setup_bovalto1
        assert setup_birth != setup_bovalto1
        assert setup_bovalto1 != setup_birth

        birth = Birth(dt.date(2023, 11, 21))
        bovalto1 = Bovalto1(birth)

        assert setup_birth < birth
        assert setup_bovalto1 < bovalto1

    def test_compare_by_actual_dates(self, setup_birth):
        birth = Birth(dt.date(2023, 11, 20))
        assert setup_birth == birth

        birth.actual_date = dt.date(2023, 11, 21)
        assert setup_birth < birth

        birth.actual_date = None
        setup_birth.actual_date = dt.date(2023, 11, 21)
        assert setup_birth > birth

        setup_birth.actual_date = None
        birth.actual_date = None
        assert setup_birth == birth

    def test_get_week(self, setup_birth):
        assert setup_birth.get_week() == 47

        setup_birth.actual_date = dt.date(2023, 11, 27)
        assert setup_birth.get_week() == 48

        setup_birth.actual_date = None
        assert setup_birth.get_week() == 47

    def test_list_operations(self):
        treatments = [
            Birth(dt.date(2023, 11, 20)),
            Birth(dt.date(2023, 11, 21)),
            Birth(dt.date(2023, 11, 22)),
            Birth(dt.date(2023, 11, 23)),
            Birth(dt.date(2023, 11, 24)),
            Birth(dt.date(2023, 11, 19)),
        ]

        last_treatment = max(treatments, key=lambda treatment: treatment)
        assert last_treatment == Birth(dt.date(2023, 11, 24))

        first_treatment = min(treatments, key=lambda treatment: treatment)
        assert first_treatment == Birth(dt.date(2023, 11, 19))

        treatments.sort(key=lambda treatment: treatment)
        assert treatments == [
            Birth(dt.date(2023, 11, 19)),
            Birth(dt.date(2023, 11, 20)),
            Birth(dt.date(2023, 11, 21)),
            Birth(dt.date(2023, 11, 22)),
            Birth(dt.date(2023, 11, 23)),
            Birth(dt.date(2023, 11, 24)),
        ]
