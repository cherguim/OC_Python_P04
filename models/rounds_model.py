from models.database_model import DBChess
from models.database_model import db_round

db_round = DBChess(db_round, "round")


class Round:
    """This class represents a model of match."""

    def __init__(
        self,
        round_name="",
        datetime_begin="",
        datetime_end="",
        list_match=[],
        status="",
        id="",
    ):
        self.round_name = round_name            # The name of the round.
        self.datetime_begin = datetime_begin    # The start datetime of the round.
        self.datetime_end = datetime_end        # The end datetime of the round.
        self.list_match = list_match            # A list of match IDs associated with the round.
        self.status = status                    # The status of the round (started, ended).
        self.id = id                            # The ID of the round.

    def save_update_record(self):
        """Save or update the round attributes in the database based on the self.id attribute"""
        db_round.upsert_by_id(self.__dict__, self.id)

    def save_record(self):
        """Save the round attributes to the database."""
        db_round.save_record(self.__dict__)

    def update_record(self):
        """Update the round attributes in the database."""
        db_round.update_record_by_id(self.__dict__, id)

    def load_by_id(self, id):
        """Load a round from the database to round attributes."""
        record = db_round.load_record(id)
        self.__dict__.update(record)
