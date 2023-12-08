from view.view_jobs_per_week import view_jobs_per_week
from view.view_all_calves import view_all_calves
from data.db_handler import DatabaseHandler
import data.db_handler as db
from models.farm import Farm
from models.gender import Gender
from models.calf import FatteningCalf, BreedingCalf

import pandas as pd
import numpy as np
import streamlit as st
import datetime as dt
import time


DB_PATH = "data/calves.sqlite"
DB_TYPE = "sqlite"


def save(db_path, db_type, farm):
    with DatabaseHandler(db_name=db_path, db_type=db_type) as dbh:
        dbh.save_farm(farm)


st.set_page_config(page_title="Kälberliste", page_icon="🐮", layout="wide")
calves = []

with DatabaseHandler(db_name=DB_PATH, db_type="sqlite") as dbh:
    calves = dbh.fetch_all_calves()

farm = Farm()

# Since the data directly comes from the database,
# we don't need to set the ringworm
farm.add_calves(calves, set_ringworm=False)
max_ear_tag = farm.get_max_breeding_calf_ear_tag()


# -------------- SIDEBAR --------------
st.sidebar.header("Filter")

show_all_calves = st.sidebar.toggle("Show all calves", value=False)

expander = st.sidebar.expander("Add Calf")
expander.write("Add a new calf to the database")
ear_tag = expander.number_input(
    "Ear Tag", value=max_ear_tag + 1, min_value=0, max_value=99999
)
calf_type = expander.selectbox(
    "Typ: ", options=["breeding", "fattening"], index=0  # breeding
)
birthdate = expander.date_input("Birthdate", value=dt.date.today(), format="DD.MM.YYYY")
gender = expander.selectbox(
    "Gender", options=[Gender.Female, Gender.Male], index=0
)  # w
dehorning_required = expander.checkbox("Dehorning required", value=True)

if expander.button("Add"):
    if calf_type == "breeding":
        new_calf = BreedingCalf(birthdate, gender, ear_tag, dehorning_required)
    elif calf_type == "fattening":
        new_calf = FatteningCalf(birthdate, gender, ear_tag, dehorning_required)
    else:
        raise Exception(f"Unknown calf type: {calf_type}")

    farm.add_calf(new_calf)

    # We have to safe the whole farm incase other calves were changed
    # This happens when we have to set the ringworm
    save(DB_PATH, DB_TYPE, farm)
    st.rerun()


# -------------- VIEWS --------------
if show_all_calves:
    new_farm, delete_calves = view_all_calves(farm)

    if new_farm:
        db.delete(DB_PATH)
        save(DB_PATH, DB_TYPE, farm)
        st.rerun()


else:
    new_farm = view_jobs_per_week(farm)

    if new_farm:
        save(DB_PATH, DB_TYPE, farm)
        st.rerun()
