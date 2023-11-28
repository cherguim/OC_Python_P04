"""
DBChess class is used to interact with TinyDB database.
It provides methods to load, save, update and delete records from the database.
"""

# Import the necessary modules
from tinydb import TinyDB, Query

# Define the path to the database files
DB_PATH = "data/chess_tournament/"
DB_PATH_PLAYER = DB_PATH + "players.json"
DB_PATH_TOURNAMENT = DB_PATH + "tournaments.json"
DB_PATH_ROUND = DB_PATH + "rounds.json"
DB_PATH_MATCH = DB_PATH + "matches.json"


# Create instances of TinyDB for players and tournaments databases

db_player = TinyDB(DB_PATH_PLAYER)
db_tournament = TinyDB(DB_PATH_TOURNAMENT)
db_round = TinyDB(DB_PATH_ROUND)
db_match = TinyDB(DB_PATH_MATCH)


class DBChess:
    def __init__(self, db, table):
        """Set the current table as an attribute of the DBChess instance"""
        self.table = db.table(table)

    def upsert_by_id(self, record, id):
        self.table.upsert(record, Query().id == id)

    def load_record(self, id_value: str):
        """Retrieve a record from the table based on its ID value"""
        # return self.table.search(Query()['id'] == id_value)
        return self.table.search(Query().id == id_value)[0]

    def load_records(self):
        """Retrieve all records from the table"""
        return self.table.all()

    def save_record(self, record):
        """Insert a new record into the table"""
        return self.table.insert(record)

    def update_record_by_doc_id(self, record, doc_id: int):
        """Update a record in the table based on its document ID"""
        return self.table.update(record, doc_ids=[doc_id])

    def delete_record_by_doc_id(self, doc_id: int):
        """Remove a record from the table based on its document ID"""
        return self.table.remove(doc_ids=[doc_id])
