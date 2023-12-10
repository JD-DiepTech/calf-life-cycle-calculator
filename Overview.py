from data.db_handler import DatabaseHandler
import data.db_handler as db
from models.farm import Farm
from models.gender import Gender
from models.calf import FatteningCalf, BreedingCalf

import streamlit as st
import datetime as dt


DB_PATH = "data/calves.sqlite"
DB_TYPE = "sqlite"
BREEDING_STR = "breeding"
FATTENING_STR = "fattening"
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


def save(db_path, db_type, farm):
    with DatabaseHandler(db_name=db_path, db_type=db_type) as dbh:
        dbh.save_farm(farm)


# -------------- SIDEBAR --------------
def create_sidebar(farm):
    st.sidebar.header("Filter")

    expander = st.sidebar.expander("Add Calf")
    expander.write("Add a new calf to the database")
    ear_tag = expander.number_input(
        "Ear Tag", value=max_ear_tag + 1, min_value=0, max_value=99999
    )
    calf_type = expander.selectbox(
        "Typ: ",
        options=[BREEDING_STR, FATTENING_STR],
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
        if calf_type == BREEDING_STR:
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


def main(farm: Farm) -> Farm:
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
    # st.write(st.session_state["st_edited_calf_data"])

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
            return farm

    return None


if __name__ == "__main__":
    st.set_page_config(page_title="Kälberliste", page_icon="🐮", layout="wide")
    st.title("All Calves")

    calves = []

    with DatabaseHandler(db_name=DB_PATH, db_type="sqlite") as dbh:
        calves = dbh.fetch_all_calves()

    farm = Farm()

    # Since the data directly comes from the database,
    # we don't need to set the ringworm
    farm.add_calves(calves, set_ringworm=False)
    max_ear_tag = farm.get_max_breeding_calf_ear_tag()

    create_sidebar(farm)
    new_farm = main(farm)

    if new_farm is not None:
        db.delete(DB_PATH)
        save(DB_PATH, DB_TYPE, new_farm)
        st.rerun()
