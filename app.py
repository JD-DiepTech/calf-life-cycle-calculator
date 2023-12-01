from view.view_jobs_per_week import view_jobs_per_week
from view.view_all_calves import view_all_calves
from data.db_handler import DatabaseHandler
from models.farm import Farm

import pandas as pd
import numpy as np
import streamlit as st
import datetime as dt
import time


DB_PATH = "data/calf_data.sqlite"


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

# -------------- SIDEBAR --------------
st.sidebar.header("Filter")

show_all_calves = st.sidebar.toggle("Show all calves", value=False)


# -------------- MAIN --------------
calves = []

with DatabaseHandler(db_name=DB_PATH) as db:
    calves = db.fetch_all_calves()

farm = Farm()
farm.add_calves(calves)

if show_all_calves:
    new_farm = view_all_calves()
else:
    new_farm = view_jobs_per_week(farm)

if new_farm:
    with DatabaseHandler(db_name=DB_PATH) as db:
        db.save_farm(new_farm)
    st.rerun()
