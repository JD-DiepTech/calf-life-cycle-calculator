from view.view_jobs_per_week import view_jobs_per_week
from view.view_all_calves import view_all_calves
from data.db_handler import DatabaseHandler
from models.farm import Farm
from models.gender import Gender
from models.calf import FatteningCalf, BreedingCalf

import pandas as pd
import numpy as np
import streamlit as st
import datetime as dt
import time


DB_PATH = "data/calves.sqlite"


def fade_out(handler, message, icon):
    # st.toast(message, icon="✅")
    # st.success(message, icon="✅")

    global ok_message, ok_css
    ok_message.empty()
    ok_css.empty()
    ok_css.markdown(
        """
        <style>
            .stAlert {
                opacity: 1;
                anmation: None;
            }
        </style>""",
        unsafe_allow_html=True,
    )
    time.sleep(0.1)
    handler(message, icon=icon)
    ok_css.markdown(
        """
        <style>
            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }
            .stAlert {
                animation-name: fadeOut;
                animation-duration:  5s;
                opacity: 0;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )


st.set_page_config(page_title="Kälberliste", page_icon="🐮", layout="wide")
calves = []

# Issue #1
# This needs to be done only on startup
with DatabaseHandler(db_name=DB_PATH) as db:
    calves = db.fetch_all_calves()

farm = Farm()

# #2: Since the data directly comes from the database
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
        calf = BreedingCalf(birthdate, gender, ear_tag, dehorning_required)
    elif calf_type == "fattening":
        calf = FatteningCalf(birthdate, gender, ear_tag, dehorning_required)
    else:
        raise Exception(f"Unknown calf type: {calf_type}")

    farm.add_calf(calf)

    with DatabaseHandler(db_name=DB_PATH) as db:
        db.save_farm(farm)
    st.rerun()


# -------------- VIEWS --------------
if show_all_calves:
    new_farm = view_all_calves(farm)
else:
    new_farm = view_jobs_per_week(farm)

if new_farm:
    with DatabaseHandler(db_name=DB_PATH) as db:
        db.save_farm(new_farm)
    st.rerun()
