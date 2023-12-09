import os
import sys

# This code snippet does the following:
#     1. It adjusts the Python path to include the parent directory
#        (which contains models and other packages).
#        This allows Python to locate and import modules from these directories.
#     2. Then, it imports the necessary modules from the models package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.db_handler import DatabaseHandler
from models.calf import FatteningCalf, BreedingCalf
from models.farm import Farm
from models.gender import Gender

import streamlit as st
import datetime as dt

DB_PATH = "data/calves.sqlite"
DB_TYPE = "sqlite"
BREDING_STR = "breeding"
FATTENING_STR = "fattening"
DISPLAY_CALF = -1
week = dt.datetime.now().isocalendar().week

CONFIG = {
    "0": st.column_config.DateColumn(
        label="Datum",
        format="DD.MM.YYYY",
        default=dt.date.today(),
        required=True,
    ),
    "1": st.column_config.NumberColumn(
        label="Gewicht",
        required=True,
    ),
}


def save(db_path, db_type, farm):
    with DatabaseHandler(db_name=db_path, db_type=db_type) as dbh:
        dbh.save_farm(farm)


def check_unique_dates(data_list):
    dates = [item[0] for item in data_list]
    unique_dates = set(dates)

    return len(dates) == len(unique_dates)


def check_nonzero_values(data_list):
    for item in data_list:
        if item[1] == 0:
            return False
    return True


def create_sidebar(farm: Farm):
    global week

    expander = st.sidebar.expander("Add Calf")
    expander.write("Add a new calf to the database")
    ear_tag = expander.number_input(
        "Ear Tag", value=max_ear_tag + 1, min_value=0, max_value=99999
    )
    calf_type = expander.selectbox(
        "Typ: ",
        options=[BREDING_STR, FATTENING_STR],
        index=0,  # breeding
    )
    birthdate = expander.date_input(
        "Birthdate", value=dt.date.today(), format="DD.MM.YYYY"
    )
    gender = expander.selectbox(
        "Gender", options=[Gender.Female, Gender.Male], index=0  # w
    )
    dehorning_required = expander.checkbox("Dehorning required", value=True)

    if expander.button("Add"):
        if calf_type == BREDING_STR:
            new_calf = BreedingCalf(birthdate, gender, ear_tag, dehorning_required)
        elif calf_type == FATTENING_STR:
            new_calf = FatteningCalf(birthdate, gender, ear_tag, dehorning_required)
        else:
            raise Exception(f"Unknown calf type: {calf_type}")

        farm.add_calf(new_calf)

        # We have to safe the whole farm incase other calves were changed
        # This happens when we have to set the ringworm
        save(DB_PATH, DB_TYPE, farm)
        st.rerun()

    global DISPLAY_CALF
    DISPLAY_CALF = st.sidebar.selectbox(
        "Select Calf",
        options=sorted(farm.get_ear_tags(), reverse=True),
        index=0,
    )


def main() -> None:
    with DatabaseHandler(db_name=DB_PATH, db_type=DB_TYPE) as dbh:
        weights = dbh.fetch_calf_weights(DISPLAY_CALF)

    if weights is None or len(weights) == 0:
        weights = [[dt.date.today(), 0]]

    updated_weights = st.data_editor(
        weights,
        num_rows="dynamic",
        column_config=CONFIG,
        key="st_edited_calf_data",
    )

    # Check that the new data doesn't contain a zero weight
    # If it does, show a warning and don't save the data
    if not check_nonzero_values(updated_weights):
        st.warning("Weight cannot be zero")
        return None

    # Check if there dates doubled in the new data
    # If they do, show a warning and don't save the data
    if not check_unique_dates(updated_weights):
        st.warning("Dates cannot be doubled")
        return None

    if st.button("Save"):
        with DatabaseHandler(db_name=DB_PATH, db_type=DB_TYPE) as dbh:
            dbh.save_calf_weights(DISPLAY_CALF, updated_weights)


if __name__ == "__main__":
    st.set_page_config(page_title="Kälberliste", page_icon="🐮", layout="wide")
    st.title("Weights")

    calves = []

    with DatabaseHandler(db_name=DB_PATH, db_type="sqlite") as dbh:
        calves = dbh.fetch_all_calves()

    farm = Farm()

    # Since the data directly comes from the database,
    # we don't need to set the ringworm
    farm.add_calves(calves, set_ringworm=False)
    max_ear_tag = farm.get_max_breeding_calf_ear_tag()

    create_sidebar(farm)
    main()
