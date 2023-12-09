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

import streamlit as st
import datetime as dt

DB_PATH = "data/calves.sqlite"
DB_TYPE = "sqlite"
BREDING_STR = "breeding"
FATTENING_STR = "fattening"
week = dt.datetime.now().isocalendar().week


def save(db_path, db_type, farm):
    with DatabaseHandler(db_name=db_path, db_type=db_type) as dbh:
        dbh.save_farm(farm)


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

    # Create a list of weeks for the next three weeks
    calendar_week_options = [
        (dt.datetime.now() + dt.timedelta(days=7 * i)).isocalendar().week
        for i in range(4)
    ]

    week = st.sidebar.selectbox(
        "Calender Week",
        options=calendar_week_options,
        index=0,  # Current week
    )


def get_changed_calves(
    old: list[tuple[int, str, dt.date]], new: list[tuple[int, str, dt.date]]
) -> list[tuple[int, str, dt.date]]:
    """
    Returns a list of tuples with the changed calves.
    The tuples contain the ear tag, the treatment and the date.
    """
    changed_calves = []

    for old_calf in old:
        for new_calf in new:
            if old_calf[0] == new_calf[0]:
                if old_calf[2] != new_calf[2]:
                    changed_calves.append(new_calf)

    return changed_calves


def get_treatment(
    treatment: str,
) -> type[
    Birth | Bovalto1 | Dehorn | Restall | Sell | Bovalto2 | Ringworm1 | Ringworm2
]:
    match treatment:
        case "birth":
            return Birth
        case "bovalto1":
            return Bovalto1
        case "dehorn":
            return Dehorn
        case "restall":
            return Restall
        case "sell":
            return Sell
        case "bovalto2":
            return Bovalto2
        case "ringworm1":
            return Ringworm1
        case "ringworm2":
            return Ringworm2
        case _:
            raise Exception("Job not found")


def view_jobs_per_week(farm: Farm) -> Farm | None:
    displayed_data = farm.get_jobs_in_week(week)

    config = {
        "0": st.column_config.NumberColumn("Ohrmarke"),
        "1": st.column_config.TextColumn(label="Aufgabe"),
        "2": st.column_config.DateColumn(label="Datum", format="DD.MM.YYYY"),
    }

    num_rows = len(displayed_data)
    height = (num_rows + 1) * 35 + 3  # 35px per row + 1 header row + 3px for the border
    width = 400

    # Display the data in a data editor
    # The return value is the updated list (as the input)
    updated_calf_data = st.data_editor(
        displayed_data,
        hide_index=True,
        width=width,
        height=height,
        use_container_width=False,
        column_config=config,
        disabled=["0", "1"],
    )

    updated_list = get_changed_calves(displayed_data, updated_calf_data)

    if len(updated_list) > 0:
        if st.button("Submit"):
            for ear_tag, treatment, date in updated_list:
                calf = farm.get_calf(ear_tag)

                farm.edit_calf(
                    ear_tag,
                    get_treatment(treatment.lower()),
                    date,
                    calf.dehorning_required,
                )

                return farm

    return None


if __name__ == "__main__":
    st.set_page_config(page_title="Kälberliste", page_icon="🐮", layout="wide")
    st.title("Jobs This Week")

    calves = []

    with DatabaseHandler(db_name=DB_PATH, db_type="sqlite") as dbh:
        calves = dbh.fetch_all_calves()

    farm = Farm()

    # Since the data directly comes from the database,
    # we don't need to set the ringworm
    farm.add_calves(calves, set_ringworm=False)
    max_ear_tag = farm.get_max_breeding_calf_ear_tag()

    create_sidebar(farm)
    new_farm = view_jobs_per_week(farm)

    if new_farm is not None:
        save(DB_PATH, DB_TYPE, new_farm)
        st.rerun()
