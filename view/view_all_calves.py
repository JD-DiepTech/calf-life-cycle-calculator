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
from data.db_handler import DatabaseHandler

import streamlit as st
import datetime as dt

COLUMN_TO_TREATMENT = {
    "0": None,  # Delete
    "1": None,  # Ear Tag
    "2": None,  # "breeding" or "fattening"
    "3": Birth,
    "4": Gender,
    "5": None,  # Dehorning required
    "6": Bovalto1,
    "7": Dehorn,
    "8": Restall,
    "9": Sell,
    "10": Bovalto2,
    "11": Ringworm1,
    "12": Ringworm2,
}

CONFIG = {
    "0": st.column_config.CheckboxColumn(
        label="Löschen?",
        default=False,
        required=True,
    ),
    "1": st.column_config.NumberColumn(
        label="Ohrmarke",
        default=int(5) + 1,
        required=True,
    ),
    "2": st.column_config.SelectboxColumn(
        label="Typ",
        options=["breeding", "fattening"],
        default="breeding",
        required=True,
    ),
    "3": st.column_config.DateColumn(
        label="Geburtsdatum",
        format="DD.MM.YYYY",
        default=dt.date.today(),
        required=True,
    ),
    "4": st.column_config.SelectboxColumn(
        label="Geschlecht",
        options=["w", "m"],
        default="w",
        required=True,
    ),
    "5": st.column_config.CheckboxColumn(
        label="Enthornung benötigt",
        default=True,
        required=True,
    ),
    "6": st.column_config.DateColumn(
        label="Bovalto 1",
        format="DD.MM.YYYY",
        required=True,
    ),
    "7": st.column_config.DateColumn(label="Enthornung", format="DD.MM.YYYY"),
    "8": st.column_config.DateColumn(
        label="Umstallen", format="DD.MM.YYYY", required=True
    ),
    "9": st.column_config.DateColumn(label="Verkaufsdatum", format="DD.MM.YYYY"),
    "10": st.column_config.DateColumn(label="Bovalto 2", format="DD.MM.YYYY"),
    "11": st.column_config.DateColumn(label="Flechte 1", format="DD.MM.YYYY"),
    "12": st.column_config.DateColumn(label="Flechte 2", format="DD.MM.YYYY"),
}

sort_by = "Birthdate"
ascending = True


def create_sidebar(farm: Farm):
    # global sort_by, ascending
    #
    # # Sort by selector
    # sort_by = st.sidebar.selectbox(
    #     "Sort by",
    #     options=["Ear Tag", "Birthdate"],
    #     index=1,  # Birthdate
    # )
    #
    # ascending = st.sidebar.toggle("Ascending Order", value=False)
    pass


def view_all_calves(farm: Farm) -> Farm | None:
    create_sidebar(farm)

    st.write("View all calves")

    displayed_calves = farm.get_calves_as_tuple()

    # Create a column to select and then delete calves
    displayed_data = [(False,) + calf_data for calf_data in displayed_calves]

    num_rows = len(displayed_data)
    height = (
        num_rows + 1
    ) * 35 + 10  # 35px per row + 1 header row + 3px for the border

    updated_calf_data = st.data_editor(
        displayed_data,
        hide_index=True,
        height=height,
        use_container_width=True,
        # num_rows="dynamic",
        column_config=CONFIG,
        key="st_edited_calf_data",
    )

    # Debug changes
    st.write(st.session_state["st_edited_calf_data"])

    st_edited_rows = st.session_state["st_edited_calf_data"]["edited_rows"]
    print(f"st_edited_rows: {st_edited_rows}")
    delete_rows = []
    edited_rows = []

    # Check for changes in existing calves
    if len(st_edited_rows) > 0:
        # Check if the first column has been edited to True (that calf shall be deleted)
        # Example: {29: {'0': False, '5': False}, 30: {'0': True, '5': False}, 31: {'0': True}, 32: {'0': False, '5': True}}
        # It is possible that multiple calves have been edited to be deleted
        # It is also possible that it has been edited and then edited back to False (i.e. calf 32 (the value before for "5" was also True))
        # It is also possible that it has been edited and marked as deleted (i.e. calf 30 and 31)

        for row_number, edited_values in st_edited_rows.items():
            # Check if the first column has been edited to True (that calf shall be deleted)
            if "0" in edited_values and edited_values["0"] is True:
                delete_rows.append(row_number)
            elif "0" not in edited_values or (
                "0" in edited_values
                and edited_values["0"] is False
                and len(edited_values) > 1
            ):
                # The first column has not been edited
                # OR, the first column has been edited and is false
                #     AND, there are other columns that have been edited
                # It needs to be double checked, if that edited value was set to value we had before
                # If it is, then it is not an edit, and we can ignore it
                # If it is not, then it is an edit, and we need to add it to the edited_rows list
                for column, edited_value in edited_values.items():
                    if column == "0":
                        continue

                    # Check if the edited value is the same as the value we had before
                    # If it is, then it is not an edit, and we can ignore it
                    # If it is not, then it is an edit, and we need to add it to the edited_rows list
                    # We have to convert both values to strings, because bools will be treated as bools
                    #  while DateTime objects will be treated as strings
                    if str(edited_value) == str(
                        displayed_data[row_number][int(column)]
                    ):
                        continue
                    edited_rows.append(row_number)

    print(f"delete_rows: {delete_rows}")
    print(f"edited_rows: {edited_rows}")

    if len(delete_rows) > 0 or len(edited_rows) > 0:
        if st.button("Submit"):
            delete_ear_tags = []
            edited_eartags = []

            if len(delete_rows) > 0:
                for row in delete_rows:
                    ear_tag = displayed_data[row][1]
                    delete_ear_tags.append(ear_tag)

                print(f"Delete calves: {delete_ear_tags}")
                farm.delete_calves(delete_ear_tags)

            if len(edited_rows) > 0:
                for row in edited_rows:
                    ear_tag = displayed_data[row][1]

                    edited_cells = st_edited_rows[row].copy()

                    # There might be a case where the user edits a cell, and then edits it back to the original value
                    # While he also edited another cell
                    for key, value in st_edited_rows[row].items():
                        if str(value) == str(displayed_data[row][int(key)]):
                            del edited_cells[key]

                    if "0" in edited_cells:
                        del edited_cells["0"]

                    print(f"Edit calf: {ear_tag} - {edited_cells}")
                    for key, value in edited_cells.items():
                        calf = farm.get_calf(ear_tag)
                        print(f"Edit calf: {ear_tag} - {key} - {value}")

                        # TODO: Check if I can use a match statement here
                        #       It might be a problem that we need to edit the calf in a certain order
                        if key == "2":
                            # Calf type changed
                            # We need to delete the calf and add it again with the new type
                            # This needs to be done first, because we need to retrieve the old calf
                            print(f"Delete calf: {farm.get_calf(ear_tag)}")
                            # Before we delete the calf, we need to retrieve all available treatments
                            farm.delete_calf(ear_tag, set_ringworm=False)
                            if value == "breeding":
                                new_calf = BreedingCalf(
                                    displayed_data[row][3],
                                    displayed_data[row][4],
                                    ear_tag,
                                    displayed_data[row][5],
                                )

                            elif value == "fattening":
                                new_calf = FatteningCalf(
                                    displayed_data[row][3],
                                    displayed_data[row][4],
                                    ear_tag,
                                    displayed_data[row][5],
                                )

                            else:
                                raise Exception(f"Unknown calf type: {value}")

                            new_calf.birth = calf.birth
                            new_calf.bovalto_1 = calf.bovalto_1
                            new_calf.dehorn = calf.dehorn
                            new_calf.restall = calf.restall

                            print(f"Add calf: {new_calf}")
                            farm.add_calf(new_calf)

                        elif key == "1":
                            # Ear tag changes
                            calf.change_ear_tag(value)

                        elif key == "3":
                            date = dt.datetime.strptime(value, "%Y-%m-%d").date()
                            calf.edit_birth(date)
                        elif key == "4":
                            calf.edit_gender(Gender.from_string(value))
                        elif key == "5":
                            calf.reset_dehorn(displayed_data[row][7], value)
                        elif key == "6":
                            date = dt.datetime.strptime(value, "%Y-%m-%d").date()
                            calf.edit_bovalto1(date)
                        elif key == "7":
                            if value is not None:
                                date = dt.datetime.strptime(value, "%Y-%m-%d").date()
                                calf.edit_dehorn(date)
                            else:
                                calf.delete_dehorn()
                        elif key == "8":
                            if value is not None:
                                date = dt.datetime.strptime(value, "%Y-%m-%d").date()
                                calf.edit_restall(date)
                            else:
                                st.error("Umstallen muss gesetzt werden")
                        elif key == "9":
                            if calf.calf_type == "fattening":
                                if value is not None:
                                    date = dt.datetime.strptime(
                                        value, "%Y-%m-%d"
                                    ).date()
                                    calf.edit_sell(date)
                                else:
                                    st.error("Verkaufsdatum muss gesetzt werden")
                            else:
                                # Do nothing
                                # A breeding calf cannot be sold
                                continue
                        elif key == "10":
                            if calf.calf_type == "breeding":
                                if value is not None:
                                    date = dt.datetime.strptime(
                                        value, "%Y-%m-%d"
                                    ).date()
                                    calf.edit_bovalto2(date)
                                else:
                                    st.error("Bovalto 2 muss gesetzt werden")
                            else:
                                # Do nothing
                                # A fattening calf does not have a second bovalto
                                continue
                        elif key == "11":
                            if calf.calf_type == "breeding":
                                if value is not None:
                                    date = dt.datetime.strptime(
                                        value, "%Y-%m-%d"
                                    ).date()
                                    calf.edit_ringworm1(date)
                                else:
                                    calf.delete_ringworm1()
                            else:
                                # Do nothing
                                # A fattening calf does not have a ringworm
                                continue
                        elif key == "12":
                            if calf.calf_type == "breeding":
                                if value is not None:
                                    date = dt.datetime.strptime(
                                        value, "%Y-%m-%d"
                                    ).date()
                                    calf.edit_ringworm2(date)
                                else:
                                    calf.delete_ringworm2()
                            else:
                                # Do nothing
                                # A fattening calf does not have a ringworm
                                continue

                        print(f"Edited calf: {calf}")

            print(f"New farm: {farm}")
            return (
                farm,
                None if len(delete_ear_tags) == 0 else delete_ear_tags,
            )

    return (None, None)

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
    #
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
