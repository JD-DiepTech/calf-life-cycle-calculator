import os
import sys

# This code snippet does the following:
#     1. It adjusts the Python path to include the parent directory
#        (which contains models and other packages).
#        This allows Python to locate and import modules from these directories.
#     2. Then, it imports the necessary modules from the models package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sqlite3
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
from models.gender import Gender
from models.calf import BreedingCalf, FatteningCalf
from models.farm import Farm
import datetime as dt

database_creation_script = f"""
-- Create the calf table
CREATE TABLE calf (
  ear_tag INTEGER PRIMARY KEY,
  gender TEXT,
  type TEXT
);

-- Create the weight table
CREATE TABLE weight (
  ear_tag INTEGER,
  date TIMESTAMP,
  kg INTEGER,
  PRIMARY KEY (ear_tag, date),
  FOREIGN KEY (ear_tag) REFERENCES calf(ear_tag)
);

-- Create the bovalto1 table
CREATE TABLE {Birth.__name__.lower()} (
  ear_tag INTEGER PRIMARY KEY,
  planned TIMESTAMP,
  actual TIMESTAMP,
  FOREIGN KEY (ear_tag) REFERENCES calf(ear_tag)
);

-- Create the bovalto1 table
CREATE TABLE {Bovalto1.__name__.lower()} (
  ear_tag INTEGER PRIMARY KEY,
  planned TIMESTAMP,
  actual TIMESTAMP,
  FOREIGN KEY (ear_tag) REFERENCES calf(ear_tag)
);

-- Create the dehorn table
CREATE TABLE {Dehorn.__name__.lower()} (
  ear_tag INTEGER PRIMARY KEY,
  planned TIMESTAMP,
  actual TIMESTAMP,
  FOREIGN KEY (ear_tag) REFERENCES calf(ear_tag)
);

-- Create the restall table
CREATE TABLE {Restall.__name__.lower()} (
  ear_tag INTEGER PRIMARY KEY,
  planned TIMESTAMP,
  actual TIMESTAMP,
  FOREIGN KEY (ear_tag) REFERENCES calf(ear_tag)
);

-- Create the sell table
CREATE TABLE {Sell.__name__.lower()} (
  ear_tag INTEGER PRIMARY KEY,
  planned TIMESTAMP,
  actual TIMESTAMP,
  FOREIGN KEY (ear_tag) REFERENCES calf(ear_tag)
);

-- Create the bovalto2 table
CREATE TABLE {Bovalto2.__name__.lower()} (
  ear_tag INTEGER PRIMARY KEY,
  planned TIMESTAMP,
  actual TIMESTAMP,
  FOREIGN KEY (ear_tag) REFERENCES calf(ear_tag)
);

-- Create the ringworm1 table
CREATE TABLE {Ringworm1.__name__.lower()} (
  ear_tag INTEGER PRIMARY KEY,
  planned TIMESTAMP,
  actual TIMESTAMP,
  FOREIGN KEY (ear_tag) REFERENCES calf(ear_tag)
);

-- Create the ringworm2 table
CREATE TABLE {Ringworm2.__name__.lower()} (
  ear_tag INTEGER PRIMARY KEY,
  planned TIMESTAMP,
  actual TIMESTAMP,
  FOREIGN KEY (ear_tag) REFERENCES calf(ear_tag)
);
"""


def create_database():
    # Connect to SQLite database (creates if doesn't exist)
    conn = sqlite3.connect("calf_management.sqlite")
    cursor = conn.cursor()

    # Execute the SQL script
    cursor.executescript(database_creation_script)

    # Commit changes and close connection
    conn.commit()
    conn.close()


class DatabaseHandler:
    required_tables = [
        "calf",
        "weight",
        "birth",
        "bovalto1",
        "dehorn",
        "restall",
        "sell",
        "bovalto2",
        "ringworm1",
        "ringworm2",
    ]

    def __init__(self, db_name="data/calf_data.db", db_type="sqlite"):
        self.db_type = db_type
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        print("Connecting to database...")
        self.connection = self.connect()
        self.cursor = self.connection.cursor()

        # WARNING: This creates a difference between different types of databases
        if self.db_type == "memory":
            self.execute_query(database_creation_script)
        elif self.db_type == "sqlite":
            # Sanity check: Check if the database is not initialized yet
            if not self.check_all_tables_exist():
                # Create the database
                self.execute_query(database_creation_script)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection...")
        self.close()

    def check_all_tables_exist(self) -> bool:
        all_tables_exist = True
        existing_tables = []
        # Retrieve the list of tables in the database
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        rows = self.cursor.fetchall()
        for row in rows:
            existing_tables.append(row[0])

        # Check if all required tables exist
        for table in self.required_tables:
            if table not in existing_tables:
                all_tables_exist = False

        return all_tables_exist

    def connect(self) -> sqlite3.Connection:
        if self.db_type == "sqlite":
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print("Connected to SQLite database")
        elif self.db_type == "questdb":
            # Implement connection logic for QuestDB here
            pass
        elif self.db_type == "memory":
            self.connection = sqlite3.connect(":memory:")
            self.cursor = self.connection.cursor()
            print("Connected to SQLite database")
        else:
            raise ValueError("Unsupported database type")

        return self.connection

    def close(self):
        # if self.cursor:
        #     self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed")

    def execute_query(self, query: str):
        if self.connection:
            # Execute the SQL script
            self.cursor.executescript(query)

            # Commit changes and close connection
            self.connection.commit()
        else:
            raise Exception("Database connection is not established")

    # Functions to interact with the database can be added below
    def __fetch_data(self, table_name: str, ear_tag: int | None = None) -> list[tuple]:
        # if self.connection is None or self.cursor is None:
        #     self.connect()

        # Fetch data from a table
        if ear_tag is None:
            query = f"SELECT * FROM {table_name}"
        else:
            query = f"SELECT * FROM {table_name} WHERE ear_tag={ear_tag}"

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        return result

    def __insert_treatment_data(
        self,
        table_name: str,
        ear_tag: int,
        planned: dt.date,
        actual: dt.date | None = None,
    ):
        # Insert data in a table
        query = f"""
            INSERT OR REPLACE INTO {table_name} (ear_tag, planned, actual)
            VALUES ({ear_tag}, '{planned}', '{actual}')
        """

        self.cursor.execute(query)
        self.connection.commit()

    def convert_treatment_entries(self, entries: list[tuple]) -> list[tuple]:
        # Convert the date strings to datetime.date objects
        converted_entries = []
        for entry in entries:
            converted_entry = (
                entry[0],
                dt.datetime.strptime(entry[1], "%Y-%m-%d").date(),
                (
                    dt.datetime.strptime(entry[2], "%Y-%m-%d").date()
                    if entry[2] != str(None)
                    else None
                ),
            )
            converted_entries.append(converted_entry)

        return converted_entries

    def fetch_calf_data(self, ear_tag: int | None = None) -> list[tuple]:
        # Fetch data related to a specific calf from the 'calf' table
        retrieved_entries = self.__fetch_data("calf", ear_tag)

        converted_entries = []
        for entry in retrieved_entries:
            converted_entry = (
                entry[0],
                Gender.from_str(entry[1]),
                entry[2],
            )
            converted_entries.append(converted_entry)

        return converted_entries

    def fetch_weight_data(self, ear_tag: int | None = None) -> list[tuple]:
        # Fetch data related to a specific calf from the 'weight' table
        retrieved_entries = self.__fetch_data("weight", ear_tag)

        # Convert the date strings to datetime.date objects
        converted_entries = []
        for entry in retrieved_entries:
            converted_entry = (
                entry[0],
                dt.datetime.strptime(entry[1], "%Y-%m-%d").date(),
            )
            converted_entries.append(converted_entry)

        return converted_entries

    def fetch_birth_data(self, ear_tag: int | None = None) -> list[tuple]:
        # Fetch data related to a specific calf from the 'birth' table
        retrieved_entries = self.__fetch_data(Birth.__name__.lower(), ear_tag)

        # Convert the date strings to datetime.date objects
        return self.convert_treatment_entries(retrieved_entries)

    def fetch_bovalto1_data(self, ear_tag: int | None = None) -> list[tuple]:
        # Fetch data related to a specific calf from the 'bovalto1' table
        retrieved_entries = self.__fetch_data(Bovalto1.__name__.lower(), ear_tag)

        # Convert the date strings to datetime.date objects
        return self.convert_treatment_entries(retrieved_entries)

    def fetch_dehorn_data(self, ear_tag: int | None = None) -> list[tuple]:
        # Fetch data related to a specific calf from the 'dehorn' table
        retrieved_entries = self.__fetch_data(Dehorn.__name__.lower(), ear_tag)

        # Convert the date strings to datetime.date objects
        return self.convert_treatment_entries(retrieved_entries)

    def fetch_restall_data(self, ear_tag: int | None = None) -> list[tuple]:
        # Fetch data related to a specific calf from the 'restall' table
        retrieved_entries = self.__fetch_data(Restall.__name__.lower(), ear_tag)

        # Convert the date strings to datetime.date objects
        return self.convert_treatment_entries(retrieved_entries)

    def fetch_sell_data(self, ear_tag: int | None = None) -> list[tuple]:
        # Fetch data related to a specific calf from the 'sell' table
        retrieved_entries = self.__fetch_data(Sell.__name__.lower(), ear_tag)

        # Convert the date strings to datetime.date objects
        return self.convert_treatment_entries(retrieved_entries)

    def fetch_bovalto2_data(self, ear_tag: int | None = None) -> list[tuple]:
        # Fetch data related to a specific calf from the 'bovalto2' table
        retrieved_entries = self.__fetch_data(Bovalto2.__name__.lower(), ear_tag)

        # Convert the date strings to datetime.date objects
        return self.convert_treatment_entries(retrieved_entries)

    def fetch_ringworm1_data(self, ear_tag: int | None = None) -> list[tuple]:
        # Fetch data related to a specific calf from the 'ringworm1' table
        retrieved_entries = self.__fetch_data(Ringworm1.__name__.lower(), ear_tag)

        # Convert the date strings to datetime.date objects
        return self.convert_treatment_entries(retrieved_entries)

    def fetch_ringworm2_data(self, ear_tag: int | None = None) -> list[tuple]:
        # Fetch data related to a specific calf from the 'ringworm2' table
        retrieved_entries = self.__fetch_data(Ringworm2.__name__.lower(), ear_tag)

        # Convert the date strings to datetime.date objects
        return self.convert_treatment_entries(retrieved_entries)

    def insert_calf_data(self, ear_tag: int, gender: Gender, calf_type: str):
        if calf_type not in ["breeding", "fattening"]:
            raise ValueError("Invalid calf type")

        query = f"""
            INSERT OR REPLACE INTO calf (ear_tag, gender, type)
            VALUES ({ear_tag}, '{gender}', '{calf_type}')
        """

        self.cursor.execute(query)
        self.connection.commit()

    def insert_weight(self, ear_tag: int, weight: int, date: dt.date):
        query = f"""
            INSERT OR REPLACE INTO calf (ear_tag, date, kg)
            VALUES ({ear_tag}, '{date}', '{weight}')
        """

        self.cursor.execute(query)
        self.connection.commit()

    def insert_birth_data(
        self, ear_tag: int, planned: dt.date, actual: dt.date | None = None
    ):
        return self.__insert_treatment_data(
            Birth.__name__.lower(), ear_tag, planned, actual
        )

    def insert_bovalto1_data(
        self, ear_tag: int, planned: dt.date, actual: dt.date | None = None
    ):
        return self.__insert_treatment_data(
            Bovalto1.__name__.lower(), ear_tag, planned, actual
        )

    def insert_dehorn_data(
        self, ear_tag: int, planned: dt.date, actual: dt.date | None = None
    ):
        return self.__insert_treatment_data(
            Dehorn.__name__.lower(), ear_tag, planned, actual
        )

    def insert_restall_data(
        self, ear_tag: int, planned: dt.date, actual: dt.date | None = None
    ):
        return self.__insert_treatment_data(
            Restall.__name__.lower(), ear_tag, planned, actual
        )

    def insert_sell_data(
        self, ear_tag: int, planned: dt.date, actual: dt.date | None = None
    ):
        return self.__insert_treatment_data(
            Sell.__name__.lower(), ear_tag, planned, actual
        )

    def insert_bovalto2_data(
        self, ear_tag: int, planned: dt.date, actual: dt.date | None = None
    ):
        return self.__insert_treatment_data(
            Bovalto2.__name__.lower(), ear_tag, planned, actual
        )

    def insert_ringworm1_data(
        self, ear_tag: int, planned: dt.date, actual: dt.date | None = None
    ):
        return self.__insert_treatment_data(
            Ringworm1.__name__.lower(), ear_tag, planned, actual
        )

    def insert_ringworm2_data(
        self, ear_tag: int, planned: dt.date, actual: dt.date | None = None
    ):
        return self.__insert_treatment_data(
            Ringworm2.__name__.lower(), ear_tag, planned, actual
        )

    def save_breeding_calf(self, calf: BreedingCalf):
        self.insert_calf_data(calf.ear_tag, calf.gender, calf.calf_type)
        self.insert_birth_data(
            calf.ear_tag, calf.birth.expected_date, calf.birth.actual_date
        )
        self.insert_bovalto1_data(
            calf.ear_tag, calf.bovalto_1.expected_date, calf.bovalto_1.actual_date
        )
        if calf.dehorn:
            self.insert_dehorn_data(
                calf.ear_tag, calf.dehorn.expected_date, calf.dehorn.actual_date
            )
        self.insert_restall_data(
            calf.ear_tag, calf.restall.expected_date, calf.restall.actual_date
        )
        self.insert_bovalto2_data(
            calf.ear_tag, calf.bovalto_2.expected_date, calf.bovalto_2.actual_date
        )
        self.insert_ringworm1_data(
            calf.ear_tag, calf.ringworm_1.expected_date, calf.ringworm_1.actual_date
        )
        self.insert_ringworm2_data(
            calf.ear_tag, calf.ringworm_2.expected_date, calf.ringworm_2.actual_date
        )

    def save_fattening_calf(self, calf: FatteningCalf):
        self.insert_calf_data(calf.ear_tag, calf.gender, calf.calf_type)
        self.insert_birth_data(
            calf.ear_tag, calf.birth.expected_date, calf.birth.actual_date
        )
        self.insert_bovalto1_data(
            calf.ear_tag, calf.bovalto_1.expected_date, calf.bovalto_1.actual_date
        )
        if calf.dehorn:
            self.insert_dehorn_data(
                calf.ear_tag, calf.dehorn.expected_date, calf.dehorn.actual_date
            )
        self.insert_restall_data(
            calf.ear_tag, calf.restall.expected_date, calf.restall.actual_date
        )
        self.insert_sell_data(
            calf.ear_tag, calf.sell.expected_date, calf.sell.actual_date
        )

    def save_calf(self, calf: BreedingCalf | FatteningCalf):
        if isinstance(calf, BreedingCalf):
            self.save_breeding_calf(calf)
        elif isinstance(calf, FatteningCalf):
            self.save_fattening_calf(calf)
        else:
            raise ValueError("Unsupported calf type")

    def save_farm(self, farm: Farm):
        for calf in farm.get_calves():
            self.save_calf(calf)

    def fetch_calf(self, ear_tag: int) -> BreedingCalf | FatteningCalf | None:
        """
        Fetches a calf from the database and returns it as a BreedingCalf or FatteningCalf object.

        When fetching data from the database it is supposed to be complete.
        Hence, we will strictly use the data from the database to create the calf object.
        :param ear_tag: The ear tag of the calf to fetch
        :return: BreedingCalf or FatteningCalf object, and None if the ear tag is not found
        """
        calf_data = self.fetch_calf_data(ear_tag)[0]
        if len(calf_data) == 0:
            return None

        birth_data = self.fetch_birth_data(ear_tag)[0]
        bovalto1_data = self.fetch_bovalto1_data(ear_tag)[0]
        dehorn_data = self.fetch_dehorn_data(ear_tag)  # Might be empty
        restall_data = self.fetch_restall_data(ear_tag)[0]

        gender = calf_data[1]
        calf_type = calf_data[2]

        birth_planned = birth_data[1]
        birth_actual = birth_data[2]
        birth = Birth(birth_planned)
        birth.reset(birth_planned, birth_actual)

        bovalto1_planned = bovalto1_data[1]
        bovalto1_actual = bovalto1_data[2]
        bovalto1 = Bovalto1(birth)
        bovalto1.reset(bovalto1_planned, bovalto1_actual)

        restall_planned = restall_data[1]
        restall_actual = restall_data[2]

        if len(dehorn_data) > 0:
            dehorn_data = dehorn_data[0]
            dehorn_planned = dehorn_data[1]
            dehorn_actual = dehorn_data[2]
            dehorning_required = True
            dehorn = Dehorn(bovalto1)
            dehorn.reset(dehorn_planned, dehorn_actual)

            restall = Restall(dehorn)
            restall.reset(restall_planned, restall_actual)
        else:
            dehorn_planned = None
            dehorn_actual = None
            dehorning_required = False

            dehorn = None

            restall = Restall(bovalto1)
            restall.reset(restall_planned, restall_actual)

        if calf_type == "breeding":
            calf = BreedingCalf(
                birth_planned,
                gender,
                ear_tag,
                dehorning_required,
            )

            bovalto2_data = self.fetch_bovalto2_data(ear_tag)[0]
            ringworm1_data = self.fetch_ringworm1_data(ear_tag)[0]
            ringworm2_data = self.fetch_ringworm2_data(ear_tag)[0]

            bovalto2_planned = bovalto2_data[1]
            bovalto2_actual = bovalto2_data[2]
            bovalto2 = Bovalto2(bovalto1)
            bovalto2.reset(bovalto2_planned, bovalto2_actual)

            ringworm1_planned = ringworm1_data[1]
            ringworm1_actual = ringworm1_data[2]
            ringworm1 = Ringworm1(bovalto2)
            ringworm1.reset(ringworm1_planned, ringworm1_actual)

            ringworm2_planned = ringworm2_data[1]
            ringworm2_actual = ringworm2_data[2]
            ringworm2 = Ringworm2(ringworm1)
            ringworm2.reset(ringworm2_planned, ringworm2_actual)

            calf.reset(birth, bovalto1, dehorn, restall, bovalto2, ringworm1, ringworm2)

        elif calf_type == "fattening":
            calf = FatteningCalf(
                birth_planned,
                gender,
                ear_tag,
                dehorning_required,
            )

            sell_data = self.fetch_sell_data(ear_tag)[0]
            sell_planned = sell_data[1]
            sell_actual = sell_data[2]

            sell = Sell(calf.birth)
            sell.reset(sell_planned, sell_actual)

            calf.reset(birth, bovalto1, dehorn, restall, sell)

        else:
            raise ValueError("Unsupported calf type")

        # TODO: Implement the weight of a calf
        # Fetch weight data
        # weight_data = self.fetch_weight_data(ear_tag)
        # for entry in weight_data:
        #     calf.add_weight(entry[1], entry[2])

        return calf

    def delete_calf(self, ear_tag: int):
        query = f"""
            DELETE FROM calf WHERE ear_tag = {ear_tag};
            DELETE FROM weight WHERE ear_tag = {ear_tag};
            DELETE FROM {Birth.__name__.lower()} WHERE ear_tag = {ear_tag};
            DELETE FROM {Bovalto1.__name__.lower()} WHERE ear_tag = {ear_tag};
            DELETE FROM {Dehorn.__name__.lower()} WHERE ear_tag = {ear_tag};
            DELETE FROM {Restall.__name__.lower()} WHERE ear_tag = {ear_tag};
            DELETE FROM {Sell.__name__.lower()} WHERE ear_tag = {ear_tag};
            DELETE FROM {Bovalto2.__name__.lower()} WHERE ear_tag = {ear_tag};
            DELETE FROM {Ringworm1.__name__.lower()} WHERE ear_tag = {ear_tag};
            DELETE FROM {Ringworm2.__name__.lower()} WHERE ear_tag = {ear_tag};
        """

        try:
            self.cursor.executescript(query)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting entries: {e}")


if __name__ == "__main__":
    db_path = f"test_calf_data.sqlite"
    # table_name = "calves"

    # Create the database
    create_database()

    # db_handler = DatabaseHandler()
    # data = db_handler.fetch_calf_data()
    #
    # for row in data:
    #     print(row)
