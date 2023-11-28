from models.tournaments_model import Tournament
from views.tournaments_view import ViewTournament

# A dictionary of options for sorting the tournaments.
OPTIONS_TOURNAMENTS = {
    "a": "name",
    "b": "description",
    "c": "location",
    "d": "status",
    "e": "date_begin",
    "f": "date_end",
    "z": "",
}


class ControllerTournament:
    """This class manages the registration of tournaments, display, sorting, deletion and updating."""

    options_sort = OPTIONS_TOURNAMENTS  # A dictionary of options for sorting the tournaments.
    sort_by = ""                        # The attribute to sort the tournaments by.
    tournaments_list = []               # A list of tournament dictionaries.

    def tournament_add():
        """
        Adds a new tournament by collecting information from the user,
        creating a Tournament object, and saving it.
        """
        user_answers = ViewTournament.add_tournament()
        tournament = Tournament(**user_answers)
        tournament.save_record()
        ViewTournament.display_tournament_details(tournament.__dict__)
        user_answers = ViewTournament.get_yes_or_no_add_another_tournament()
        if user_answers == "y":
            ControllerTournament.tournament_add()

    def tournaments_display():
        """
        Retrieves all tournaments from the database,
        sorts them if a sort option is specified, and displays them.
        """
        ControllerTournament.tournaments_list = []
        tournament = Tournament()
        tournaments_objects = tournament.load_records()
        for tournament in tournaments_objects:
            ControllerTournament.tournaments_list.append(tournament.__dict__)
        if not ControllerTournament.sort_by == "":
            ControllerTournament.tournaments_list.sort(
                key=lambda x: x[ControllerTournament.sort_by]
            )
        ViewTournament.display_tournaments(ControllerTournament.tournaments_list)
        return

    def tournaments_sort_by(user_answer):
        """Sorts the tournaments based on the specified sort option."""
        if user_answer in OPTIONS_TOURNAMENTS:
            sort_option = OPTIONS_TOURNAMENTS[user_answer]
            ControllerTournament.sort_by = sort_option
            ControllerTournament.tournaments_display()

    def tournament_delete():
        """Allows the user to select tournaments to delete and deletes them from the database."""
        tournaments_selected_to_delete = ViewTournament.select_tournaments_to_delete(
            ControllerTournament.tournaments_list
        )
        if tournaments_selected_to_delete:
            tournament = Tournament()
            user_answers = ViewTournament.get_yes_or_no_delete_tournaments()
            if user_answers == "y":
                for tournament_list in tournaments_selected_to_delete:
                    tournament.__dict__.update(tournament_list)
                    tournament.delete_record()
        return ControllerTournament.tournaments_display()

    def tournament_update():
        """
        Allows the user to select tournaments to update,
        updates their information, and saves the changes to the database.
        """
        tournaments_selected_to_update = ViewTournament.select_tournaments_to_update(
            ControllerTournament.tournaments_list
        )
        if tournaments_selected_to_update:
            tournament = Tournament()
            for i, tournament_list in enumerate(tournaments_selected_to_update):
                tournament_updated = ViewTournament.update_tournament(tournament_list)
                tournament.__dict__.update(tournament_updated)
                tournament.update_record()
                ViewTournament.display_tournament_details(tournament.__dict__)
                if i != len(tournaments_selected_to_update) - 1:
                    user_answers = ViewTournament.get_yes_or_no_update_next_tournament()
                    if user_answers == "n":
                        break
                else:
                    ViewTournament.get_exit_pause()
        return ControllerTournament.tournaments_display()
