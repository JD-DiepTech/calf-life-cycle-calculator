from models.gender import Gender
import pytest
import sys
import os

# This code snippet does the following:
#     1. It adjusts the Python path to include the parent directory
#        (which contains models and other packages).
#        This allows Python to locate and import modules from these directories.
#     2. Then, it imports the necessary modules from the models package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestGender:
    def test_gender_creation(self):
        male = Gender.Male
        female = Gender.Female

        assert male == Gender.Male
        assert female == Gender.Female

    def test_gender_creation_from_string(self):
        male = Gender.from_str("m")
        female = Gender.from_str("w")

        assert male == Gender.Male
        assert female == Gender.Female

    def test_gender_str(self):
        male = Gender.from_str("m")
        female = Gender.from_str("w")

        assert str(male) == "m"
        assert str(female) == "w"
