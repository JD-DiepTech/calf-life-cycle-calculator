from models.calf import FatteningCalf, BreedingCalf, Calf
from models.gender import Gender
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
def setup_fattening_calf():
    return FatteningCalf("2023-11-20", Gender.from_str("m"), 12345, True)


@pytest.fixture(scope="function")
def setup_breeding_calf():
    return BreedingCalf("2023-11-20", Gender.from_str("m"), 12345, True)


@pytest.fixture(scope="function")
def setup_calf():
    return Calf("2023-11-20", Gender.from_str("m"), 12345, True)


class TestCalfOperations:
    def test_fattening_calf_creation_default(self, setup_fattening_calf):
        assert setup_fattening_calf.gender == Gender.Male
        assert setup_fattening_calf.ear_tag == 12345
        assert setup_fattening_calf.dehorning_required
        assert setup_fattening_calf.birthday == dt.date(2023, 11, 20)
        assert setup_fattening_calf.birth.expected_date == dt.date(2023, 11, 20)
        assert setup_fattening_calf.bovalto_1.expected_date == dt.date(2023, 11, 30)
        assert setup_fattening_calf.dehorn.expected_date == dt.date(2023, 12, 5)
        assert setup_fattening_calf.restall.expected_date == dt.date(2023, 12, 11)
        assert setup_fattening_calf.sell.expected_date == dt.date(2023, 12, 19)

    def test_breeding_calf_creation_default(self, setup_breeding_calf):
        assert setup_breeding_calf.gender == Gender.Male
        assert setup_breeding_calf.ear_tag == 12345
        assert setup_breeding_calf.dehorning_required
        assert setup_breeding_calf.birthday == dt.date(2023, 11, 20)
        assert setup_breeding_calf.birth.expected_date == dt.date(2023, 11, 20)
        assert setup_breeding_calf.bovalto_1.expected_date == dt.date(2023, 11, 30)
        assert setup_breeding_calf.dehorn.expected_date == dt.date(2023, 12, 5)
        assert setup_breeding_calf.restall.expected_date == dt.date(2023, 12, 11)
        assert setup_breeding_calf.bovalto_2.expected_date == dt.date(2023, 12, 21)
        assert setup_breeding_calf.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert setup_breeding_calf.ringworm_2.expected_date == dt.date(2024, 1, 9)

    def test_fattening_calf_creation_without_dehorning(self):
        calf = FatteningCalf("2023-11-20", Gender.from_str("m"), 12345, False)

        assert calf.birth.expected_date == dt.date(2023, 11, 20)
        assert calf.bovalto_1.expected_date == dt.date(2023, 11, 30)
        assert calf.dehorn is None
        assert calf.restall.expected_date == dt.date(2023, 12, 5)
        assert calf.sell.expected_date == dt.date(2023, 12, 19)

    def test_fattening_calf_edit_birth(self):
        calf = FatteningCalf("2023-11-19", Gender.from_str("m"), 12345, True)
        assert calf.birth.expected_date == dt.date(2023, 11, 19)
        calf.edit_birth(dt.date(2023, 11, 20))

        assert calf.birth.actual_date == dt.date(2023, 11, 20)
        assert calf.bovalto_1.expected_date == dt.date(2023, 11, 30)
        assert calf.dehorn.expected_date == dt.date(2023, 12, 5)
        assert calf.restall.expected_date == dt.date(2023, 12, 11)
        assert calf.sell.expected_date == dt.date(2023, 12, 19)

    def test_fattening_calf_edit_bovalto1(self):
        calf = FatteningCalf("2023-11-19", Gender.from_str("m"), 12345, True)

        assert calf.birth.expected_date == dt.date(2023, 11, 19)
        assert calf.bovalto_1.expected_date == dt.date(2023, 11, 29)

        calf.edit_bovalto1(dt.date(2023, 11, 30))
        assert calf.bovalto_1.actual_date == dt.date(2023, 11, 30)
        assert calf.dehorn.expected_date == dt.date(2023, 12, 5)
        assert calf.restall.expected_date == dt.date(2023, 12, 11)
        assert calf.sell.expected_date == dt.date(2023, 12, 19)

    def test_fattening_calf_edit_dehorn(self):
        calf = FatteningCalf("2023-11-19", Gender.from_str("m"), 12345, True)

        assert calf.birth.expected_date == dt.date(2023, 11, 19)
        assert calf.bovalto_1.expected_date == dt.date(2023, 11, 29)
        assert calf.dehorn.expected_date == dt.date(2023, 12, 4)

        calf.edit_dehorn(dt.date(2023, 12, 5))
        assert calf.dehorn.actual_date == dt.date(2023, 12, 5)
        assert calf.restall.expected_date == dt.date(2023, 12, 11)
        assert calf.sell.expected_date == dt.date(2023, 12, 19)

    def test_fattening_calf_edit_restall(self):
        calf = FatteningCalf("2023-11-19", Gender.from_str("m"), 12345, True)

        assert calf.birth.expected_date == dt.date(2023, 11, 19)
        assert calf.bovalto_1.expected_date == dt.date(2023, 11, 29)
        assert calf.dehorn.expected_date == dt.date(2023, 12, 4)
        assert calf.restall.expected_date == dt.date(2023, 12, 11)

        calf.edit_restall(dt.date(2023, 12, 12))
        assert calf.restall.actual_date == dt.date(2023, 12, 12)
        assert calf.sell.expected_date == dt.date(2023, 12, 19)

    def test_fattening_calf_edit_sell(self):
        calf = FatteningCalf("2023-11-19", Gender.from_str("m"), 12345, True)

        assert calf.birth.expected_date == dt.date(2023, 11, 19)
        assert calf.bovalto_1.expected_date == dt.date(2023, 11, 29)
        assert calf.dehorn.expected_date == dt.date(2023, 12, 4)
        assert calf.restall.expected_date == dt.date(2023, 12, 11)
        assert calf.sell.expected_date == dt.date(2023, 12, 19)

        calf.edit_sell(dt.date(2023, 12, 19))
        assert calf.sell.expected_date == dt.date(2023, 12, 19)

    def test_breeding_calf_edit_birth(self):
        calf = BreedingCalf("2023-11-19", Gender.from_str("m"), 12345, True)
        assert calf.birth.expected_date == dt.date(2023, 11, 19)
        calf.edit_birth(dt.date(2023, 11, 20))

        assert calf.birth.actual_date == dt.date(2023, 11, 20)
        assert calf.bovalto_1.expected_date == dt.date(2023, 11, 30)
        assert calf.dehorn.expected_date == dt.date(2023, 12, 5)
        assert calf.restall.expected_date == dt.date(2023, 12, 11)
        assert calf.bovalto_2.expected_date == dt.date(2023, 12, 21)
        assert calf.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf.ringworm_2.expected_date == dt.date(2024, 1, 9)

    def test_breeding_calf_edit_bovalto1(self):
        calf = BreedingCalf("2023-11-19", Gender.from_str("m"), 12345, True)
        assert calf.birth.expected_date == dt.date(2023, 11, 19)
        assert calf.bovalto_1.expected_date == dt.date(2023, 11, 29)

        calf.edit_bovalto1(dt.date(2023, 11, 30))

        assert calf.bovalto_1.actual_date == dt.date(2023, 11, 30)
        assert calf.dehorn.expected_date == dt.date(2023, 12, 5)
        assert calf.restall.expected_date == dt.date(2023, 12, 11)
        assert calf.bovalto_2.expected_date == dt.date(2023, 12, 21)
        assert calf.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf.ringworm_2.expected_date == dt.date(2024, 1, 9)

    def test_breeding_calf_edit_dehorn(self):
        calf = BreedingCalf("2023-11-19", Gender.from_str("m"), 12345, True)
        assert calf.birth.expected_date == dt.date(2023, 11, 19)
        assert calf.bovalto_1.expected_date == dt.date(2023, 11, 29)
        assert calf.dehorn.expected_date == dt.date(2023, 12, 4)

        calf.edit_dehorn(dt.date(2023, 12, 5))

        assert calf.dehorn.actual_date == dt.date(2023, 12, 5)
        assert calf.restall.expected_date == dt.date(2023, 12, 11)
        assert calf.bovalto_2.expected_date == dt.date(2023, 12, 20)
        assert calf.ringworm_1.expected_date == dt.date(2023, 12, 25)
        assert calf.ringworm_2.expected_date == dt.date(2024, 1, 8)

    def test_breeding_calf_edit_restall(self):
        calf = BreedingCalf("2023-11-19", Gender.from_str("m"), 12345, True)
        assert calf.birth.expected_date == dt.date(2023, 11, 19)
        assert calf.bovalto_1.expected_date == dt.date(2023, 11, 29)
        assert calf.dehorn.expected_date == dt.date(2023, 12, 4)
        assert calf.restall.expected_date == dt.date(2023, 12, 11)

        calf.edit_restall(dt.date(2023, 12, 12))

        assert calf.restall.actual_date == dt.date(2023, 12, 12)
        assert calf.bovalto_2.expected_date == dt.date(2023, 12, 20)
        assert calf.ringworm_1.expected_date == dt.date(2023, 12, 25)
        assert calf.ringworm_2.expected_date == dt.date(2024, 1, 8)

    def test_breeding_calf_edit_bovalto2(self):
        calf = BreedingCalf("2023-11-19", Gender.from_str("m"), 12345, True)
        assert calf.birth.expected_date == dt.date(2023, 11, 19)
        assert calf.bovalto_1.expected_date == dt.date(2023, 11, 29)
        assert calf.dehorn.expected_date == dt.date(2023, 12, 4)
        assert calf.restall.expected_date == dt.date(2023, 12, 11)
        assert calf.bovalto_2.expected_date == dt.date(2023, 12, 20)

        calf.edit_bovalto2(dt.date(2023, 12, 21))

        assert calf.bovalto_2.actual_date == dt.date(2023, 12, 21)
        assert calf.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf.ringworm_2.expected_date == dt.date(2024, 1, 9)

    def test_breeding_calf_edit_ringworm1(self):
        calf = BreedingCalf("2023-11-19", Gender.from_str("m"), 12345, True)
        assert calf.birth.expected_date == dt.date(2023, 11, 19)
        assert calf.bovalto_1.expected_date == dt.date(2023, 11, 29)
        assert calf.dehorn.expected_date == dt.date(2023, 12, 4)
        assert calf.restall.expected_date == dt.date(2023, 12, 11)
        assert calf.bovalto_2.expected_date == dt.date(2023, 12, 20)
        assert calf.ringworm_1.expected_date == dt.date(2023, 12, 25)

        calf.edit_ringworm1(dt.date(2023, 12, 26))

        assert calf.ringworm_1.actual_date == dt.date(2023, 12, 26)
        assert calf.ringworm_2.expected_date == dt.date(2024, 1, 9)

    def test_breeding_calf_edit_ringworm2(self):
        calf = BreedingCalf("2023-11-19", Gender.from_str("m"), 12345, True)
        assert calf.birth.expected_date == dt.date(2023, 11, 19)
        assert calf.bovalto_1.expected_date == dt.date(2023, 11, 29)
        assert calf.dehorn.expected_date == dt.date(2023, 12, 4)
        assert calf.restall.expected_date == dt.date(2023, 12, 11)
        assert calf.bovalto_2.expected_date == dt.date(2023, 12, 20)
        assert calf.ringworm_1.expected_date == dt.date(2023, 12, 25)
        assert calf.ringworm_2.expected_date == dt.date(2024, 1, 8)

        calf.edit_ringworm2(dt.date(2024, 1, 9))

        assert calf.ringworm_2.actual_date == dt.date(2024, 1, 9)

    @pytest.mark.parametrize(
        "calf",
        [
            pytest.param(
                FatteningCalf("2023-11-20", Gender.from_str("m"), 12345, True),
                id="fattening_calf",
            ),
            pytest.param(
                BreedingCalf("2023-11-20", Gender.from_str("m"), 12345, True),
                id="breeding_calf",
            ),
        ],
    )
    def test_change_ear_tag(self, calf):
        assert calf.ear_tag == 12345
        calf.change_ear_tag(54321)
        assert calf.ear_tag == 54321

    @pytest.mark.parametrize(
        "calf",
        [
            pytest.param(
                FatteningCalf("2023-11-20", Gender.from_str("m"), 12345, True),
                id="fattening_calf",
            ),
            pytest.param(
                BreedingCalf("2023-11-20", Gender.from_str("m"), 12345, True),
                id="breeding_calf",
            ),
        ],
    )
    def test_edit_gender(self, calf):
        assert calf.gender == Gender.Male
        calf.edit_gender(Gender.Female)
        assert calf.gender == Gender.Female

    @pytest.mark.parametrize(
        "calf",
        [
            pytest.param(
                FatteningCalf("2023-11-20", Gender.from_str("m"), 12345, True),
                id="fattening_calf",
            ),
            pytest.param(
                BreedingCalf("2023-11-20", Gender.from_str("m"), 12345, True),
                id="breeding_calf",
            ),
        ],
    )
    def test_reset_dehorn(self, calf):
        date = dt.date(2023, 11, 20)
        assert calf.dehorning_required
        calf.reset_dehorn(date, False)
        assert not calf.dehorning_required
        assert calf.dehorn is None


class TestFatteningCalf:
    def test_calf_type(self, setup_fattening_calf):
        assert setup_fattening_calf.calf_type == "fattening"


class TestBreedingCalf:
    def test_calf_type(self, setup_breeding_calf):
        assert setup_breeding_calf.calf_type == "breeding"

    def test_edit_ringworm1_while_None(self, setup_breeding_calf):
        calf = setup_breeding_calf
        assert calf.ringworm_1.expected_date == dt.date(2023, 12, 26)

        calf.delete_ringworm()
        assert calf.ringworm_1 is None
        assert calf.ringworm_2 is None

        calf.edit_ringworm1(dt.date(2023, 12, 25))
        assert calf.ringworm_1 is not None
        assert calf.ringworm_2 is not None
        assert calf.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf.ringworm_1.actual_date == dt.date(2023, 12, 25)
        assert calf.ringworm_2.expected_date == dt.date(2024, 1, 8)
        assert calf.ringworm_2.actual_date is None
