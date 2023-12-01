import os
import sys

# This code snippet does the following:
#     1. It adjusts the Python path to include the parent directory
#        (which contains models and other packages).
#        This allows Python to locate and import modules from these directories.
#     2. Then, it imports the necessary modules from the models package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.calf import FatteningCalf, BreedingCalf
from models.farm import Farm
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
from data.db_handler import DatabaseHandler

import streamlit as st
import datetime as dt


week = dt.datetime.now().isocalendar().week


def create_sidebar():
    global week

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
    create_sidebar()

    st.write("View jobs per week")
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
