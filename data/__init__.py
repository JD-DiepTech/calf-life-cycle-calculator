"""
This file is used to import the data from a csv/xslx file to the actual sqlite database.
"""
import os
import sys

# This code snippet does the following:
#     1. It adjusts the Python path to include the parent directory
#        (which contains models and other packages).
#        This allows Python to locate and import modules from these directories.
#     2. Then, it imports the necessary modules from the models package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from models.calf import FatteningCalf, BreedingCalf
from models.gender import Gender
from models.farm import Farm
from db_handler import DatabaseHandler


def get_data(path: str) -> pd.DataFrame:
    if path.endswith(".xlsx"):
        calf_data = pd.read_excel(
            io=path,
            engine="openpyxl",
            sheet_name="Kaelberliste",
            skiprows=1,
            usecols="B:D",
            nrows=40,
        )

        return calf_data


def main():
    calf_data = get_data("calf_2.xlsx")
    farm = Farm()

    # Go through all rows
    for index, row in calf_data.iterrows():
        ear_tag = row["Ear Tag"]
        birthday = row["Birthdate"]
        gender = Gender.from_str(row["Gender"])

        birthday = pd.to_datetime(birthday)
        birthday = birthday.date()

        # Create a new calf
        if ear_tag > 99000:
            # I assume, that dehorning is required for all calves
            calf = FatteningCalf(birthday, gender, ear_tag, True)
        else:
            calf = BreedingCalf(birthday, gender, ear_tag, True)

        farm.add_calf(calf)

    with DatabaseHandler(db_type="sqlite", db_name="calf_data_test.sqlite") as db:
        db.save_farm(farm)


if __name__ == "__main__":
    main()
