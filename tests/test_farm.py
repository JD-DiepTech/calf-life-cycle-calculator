from models.calf import FatteningCalf, BreedingCalf
from models.gender import Gender
from models.treatment import (
    Birth,
    Bovalto1,
    Dehorn,
    Restall,
    Sell,
    Bovalto2,
    Ringworm1,
    Ringworm2,
)
from models.farm import Farm
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


class TestFarm:
    def test_add_calf(self):
        farm = Farm()
        calf = BreedingCalf("2023-11-20", Gender.from_str("m"), 12345, True)
        farm.add_calf(calf)
        assert farm.get_calf(12345) == calf
        assert farm.get_calves() == [calf]
        assert farm.get_ear_tags() == [12345]
        assert len(farm) == 1
        assert farm.__sizeof__() == 1
        assert str(farm) == "Farm with 0 fattening calves and 1 breeding calves"
        assert repr(farm) == "Farm([], [BreedingCalf(12345)])"
        assert farm.get_calf(12345).ringworm_1 is None
        assert farm.get_calf(12345).ringworm_2 is None

    def test_add_calves(self):
        farm = Farm()

        calf_1 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12341, True)
        calf_2 = BreedingCalf("2023-11-18", Gender.from_str("m"), 12342, True)
        calf_3 = BreedingCalf("2023-11-21", Gender.from_str("m"), 12343, True)
        calf_4 = BreedingCalf("2023-11-24", Gender.from_str("m"), 12344, True)
        calf_5 = BreedingCalf("2023-11-27", Gender.from_str("m"), 12345, True)

        farm.add_calves([calf_1, calf_2, calf_3, calf_4, calf_5])
        assert len(farm) == 5
        assert farm.get_calves() == [calf_1, calf_2, calf_3, calf_4, calf_5]
        assert farm.get_ear_tags() == [12341, 12342, 12343, 12344, 12345]

    def test_add_calf_same_ear_tag(self):
        farm = Farm()

        calf_1 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12341, True)
        calf_2 = BreedingCalf("2023-11-18", Gender.from_str("m"), 12341, True)

        farm.add_calf(calf_1)

        with pytest.raises(Exception) as exc_info:
            farm.add_calf(calf_2)

        assert str(exc_info.value) == "Ear tag 12341 already exists"

    def test_delete_calf(self):
        farm = Farm()
        calf = BreedingCalf("2023-11-20", Gender.from_str("m"), 12345, True)
        farm.add_calf(calf)
        assert len(farm) == 1

        farm.delete_calf(12345)
        assert len(farm) == 0

    def test_ringworm_creation_born_same_date(self):
        farm = Farm()
        calf_1 = BreedingCalf("2023-11-20", Gender.from_str("m"), 12341, True)
        calf_2 = BreedingCalf("2023-11-20", Gender.from_str("m"), 12342, True)
        calf_3 = BreedingCalf("2023-11-20", Gender.from_str("m"), 12343, True)
        calf_4 = BreedingCalf("2023-11-20", Gender.from_str("m"), 12344, True)
        calf_5 = BreedingCalf("2023-11-20", Gender.from_str("m"), 12345, True)
        assert calf_1.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf_2.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf_3.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf_4.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf_5.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf_1.ringworm_2.expected_date == dt.date(2024, 1, 9)
        assert calf_2.ringworm_2.expected_date == dt.date(2024, 1, 9)
        assert calf_3.ringworm_2.expected_date == dt.date(2024, 1, 9)
        assert calf_4.ringworm_2.expected_date == dt.date(2024, 1, 9)
        assert calf_5.ringworm_2.expected_date == dt.date(2024, 1, 9)

        farm.add_calf(calf_1)
        calf_1 = farm.get_calf(12341)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None

        farm.add_calf(calf_2)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None
        assert calf_2.ringworm_1 is None
        assert calf_2.ringworm_2 is None

        farm.add_calf(calf_3)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        calf_3 = farm.get_calf(12343)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None
        assert calf_2.ringworm_1 is None
        assert calf_2.ringworm_2 is None
        assert calf_3.ringworm_1 is None
        assert calf_3.ringworm_2 is None

        farm.add_calf(calf_4)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        calf_3 = farm.get_calf(12343)
        calf_4 = farm.get_calf(12344)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None
        assert calf_2.ringworm_1 is None
        assert calf_2.ringworm_2 is None
        assert calf_3.ringworm_1 is None
        assert calf_3.ringworm_2 is None
        assert calf_4.ringworm_1 is None
        assert calf_4.ringworm_2 is None

        farm.add_calf(calf_5)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        calf_3 = farm.get_calf(12343)
        calf_4 = farm.get_calf(12344)
        calf_5 = farm.get_calf(12345)
        assert calf_1.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf_2.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf_3.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf_4.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf_5.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf_1.ringworm_2.expected_date == dt.date(2024, 1, 9)
        assert calf_2.ringworm_2.expected_date == dt.date(2024, 1, 9)
        assert calf_3.ringworm_2.expected_date == dt.date(2024, 1, 9)
        assert calf_4.ringworm_2.expected_date == dt.date(2024, 1, 9)
        assert calf_5.ringworm_2.expected_date == dt.date(2024, 1, 9)

    def test_ringworm_creation_same_week(self):
        farm = Farm()
        calf_1 = BreedingCalf("2023-11-20", Gender.from_str("m"), 12341, True)
        calf_2 = BreedingCalf("2023-11-20", Gender.from_str("m"), 12342, True)
        calf_3 = BreedingCalf("2023-11-20", Gender.from_str("m"), 12343, True)
        calf_4 = BreedingCalf("2023-11-20", Gender.from_str("m"), 12344, True)
        calf_5 = BreedingCalf("2023-11-20", Gender.from_str("m"), 12345, True)

        calf_1.edit_bovalto2(dt.date(2023, 12, 20))
        calf_2.edit_bovalto2(dt.date(2023, 12, 21))
        calf_3.edit_bovalto2(dt.date(2023, 12, 22))
        calf_4.edit_bovalto2(dt.date(2023, 12, 23))
        calf_5.edit_bovalto2(dt.date(2023, 12, 24))

        assert calf_1.ringworm_1.expected_date == dt.date(2023, 12, 25)
        assert calf_2.ringworm_1.expected_date == dt.date(2023, 12, 26)
        assert calf_3.ringworm_1.expected_date == dt.date(2023, 12, 27)
        assert calf_4.ringworm_1.expected_date == dt.date(2023, 12, 28)
        assert calf_5.ringworm_1.expected_date == dt.date(2023, 12, 29)
        assert calf_1.ringworm_2.expected_date == dt.date(2024, 1, 8)
        assert calf_2.ringworm_2.expected_date == dt.date(2024, 1, 9)
        assert calf_3.ringworm_2.expected_date == dt.date(2024, 1, 10)
        assert calf_4.ringworm_2.expected_date == dt.date(2024, 1, 11)
        assert calf_5.ringworm_2.expected_date == dt.date(2024, 1, 12)

        farm.add_calf(calf_1)
        calf_1 = farm.get_calf(12341)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None

        farm.add_calf(calf_2)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None
        assert calf_2.ringworm_1 is None
        assert calf_2.ringworm_2 is None

        farm.add_calf(calf_3)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        calf_3 = farm.get_calf(12343)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None
        assert calf_2.ringworm_1 is None
        assert calf_2.ringworm_2 is None
        assert calf_3.ringworm_1 is None
        assert calf_3.ringworm_2 is None

        farm.add_calf(calf_4)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        calf_3 = farm.get_calf(12343)
        calf_4 = farm.get_calf(12344)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None
        assert calf_2.ringworm_1 is None
        assert calf_2.ringworm_2 is None
        assert calf_3.ringworm_1 is None
        assert calf_3.ringworm_2 is None
        assert calf_4.ringworm_1 is None
        assert calf_4.ringworm_2 is None

        farm.add_calf(calf_5)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        calf_3 = farm.get_calf(12343)
        calf_4 = farm.get_calf(12344)
        calf_5 = farm.get_calf(12345)
        assert calf_1.ringworm_1.expected_date == dt.date(2023, 12, 29)
        assert calf_2.ringworm_1.expected_date == dt.date(2023, 12, 29)
        assert calf_3.ringworm_1.expected_date == dt.date(2023, 12, 29)
        assert calf_4.ringworm_1.expected_date == dt.date(2023, 12, 29)
        assert calf_5.ringworm_1.expected_date == dt.date(2023, 12, 29)
        assert calf_1.ringworm_2.expected_date == dt.date(2024, 1, 12)
        assert calf_2.ringworm_2.expected_date == dt.date(2024, 1, 12)
        assert calf_3.ringworm_2.expected_date == dt.date(2024, 1, 12)
        assert calf_4.ringworm_2.expected_date == dt.date(2024, 1, 12)
        assert calf_5.ringworm_2.expected_date == dt.date(2024, 1, 12)

    def test_ringworm_creation_different_weeks(self):
        farm = Farm()
        calf_1 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12341, True)
        calf_2 = BreedingCalf("2023-11-18", Gender.from_str("m"), 12342, True)
        calf_3 = BreedingCalf("2023-11-21", Gender.from_str("m"), 12343, True)
        calf_4 = BreedingCalf("2023-11-24", Gender.from_str("m"), 12344, True)
        calf_5 = BreedingCalf("2023-11-27", Gender.from_str("m"), 12345, True)

        assert calf_1.ringworm_1.expected_date == dt.date(2023, 12, 25)
        assert calf_2.ringworm_1.expected_date == dt.date(2023, 12, 25)
        assert calf_3.ringworm_1.expected_date == dt.date(2023, 12, 27)
        assert calf_4.ringworm_1.expected_date == dt.date(2024, 1, 1)
        assert calf_5.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_1.ringworm_2.expected_date == dt.date(2024, 1, 8)
        assert calf_2.ringworm_2.expected_date == dt.date(2024, 1, 8)
        assert calf_3.ringworm_2.expected_date == dt.date(2024, 1, 10)
        assert calf_4.ringworm_2.expected_date == dt.date(2024, 1, 15)
        assert calf_5.ringworm_2.expected_date == dt.date(2024, 1, 16)

        farm.add_calf(calf_1)
        calf_1 = farm.get_calf(12341)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None

        farm.add_calf(calf_2)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None
        assert calf_2.ringworm_1 is None
        assert calf_2.ringworm_2 is None

        farm.add_calf(calf_3)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        calf_3 = farm.get_calf(12343)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None
        assert calf_2.ringworm_1 is None
        assert calf_2.ringworm_2 is None
        assert calf_3.ringworm_1 is None
        assert calf_3.ringworm_2 is None

        farm.add_calf(calf_4)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        calf_3 = farm.get_calf(12343)
        calf_4 = farm.get_calf(12344)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None
        assert calf_2.ringworm_1 is None
        assert calf_2.ringworm_2 is None
        assert calf_3.ringworm_1 is None
        assert calf_3.ringworm_2 is None
        assert calf_4.ringworm_1 is None
        assert calf_4.ringworm_2 is None

        farm.add_calf(calf_5)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        calf_3 = farm.get_calf(12343)
        calf_4 = farm.get_calf(12344)
        calf_5 = farm.get_calf(12345)
        assert calf_1.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_2.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_3.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_4.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_5.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_1.ringworm_2.expected_date == dt.date(2024, 1, 16)
        assert calf_2.ringworm_2.expected_date == dt.date(2024, 1, 16)
        assert calf_3.ringworm_2.expected_date == dt.date(2024, 1, 16)
        assert calf_4.ringworm_2.expected_date == dt.date(2024, 1, 16)
        assert calf_5.ringworm_2.expected_date == dt.date(2024, 1, 16)

    def test_ringworm_creation_more_calves(self):
        farm = Farm()
        calf_1 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12341, True)
        calf_2 = BreedingCalf("2023-11-18", Gender.from_str("m"), 12342, True)
        calf_3 = BreedingCalf("2023-11-21", Gender.from_str("m"), 12343, True)
        calf_4 = BreedingCalf("2023-11-24", Gender.from_str("m"), 12344, True)
        calf_5 = BreedingCalf("2023-11-27", Gender.from_str("m"), 12345, True)
        calf_6 = BreedingCalf("2024-11-15", Gender.from_str("m"), 12346, True)

        assert calf_1.ringworm_1.expected_date == dt.date(2023, 12, 25)
        assert calf_2.ringworm_1.expected_date == dt.date(2023, 12, 25)
        assert calf_3.ringworm_1.expected_date == dt.date(2023, 12, 27)
        assert calf_4.ringworm_1.expected_date == dt.date(2024, 1, 1)
        assert calf_5.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_6.ringworm_1.expected_date == dt.date(2024, 12, 23)
        assert calf_1.ringworm_2.expected_date == dt.date(2024, 1, 8)
        assert calf_2.ringworm_2.expected_date == dt.date(2024, 1, 8)
        assert calf_3.ringworm_2.expected_date == dt.date(2024, 1, 10)
        assert calf_4.ringworm_2.expected_date == dt.date(2024, 1, 15)
        assert calf_5.ringworm_2.expected_date == dt.date(2024, 1, 16)
        assert calf_6.ringworm_2.expected_date == dt.date(2025, 1, 6)

        farm.add_calf(calf_1)
        calf_1 = farm.get_calf(12341)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None

        farm.add_calf(calf_2)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None
        assert calf_2.ringworm_1 is None
        assert calf_2.ringworm_2 is None

        farm.add_calf(calf_3)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        calf_3 = farm.get_calf(12343)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None
        assert calf_2.ringworm_1 is None
        assert calf_2.ringworm_2 is None
        assert calf_3.ringworm_1 is None
        assert calf_3.ringworm_2 is None

        farm.add_calf(calf_4)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        calf_3 = farm.get_calf(12343)
        calf_4 = farm.get_calf(12344)
        assert calf_1.ringworm_1 is None
        assert calf_1.ringworm_2 is None
        assert calf_2.ringworm_1 is None
        assert calf_2.ringworm_2 is None
        assert calf_3.ringworm_1 is None
        assert calf_3.ringworm_2 is None
        assert calf_4.ringworm_1 is None
        assert calf_4.ringworm_2 is None

        farm.add_calf(calf_5)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        calf_3 = farm.get_calf(12343)
        calf_4 = farm.get_calf(12344)
        calf_5 = farm.get_calf(12345)
        assert calf_1.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_2.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_3.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_4.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_5.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_1.ringworm_2.expected_date == dt.date(2024, 1, 16)
        assert calf_2.ringworm_2.expected_date == dt.date(2024, 1, 16)
        assert calf_3.ringworm_2.expected_date == dt.date(2024, 1, 16)
        assert calf_4.ringworm_2.expected_date == dt.date(2024, 1, 16)
        assert calf_5.ringworm_2.expected_date == dt.date(2024, 1, 16)

        farm.add_calf(calf_6)
        calf_1 = farm.get_calf(12341)
        calf_2 = farm.get_calf(12342)
        calf_3 = farm.get_calf(12343)
        calf_4 = farm.get_calf(12344)
        calf_5 = farm.get_calf(12345)
        calf_6 = farm.get_calf(12346)
        assert calf_1.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_2.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_3.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_4.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_5.ringworm_1.expected_date == dt.date(2024, 1, 2)
        assert calf_1.ringworm_2.expected_date == dt.date(2024, 1, 16)
        assert calf_2.ringworm_2.expected_date == dt.date(2024, 1, 16)
        assert calf_3.ringworm_2.expected_date == dt.date(2024, 1, 16)
        assert calf_4.ringworm_2.expected_date == dt.date(2024, 1, 16)
        assert calf_5.ringworm_2.expected_date == dt.date(2024, 1, 16)
        assert calf_6.ringworm_1 is None
        assert calf_6.ringworm_2 is None

    def test_get_jobs_in_week(self):
        farm = Farm()
        calf_1 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12341, True)
        calf_2 = BreedingCalf("2023-11-18", Gender.from_str("m"), 12342, True)
        calf_3 = BreedingCalf("2023-11-21", Gender.from_str("m"), 12343, True)
        calf_4 = BreedingCalf("2023-11-24", Gender.from_str("m"), 12344, True)
        calf_5 = BreedingCalf("2023-11-27", Gender.from_str("m"), 12345, True)

        farm.add_calves([calf_1, calf_2, calf_3, calf_4, calf_5])

        jobs = farm.get_jobs_in_week(46)
        assert len(jobs) == 0

        jobs = farm.get_jobs_in_week(47)
        assert len(jobs) == 0

        jobs = farm.get_jobs_in_week(48)
        assert len(jobs) == 3
        assert jobs[0][0] == 12341
        assert jobs[0][1] == "Bovalto1"
        assert jobs[0][2] == dt.date(2023, 11, 27)
        assert jobs[1][0] == 12342
        assert jobs[1][1] == "Bovalto1"
        assert jobs[1][2] == dt.date(2023, 11, 28)
        assert jobs[2][0] == 12343
        assert jobs[2][1] == "Bovalto1"
        assert jobs[2][2] == dt.date(2023, 12, 1)

        jobs = farm.get_jobs_in_week(49)
        assert len(jobs) == 5
        assert jobs[0][0] == 12341
        assert jobs[0][1] == "Dehorn"
        assert jobs[0][2] == dt.date(2023, 12, 4)
        assert jobs[1][0] == 12342
        assert jobs[1][1] == "Dehorn"
        assert jobs[1][2] == dt.date(2023, 12, 4)
        assert jobs[2][0] == 12343
        assert jobs[2][1] == "Dehorn"
        assert jobs[2][2] == dt.date(2023, 12, 6)
        assert jobs[3][0] == 12344
        assert jobs[3][1] == "Bovalto1"
        assert jobs[3][2] == dt.date(2023, 12, 4)
        assert jobs[4][0] == 12345
        assert jobs[4][1] == "Bovalto1"
        assert jobs[4][2] == dt.date(2023, 12, 7)

        jobs = farm.get_jobs_in_week(50)
        assert len(jobs) == 5
        assert jobs[0][0] == 12341
        assert jobs[0][1] == "Restall"
        assert jobs[0][2] == dt.date(2023, 12, 11)
        assert jobs[1][0] == 12342
        assert jobs[1][1] == "Restall"
        assert jobs[1][2] == dt.date(2023, 12, 11)
        assert jobs[2][0] == 12343
        assert jobs[2][1] == "Restall"
        assert jobs[2][2] == dt.date(2023, 12, 11)
        assert jobs[3][0] == 12344
        assert jobs[3][1] == "Dehorn"
        assert jobs[3][2] == dt.date(2023, 12, 11)
        assert jobs[4][0] == 12345
        assert jobs[4][1] == "Dehorn"
        assert jobs[4][2] == dt.date(2023, 12, 12)

        jobs = farm.get_jobs_in_week(51)
        assert len(jobs) == 5
        assert jobs[0][0] == 12341
        assert jobs[0][1] == "Bovalto2"
        assert jobs[0][2] == dt.date(2023, 12, 18)
        assert jobs[1][0] == 12342
        assert jobs[1][1] == "Bovalto2"
        assert jobs[1][2] == dt.date(2023, 12, 19)
        assert jobs[2][0] == 12343
        assert jobs[2][1] == "Bovalto2"
        assert jobs[2][2] == dt.date(2023, 12, 22)
        assert jobs[3][0] == 12344
        assert jobs[3][1] == "Restall"
        assert jobs[3][2] == dt.date(2023, 12, 18)
        assert jobs[4][0] == 12345
        assert jobs[4][1] == "Restall"
        assert jobs[4][2] == dt.date(2023, 12, 18)

        jobs = farm.get_jobs_in_week(52)
        assert len(jobs) == 2
        assert jobs[0][0] == 12344
        assert jobs[0][1] == "Bovalto2"
        assert jobs[0][2] == dt.date(2023, 12, 25)
        assert jobs[1][0] == 12345
        assert jobs[1][1] == "Bovalto2"
        assert jobs[1][2] == dt.date(2023, 12, 28)

        jobs = farm.get_jobs_in_week(1)
        assert len(jobs) == 5
        assert jobs[0][0] == 12341
        assert jobs[0][1] == "Ringworm1"
        assert jobs[0][2] == dt.date(2024, 1, 2)
        assert jobs[1][0] == 12342
        assert jobs[1][1] == "Ringworm1"
        assert jobs[1][2] == dt.date(2024, 1, 2)
        assert jobs[2][0] == 12343
        assert jobs[2][1] == "Ringworm1"
        assert jobs[2][2] == dt.date(2024, 1, 2)
        assert jobs[3][0] == 12344
        assert jobs[3][1] == "Ringworm1"
        assert jobs[3][2] == dt.date(2024, 1, 2)
        assert jobs[4][0] == 12345
        assert jobs[4][1] == "Ringworm1"
        assert jobs[4][2] == dt.date(2024, 1, 2)

        jobs = farm.get_jobs_in_week(2)
        assert len(jobs) == 0

        jobs = farm.get_jobs_in_week(3)
        assert len(jobs) == 5
        assert jobs[0][0] == 12341
        assert jobs[0][1] == "Ringworm2"
        assert jobs[0][2] == dt.date(2024, 1, 16)
        assert jobs[1][0] == 12342
        assert jobs[1][1] == "Ringworm2"
        assert jobs[1][2] == dt.date(2024, 1, 16)
        assert jobs[2][0] == 12343
        assert jobs[2][1] == "Ringworm2"
        assert jobs[2][2] == dt.date(2024, 1, 16)
        assert jobs[3][0] == 12344
        assert jobs[3][1] == "Ringworm2"
        assert jobs[3][2] == dt.date(2024, 1, 16)
        assert jobs[4][0] == 12345
        assert jobs[4][1] == "Ringworm2"
        assert jobs[4][2] == dt.date(2024, 1, 16)

        jobs = farm.get_jobs_in_week(4)
        assert len(jobs) == 0

    def test_farm_delete_calf(self):
        farm = Farm()
        calf_1 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12341, True)
        calf_2 = BreedingCalf("2023-11-18", Gender.from_str("m"), 12342, True)
        calf_3 = BreedingCalf("2023-11-21", Gender.from_str("m"), 12343, True)
        calf_4 = BreedingCalf("2023-11-24", Gender.from_str("m"), 12344, True)
        calf_5 = BreedingCalf("2023-11-27", Gender.from_str("m"), 12345, True)

        farm.add_calves([calf_1, calf_2, calf_3, calf_4, calf_5])

        calf = farm.get_calf(12341)
        assert calf.ringworm_1.expected_date == dt.date(2024, 1, 2)

        farm.delete_calf(12345)
        with pytest.raises(Exception) as exc_info:
            calf = farm.get_calf(12345)

        assert str(exc_info.value) == "Breeding calf with ear tag 12345 not found"

        calf = farm.get_calf(12341)
        assert calf.ringworm_1 is None

    def test_farm_edit_calf(self):
        farm = Farm()
        calf_1 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12341, True)
        calf_2 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12342, True)
        calf_3 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12343, True)
        calf_4 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12344, True)
        calf_5 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12345, True)

        farm.add_calves([calf_1, calf_2, calf_3, calf_4, calf_5])

        calf = farm.get_calf(12341)
        assert calf.ringworm_1.expected_date == dt.date(2023, 12, 25)

        farm.edit_calf(
            12341,
            Birth,
            dt.date(2023, 11, 27),
            dehorning_required=calf.dehorning_required,
        )
        calf = farm.get_calf(12341)
        assert calf.birth.actual_date == dt.date(2023, 11, 27)
        assert calf.ringworm_1.expected_date == dt.date(2024, 1, 2)

    def test_farm_edit_calf_dehorning(self):
        farm = Farm()
        calf_1 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12341, True)
        calf_2 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12342, False)
        calf_3 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12343, True)
        calf_4 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12344, False)
        calf_5 = BreedingCalf("2023-11-15", Gender.from_str("m"), 12345, False)

        farm.add_calves([calf_1, calf_2, calf_3, calf_4, calf_5])

        calf = farm.get_calf(12341)
        assert calf.dehorning_required is True
        assert calf.dehorn.expected_date == dt.date(2023, 12, 4)

        calf = farm.get_calf(12342)
        assert calf.dehorning_required is False
        assert calf.dehorn is None

        # Just update the date
        farm.edit_calf(12341, Dehorn, dt.date(2023, 12, 7), True)
        calf = farm.get_calf(12341)
        assert calf.dehorning_required is True
        assert calf.dehorn.expected_date == dt.date(2023, 12, 4)
        assert calf.dehorn.actual_date == dt.date(2023, 12, 7)
        assert calf.restall.expected_date == dt.date(2023, 12, 12)

        # Do nothing (probably a mistake by the user)
        farm.edit_calf(12342, Dehorn, dt.date(2023, 12, 5), False)
        calf = farm.get_calf(12342)
        assert calf.dehorning_required is False
        assert calf.dehorn is None

        # Remove dehorning
        farm.edit_calf(12343, Dehorn, dt.date(2023, 12, 5), False)
        calf = farm.get_calf(12343)
        assert calf.dehorning_required is False
        assert calf.dehorn is None
        assert calf.restall.expected_date == dt.date(2023, 12, 4)

        # Create a new dehorning
        farm.edit_calf(12344, Dehorn, dt.date(2023, 12, 4), True)
        calf = farm.get_calf(12344)
        assert calf.dehorning_required is True
        assert calf.dehorn.expected_date == dt.date(2023, 12, 4)
        assert calf.dehorn.actual_date is None
        assert calf.restall.expected_date == dt.date(2023, 12, 11)

        # Create a new dehorning and update the date
        farm.edit_calf(12345, Dehorn, dt.date(2023, 12, 5), True)
        calf = farm.get_calf(12345)
        assert calf.dehorning_required is True
        assert calf.dehorn.expected_date == dt.date(2023, 12, 4)
        assert calf.dehorn.actual_date == dt.date(2023, 12, 5)
        assert calf.restall.expected_date == dt.date(2023, 12, 11)
