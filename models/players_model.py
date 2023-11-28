"""This class represents a model of player and perform
CRUD operations on the database.
"""

from models.database_model import DBChess
from models.database_model import db_player
from models.database_model import db_tournament

# Initialize DBChess objects
db_player = DBChess(db_player, "player")
db_tournament = DBChess(db_tournament, "player")


class Player:
    """Class Player is used to create a player object and perform CRUD operations on the database."""

    def __init__(
        self,
        sex="",             # The sex of the player (M/F).
        first_name="",      # The first name of the player.
        last_name="",       # The last name of the player.
        country_code="",    # The ISO 3166 alpha-3 code of the player's country.
        date_of_birth="",   # The date of birth of the player in the format 'YYYY-MM-DD'.
        rating="",          # The Elo rating of the player.
        rank="",            # The rank of the player according to FIDE.
        id="",              # The unique identifier of the player.
    ):
        """Initialize the player attributs with given parameters."""
        self.sex = sex
        self.first_name = first_name
        self.last_name = last_name
        self.country_code = country_code
        self.date_of_birth = date_of_birth
        self.rating = rating
        self.rank = rank
        self.id = id
        self.doc_id = ""  # doc_id will not be saved in db

    def save(self):
        """Save the player attributes in the database."""
        delattr(self, "doc_id")  # doc_id will not be saved in db
        db_player.save_record(self.__dict__)

    def update(self):
        """Update the player attributes in the database."""
        doc_id_ = self.doc_id
        delattr(self, "doc_id")  # doc_id will not be saved in db
        db_player.update_record_by_doc_id(self.__dict__, doc_id_)

    def load_by_id(self, id):
        """Loads a player from the database and updates the player attributes."""
        record = db_player.load_record(id)
        self.doc_id = (
            record.doc_id
        )  # add the document id to doc_id attribut of player object
        self.__dict__.update(record)

    def load_all(self):
        """Load all players from the database and return a player object list."""
        players_object = []
        for record in db_player.load_records():
            player = Player()
            player.__dict__.update(record)
            player.doc_id = (
                record.doc_id
            )  # Add the document id to doc_id attribut of player model
            players_object.append(player)
        return players_object

    def delete(self):
        """Delete a player from the database."""
        db_player.delete_record_by_doc_id(self.doc_id)
