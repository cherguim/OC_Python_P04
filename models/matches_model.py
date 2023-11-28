from models.database_model import DBChess
from models.database_model import db_match
from models.players_model import Player

db_match = DBChess(db_match, "match")


class Match:
    """This class represents a model of a match. It has methods to create, update,
    and load match records from a database.
    It also has methods to add and remove attributes related to the players involved in the match.
    """
    def __init__(self, id_chess_A="", score_A="0", id_chess_B="", score_B="0", id=""):
        self.id_chess_A = id_chess_A    # The ID of player A in the match.
        self.score_A = score_A          # The score of player A in the match.
        self.id_chess_B = id_chess_B    # The ID of player B in the match.
        self.score_B = score_B          # The score of player B in the match.
        self.id = id                    # The ID of the match.

    def match(self):
        """Get the match details.
        Returns a tuple containing two lists, each representing a player's ID and score.
        """
        match = ([self.id_chess_A, self.score_A], [self.id_chess_B, self.score_B])
        return match

    def save_update_record(self):
        """Save or update the match record in the database using the self.id attribute."""
        self.del_attributes()
        db_match.upsert_by_id(self.__dict__, self.id)

    def load_by_id(self, id):
        """Loads a match from the database based on id and fills the match attributes."""
        record = db_match.load_record(id)
        self.__dict__.update(record)
        self.add_attributes()

    def add_attributes(self):
        """Add player attributes to the match model."""
        player = Player()
        player.load_by_id(self.id_chess_A)
        self.__dict__.update(
            {"first_name_A": player.first_name, "last_name_A": player.last_name}
        )
        player.load_by_id(self.id_chess_B)
        self.__dict__.update(
            {"first_name_B": player.first_name, "last_name_B": player.last_name}
        )

    def del_attributes(self):
        """Remove player attributes."""
        list_del_attributes = [
            "first_name_A",
            "last_name_A",
            "first_name_B",
            "last_name_B",
        ]
        for attribute in list_del_attributes:
            if hasattr(self, attribute):
                delattr(self, attribute)
