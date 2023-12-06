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

sort_by = "Birthdate"
ascending = True


def create_sidebar():
    global sort_by, ascending

    # Sort by selector
    sort_by = st.sidebar.selectbox(
        "Sort by",
        options=["Ear Tag", "Birthdate"],
        index=1,  # Birthdate
    )

    ascending = st.sidebar.toggle("Ascending Order", value=False)


def view_all_calves(farm: Farm) -> Farm | None:
    create_sidebar()

    st.write("View all calves")
    # displayed_data = calf_data.sort_values(by=sort_by, ascending=ascending)
    #
    # # Convert columns to datetime format
    # for column in displayed_data.columns:
    #     if column == "Ear Tag" or column == "Gender" or column == "dehorning_required":
    #         continue
    #
    #     displayed_data[column] = pd.to_datetime(displayed_data[column])
    #
    # # Find the max ear tag number for breeding calves
    # max_breeding_ear_tag = displayed_data.loc[
    #     displayed_data["Ear Tag"] < 99000, "Ear Tag"
    # ].max()
    #
    # config = {
    #     "Ear Tag": st.column_config.NumberColumn(
    #         label="Ohrmarke",
    #         default=int(max_breeding_ear_tag) + 1,
    #         required=True,
    #     ),
    #     "Birthdate": st.column_config.DateColumn(
    #         label="Geburtsdatum",
    #         format="DD.MM.YYYY",
    #         default=dt.date.today(),
    #         required=True,
    #     ),
    #     "Gender": st.column_config.SelectboxColumn(
    #         label="Geschlecht",
    #         options=["w", "m"],
    #         default="w",
    #         required=True,
    #     ),
    #     "dehorning_required": st.column_config.CheckboxColumn(
    #         label="Enthornung benötigt",
    #         default=True,
    #         required=True,
    #     ),
    #     "Bovalto1": st.column_config.DateColumn(
    #         label="Bovalto 1",
    #         format="DD.MM.YYYY",
    #     ),
    #     "Dehorn": st.column_config.DateColumn(label="Enthornung", format="DD.MM.YYYY"),
    #     "Restall": st.column_config.DateColumn(label="Umstallen", format="DD.MM.YYYY"),
    #     "Sell": st.column_config.DateColumn(label="Verkaufsdatum", format="DD.MM.YYYY"),
    #     "Bovalto2": st.column_config.DateColumn(label="Bovalto 2", format="DD.MM.YYYY"),
    #     "Ringworm1": st.column_config.DateColumn(
    #         label="Flechte 1", format="DD.MM.YYYY"
    #     ),
    #     "Ringworm2": st.column_config.DateColumn(
    #         label="Flechte 2", format="DD.MM.YYYY"
    #     ),
    # }
    #
    # numRows = len(displayed_data.index)
    # height = (
    #     numRows + 2
    # ) * 35 + 3  # 35px per row + 1 header row + 1 "Add"-Row + 3px for the border
    # width = 400
    #
    # updated_calf_data = st.data_editor(
    #     displayed_data,
    #     hide_index=True,
    #     width=width,
    #     height=height,
    #     use_container_width=show_all_calves,
    #     num_rows="dynamic",
    #     column_config=config,
    #     key="st_edited_calf_data",
    # )
    #
    # # Debug changes
    # st.write(st.session_state["st_edited_calf_data"])
    #
    # clean_data = True
    # added_calves = False
    # edited_calves = False
    # deleted_calves = False
    #
    # # Check that the ear tag number is unique
    # if not updated_calf_data["Ear Tag"].is_unique:
    #     st.warning("Ear tag number must be unique")
    #     clean_data = False
    #
    # # Check that if dehorning is required, the dehorning date is set
    # # new_ear_tags = [
    # #     d["Ear Tag"] for d in st.session_state["st_edited_calf_data"]["added_rows"]
    # # ]
    # # if (
    # #     not updated_calf_data.loc[
    # #         updated_calf_data["dehorning_required"] == True, "Dehorn"
    # #     ]
    # #     .notnull()
    # #     .all()
    # # ):
    # #     st.warning("Dehorning date must be set if dehorning is required")
    # #     clean_data = False
    #
    # # Check for new calves
    # if len(st.session_state["st_edited_calf_data"]["added_rows"]) > 0:
    #     added_calves = True
    #
    # # Check for changes in existing calves
    # if len(st.session_state["st_edited_calf_data"]["edited_rows"]) > 0:
    #     # A calf has been edited
    #     edited_calves = True
    #
    # # Check for deleted calves
    # if len(st.session_state["st_edited_calf_data"]["deleted_rows"]) > 0:
    #     deleted_calves = True
    #
    # if clean_data and (added_calves or edited_calves or deleted_calves):
    #     if st.button("Submit"):
    #         if added_calves:
    #             calf_data = cd.bulk_add_calf(
    #                 calf_data, st.session_state["st_edited_calf_data"]["added_rows"]
    #             )
    #
    #         if edited_calves:
    #             calf_data.sort_values(by=sort_by, ascending=ascending, inplace=True)
    #             for row in st.session_state["st_edited_calf_data"]["edited_rows"]:
    #                 print(row)
    #
    #                 ear_tag = calf_data.iloc[row]["Ear Tag"]
    #                 edited_cells = st.session_state["st_edited_calf_data"][
    #                     "edited_rows"
    #                 ][row]
    #                 print(f"Edit calf: {ear_tag} - {edited_cells}")
    #
    #                 calf_data = cd.edit_calf(calf_data, ear_tag, edited_cells)
    #
    #         if deleted_calves:
    #             ear_tags = []
    #             calf_data.sort_values(by=sort_by, ascending=ascending, inplace=True)
    #             for row in st.session_state["st_edited_calf_data"]["deleted_rows"]:
    #                 ear_tag = calf_data.iloc[row]["Ear Tag"]
    #                 ear_tags.append(ear_tag)
    #
    #             calf_data = cd.bulk_delete_calf(calf_data, ear_tags)
    #
    #         cd.save(
    #             calf_data=calf_data,
    #             db_path=DB_PATH,
    #         )
    #         st.rerun()
