from data.db_handler import DatabaseHandler, database_creation_script
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
from models.calf import FatteningCalf, BreedingCalf
import datetime as dt
import pytest
import sys
import os
import sqlite3

# This code snippet does the following:
#     1. It adjusts the Python path to include the parent directory
#        (which contains models and other packages).
#        This allows Python to locate and import modules from these directories.
#     2. Then, it imports the necessary modules from the models package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Fixture to create an in-memory SQLite database for testing
@pytest.fixture(scope="module")
def test_db():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()

    # Create a table for testing
    cursor.execute(database_creation_script)
    connection.commit()
    yield connection  # Provide the fixture value
    connection.close()


class TestDatabaseHandler:
    def test_database_handler_creation(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            assert db_handler is not None
            assert db_handler.db_name == "memory.db"
            assert db_handler.db_type == "memory"
            assert db_handler.connection is not None
            assert db_handler.cursor is not None


class TestDatabaseHandlerCreateEntries:
    # Test creating an entry
    def test_insert_calf(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_calf_data(12345, Gender.Female, "breeding")

    def test_insert_birth_without_actual(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_birth_data(12345, dt.date(2021, 1, 1))

    def test_insert_birth_with_actual(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_birth_data(
                12345, dt.date(2021, 1, 1), dt.date(2021, 1, 2)
            )

    def test_insert_bovalto1_without_actual(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_bovalto1_data(12345, dt.date(2021, 1, 1))

    def test_insert_bovalto1_with_actual(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_bovalto1_data(
                12345, dt.date(2021, 1, 1), dt.date(2021, 1, 2)
            )

    def test_insert_dehorn_without_actual(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_dehorn_data(12345, dt.date(2021, 1, 1))

    def test_insert_dehorn_with_actual(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_dehorn_data(
                12345, dt.date(2021, 1, 1), dt.date(2021, 1, 2)
            )

    def test_insert_restall_without_actual(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_restall_data(12345, dt.date(2021, 1, 1))

    def test_insert_restall_with_actual(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_restall_data(
                12345, dt.date(2021, 1, 1), dt.date(2021, 1, 2)
            )

    def test_insert_bovalto2_without_actual(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_bovalto2_data(12345, dt.date(2021, 1, 1))

    def test_insert_bovalto2_with_actual(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_bovalto2_data(
                12345, dt.date(2021, 1, 1), dt.date(2021, 1, 2)
            )

    def test_insert_ringworm1_without_actual(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_ringworm1_data(12345, dt.date(2021, 1, 1))

    def test_insert_ringworm1_with_actual(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_ringworm1_data(
                12345, dt.date(2021, 1, 1), dt.date(2021, 1, 2)
            )

    def test_insert_ringworm2_without_actual(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_ringworm2_data(12345, dt.date(2021, 1, 1))

    def test_insert_ringworm2_with_actual(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_ringworm2_data(
                12345, dt.date(2021, 1, 1), dt.date(2021, 1, 2)
            )


class TestDatabaseHandlerReadEntries:
    # Test reading an entry
    def test_read_calf(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_calf_data(12345, Gender.Female, "breeding")

            retrieved_entry = db_handler.fetch_calf_data(12345)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, gender, calf_type = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag == 12345
            assert gender == Gender.Female
            assert calf_type == "breeding"

    def test_read_all_calves(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_calf_data(12341, Gender.Female, "breeding")
            db_handler.insert_calf_data(12342, Gender.Female, "breeding")
            db_handler.insert_calf_data(12343, Gender.Female, "breeding")

            retrieved_entry = db_handler.fetch_calf_data()
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 3
            i = 0
            for entry in retrieved_entry:
                assert entry is not None
                assert len(entry) == 3

                ear_tag, gender, calf_type = entry
                assert retrieved_entry is not None
                assert ear_tag == 12341 + i
                assert gender == Gender.Female
                assert calf_type == "breeding"

                i += 1

    def test_read_non_existent_calf(self):
        with DatabaseHandler(db_name="memory.db", db_type="memory") as db_handler:
            db_handler.insert_calf_data(12341, Gender.Female, "breeding")

            retrieved_entry = db_handler.fetch_calf_data(12340)
            assert len(retrieved_entry) == 0
            assert retrieved_entry == []

    def test_read_birth(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            db_handler.insert_birth_data(12345, dt.date(2021, 1, 1))

            retrieved_entry = db_handler.fetch_birth_data(12345)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert ear_tag == 12345
            assert expected_date == dt.date(2021, 1, 1)
            assert actual_date is None

    def test_read_birth_with_actual(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            planned = dt.date(2021, 1, 1)
            actual = dt.date(2021, 1, 2)
            ear_tag_in = 12345
            db_handler.insert_birth_data(ear_tag_in, planned, actual)

            retrieved_entry = db_handler.fetch_birth_data(12345)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag == ear_tag_in
            assert expected_date == planned
            assert actual_date == actual

    def test_read_bovalto1(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            db_handler.insert_bovalto1_data(12345, dt.date(2021, 1, 1))

            retrieved_entry = db_handler.fetch_bovalto1_data(12345)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag == 12345
            assert expected_date == dt.date(2021, 1, 1)
            assert actual_date is None

    def test_read_dehorn(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            db_handler.insert_dehorn_data(12345, dt.date(2021, 1, 1))

            retrieved_entry = db_handler.fetch_dehorn_data(12345)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag == 12345
            assert expected_date == dt.date(2021, 1, 1)
            assert actual_date is None

    def test_read_restall(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            db_handler.insert_restall_data(12345, dt.date(2021, 1, 1))

            retrieved_entry = db_handler.fetch_restall_data(12345)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag == 12345
            assert expected_date == dt.date(2021, 1, 1)
            assert actual_date is None

    def test_read_sell(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            planned = dt.date(2021, 1, 1)
            ear_tag_in = 12345
            db_handler.insert_sell_data(ear_tag_in, planned)

            retrieved_entry = db_handler.fetch_sell_data(ear_tag_in)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag == ear_tag_in
            assert expected_date == planned
            assert actual_date is None

    def test_read_bovalto2(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            db_handler.insert_bovalto2_data(12345, dt.date(2021, 1, 1))

            retrieved_entry = db_handler.fetch_bovalto2_data(12345)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag == 12345
            assert expected_date == dt.date(2021, 1, 1)
            assert actual_date is None

    def test_read_ringworm1(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            db_handler.insert_ringworm1_data(12345, dt.date(2021, 1, 1))

            retrieved_entry = db_handler.fetch_ringworm1_data(12345)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag == 12345
            assert expected_date == dt.date(2021, 1, 1)
            assert actual_date is None

    def test_read_ringworm2(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            db_handler.insert_ringworm2_data(12345, dt.date(2021, 1, 1))

            retrieved_entry = db_handler.fetch_ringworm2_data(12345)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag == 12345
            assert expected_date == dt.date(2021, 1, 1)
            assert actual_date is None


class TestDatabaseHandlerUpdateEntries:
    def test_update_calf(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            ear_tag = 12345
            gender = Gender.Female
            db_handler.insert_calf_data(ear_tag, gender, "breeding")

            db_handler.insert_calf_data(ear_tag, Gender.Male, "breeding")

            retrieved_entry = db_handler.fetch_calf_data(ear_tag)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, gender, calf_type = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag == ear_tag
            assert gender == Gender.Male
            assert calf_type == "breeding"

    def test_update_birth(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            ear_tag_in = 12345
            planned = dt.date(2021, 1, 1)
            actual = dt.date(2021, 1, 2)
            db_handler.insert_birth_data(ear_tag_in, planned)

            db_handler.insert_birth_data(ear_tag_in, planned, actual)

            retrieved_entry = db_handler.fetch_birth_data(ear_tag_in)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag_in == ear_tag
            assert expected_date == planned
            assert actual_date == actual

    def test_update_bovalto1(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            ear_tag_in = 12345
            planned = dt.date(2021, 1, 1)
            actual = dt.date(2021, 1, 2)
            db_handler.insert_bovalto1_data(ear_tag_in, planned)

            db_handler.insert_bovalto1_data(ear_tag_in, planned, actual)

            retrieved_entry = db_handler.fetch_bovalto1_data(ear_tag_in)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag_in == ear_tag
            assert expected_date == planned
            assert actual_date == actual

    def test_update_dehorn(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            ear_tag_in = 12345
            planned = dt.date(2021, 1, 1)
            actual = dt.date(2021, 1, 2)
            db_handler.insert_dehorn_data(ear_tag_in, planned)

            db_handler.insert_dehorn_data(ear_tag_in, planned, actual)

            retrieved_entry = db_handler.fetch_dehorn_data(ear_tag_in)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag_in == ear_tag
            assert expected_date == planned
            assert actual_date == actual

    def test_update_restall(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            ear_tag_in = 12345
            planned = dt.date(2021, 1, 1)
            actual = dt.date(2021, 1, 2)
            db_handler.insert_restall_data(ear_tag_in, planned)

            db_handler.insert_restall_data(ear_tag_in, planned, actual)

            retrieved_entry = db_handler.fetch_restall_data(ear_tag_in)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag_in == ear_tag
            assert expected_date == planned
            assert actual_date == actual

    def test_update_sell(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            ear_tag_in = 12345
            planned = dt.date(2021, 1, 1)
            actual = dt.date(2021, 1, 2)
            db_handler.insert_sell_data(ear_tag_in, planned)

            db_handler.insert_sell_data(ear_tag_in, planned, actual)

            retrieved_entry = db_handler.fetch_sell_data(ear_tag_in)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag_in == ear_tag
            assert expected_date == planned
            assert actual_date == actual

    def test_update_bovalto2(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            ear_tag_in = 12345
            planned = dt.date(2021, 1, 1)
            actual = dt.date(2021, 1, 2)
            db_handler.insert_bovalto2_data(ear_tag_in, planned)

            db_handler.insert_bovalto2_data(ear_tag_in, planned, actual)

            retrieved_entry = db_handler.fetch_bovalto2_data(ear_tag_in)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag_in == ear_tag
            assert expected_date == planned
            assert actual_date == actual

    def test_update_ringworm1(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            ear_tag_in = 12345
            planned = dt.date(2021, 1, 1)
            actual = dt.date(2021, 1, 2)
            db_handler.insert_ringworm1_data(ear_tag_in, planned)

            db_handler.insert_ringworm1_data(ear_tag_in, planned, actual)

            retrieved_entry = db_handler.fetch_ringworm1_data(ear_tag_in)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag_in == ear_tag
            assert expected_date == planned
            assert actual_date == actual

    def test_update_ringworm2(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            ear_tag_in = 12345
            planned = dt.date(2021, 1, 1)
            actual = dt.date(2021, 1, 2)
            db_handler.insert_ringworm2_data(ear_tag_in, planned)

            db_handler.insert_ringworm2_data(ear_tag_in, planned, actual)

            retrieved_entry = db_handler.fetch_ringworm2_data(ear_tag_in)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert retrieved_entry is not None
            assert ear_tag_in == ear_tag
            assert expected_date == planned
            assert actual_date == actual


class TestDatabaseHandlerDeleteEntries:
    def test_delete_calf(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            ear_tag_in = 12345
            planned = dt.date(2021, 1, 1)
            gen = Gender.Female
            actual = dt.date(2021, 1, 2)
            db_handler.insert_calf_data(ear_tag_in, gen, "breeding")
            db_handler.insert_birth_data(ear_tag_in, planned, actual)

            retrieved_entry = db_handler.fetch_calf_data(ear_tag_in)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3

            ear_tag, gender, calf_type = retrieved_entry[0]
            assert ear_tag_in == ear_tag
            assert gender == gen
            assert calf_type == "breeding"

            retrieved_entry = db_handler.fetch_birth_data(ear_tag_in)
            assert retrieved_entry is not None
            assert len(retrieved_entry) == 1
            assert len(retrieved_entry[0]) == 3
            ear_tag, expected_date, actual_date = retrieved_entry[0]
            assert ear_tag_in == ear_tag
            assert expected_date == planned
            assert actual_date == actual

            db_handler.delete_calf(ear_tag_in)

            retrieved_entry = db_handler.fetch_calf_data(ear_tag_in)
            assert retrieved_entry == []
            retrieved_entry = db_handler.fetch_birth_data(ear_tag_in)
            assert retrieved_entry == []


class TestDatabaseHandlerIntegration:
    def test_save_calf(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            calf = BreedingCalf(dt.date(2023, 11, 20), Gender.Female, 12345, True)

            db_handler.save_calf(calf)
            # Assertion no Exception is raised

    def test_fetch_fattening_calf(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            calf = FatteningCalf(dt.date(2023, 11, 20), Gender.Female, 12345, True)

            db_handler.save_calf(calf)

            retrieved_calf = db_handler.fetch_calf(12345)
            assert retrieved_calf is not None
            assert retrieved_calf.ear_tag == 12345
            assert retrieved_calf.gender == Gender.Female
            assert retrieved_calf.dehorning_required == True
            assert retrieved_calf.birth.expected_date == dt.date(2023, 11, 20)
            assert retrieved_calf.birth.actual_date is None
            assert retrieved_calf.bovalto_1.expected_date == dt.date(2023, 11, 30)
            assert retrieved_calf.bovalto_1.actual_date is None
            assert retrieved_calf.dehorn is not None
            assert retrieved_calf.dehorn.expected_date == dt.date(
                2023,
                12,
                5,
            )
            assert retrieved_calf.restall.expected_date == dt.date(2023, 12, 11)
            assert retrieved_calf.restall.actual_date is None
            assert retrieved_calf.sell.expected_date == dt.date(2023, 12, 19)
            assert retrieved_calf.sell.actual_date is None

    def test_fetch_fattening_calf_without_dehorning(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            calf = FatteningCalf(dt.date(2023, 11, 20), Gender.Female, 12345, False)

            db_handler.save_calf(calf)

            retrieved_calf = db_handler.fetch_calf(12345)
            assert retrieved_calf is not None
            assert retrieved_calf.ear_tag == 12345
            assert retrieved_calf.gender == Gender.Female
            assert retrieved_calf.dehorning_required == False
            assert retrieved_calf.birth.expected_date == dt.date(2023, 11, 20)
            assert retrieved_calf.birth.actual_date is None
            assert retrieved_calf.bovalto_1.expected_date == dt.date(2023, 11, 30)
            assert retrieved_calf.bovalto_1.actual_date is None
            assert retrieved_calf.dehorn is None
            assert retrieved_calf.restall.expected_date == dt.date(2023, 12, 5)
            assert retrieved_calf.restall.actual_date is None
            assert retrieved_calf.sell.expected_date == dt.date(2023, 12, 19)
            assert retrieved_calf.sell.actual_date is None

    def test_fetch_breeding_calf(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            calf = BreedingCalf(dt.date(2023, 11, 20), Gender.Female, 12345, True)

            db_handler.save_calf(calf)

            retrieved_calf = db_handler.fetch_calf(12345)
            assert retrieved_calf is not None
            assert retrieved_calf.ear_tag == 12345
            assert retrieved_calf.gender == Gender.Female
            assert retrieved_calf.dehorning_required == True
            assert retrieved_calf.birth.expected_date == dt.date(2023, 11, 20)
            assert retrieved_calf.birth.actual_date is None
            assert retrieved_calf.bovalto_1.expected_date == dt.date(2023, 11, 30)
            assert retrieved_calf.bovalto_1.actual_date is None
            assert retrieved_calf.dehorn is not None
            assert retrieved_calf.dehorn.expected_date == dt.date(
                2023,
                12,
                5,
            )
            assert retrieved_calf.restall.expected_date == dt.date(2023, 12, 11)
            assert retrieved_calf.restall.actual_date is None
            assert retrieved_calf.bovalto_2.expected_date == dt.date(2023, 12, 21)
            assert retrieved_calf.bovalto_2.actual_date is None
            assert retrieved_calf.ringworm_1.expected_date == dt.date(2023, 12, 26)
            assert retrieved_calf.ringworm_1.actual_date is None
            assert retrieved_calf.ringworm_2.expected_date == dt.date(2024, 1, 9)
            assert retrieved_calf.ringworm_2.actual_date is None

    def test_fetch_breeding_calf_without_dehorning(self):
        with DatabaseHandler(db_name="test.db", db_type="memory") as db_handler:
            calf = BreedingCalf(dt.date(2023, 11, 20), Gender.Female, 12345, False)

            db_handler.save_calf(calf)

            retrieved_calf = db_handler.fetch_calf(12345)
            assert retrieved_calf is not None
            assert retrieved_calf.ear_tag == 12345
            assert retrieved_calf.gender == Gender.Female
            assert retrieved_calf.dehorning_required == False
            assert retrieved_calf.birth.expected_date == dt.date(2023, 11, 20)
            assert retrieved_calf.birth.actual_date is None
            assert retrieved_calf.bovalto_1.expected_date == dt.date(2023, 11, 30)
            assert retrieved_calf.bovalto_1.actual_date is None
            assert retrieved_calf.dehorn is None
            assert retrieved_calf.restall.expected_date == dt.date(2023, 12, 5)
            assert retrieved_calf.restall.actual_date is None
            assert retrieved_calf.bovalto_2.expected_date == dt.date(2023, 12, 21)
            assert retrieved_calf.bovalto_2.actual_date is None
            assert retrieved_calf.ringworm_1.expected_date == dt.date(2023, 12, 26)
            assert retrieved_calf.ringworm_1.actual_date is None
            assert retrieved_calf.ringworm_2.expected_date == dt.date(2024, 1, 9)
            assert retrieved_calf.ringworm_2.actual_date is None
