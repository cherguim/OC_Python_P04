from views.game_view import ViewGame
from views.menu_view import ViewMenu
from .player_controller import ControllerPlayer
from .tournament_controller import ControllerTournament
from .report_controller import ControllerReport
from .game_controller import ControllerGame

"""This controller is tasked with displaying the menus of the Chess Tournament application and
directing user input to the various menus or fonction of the application."""

controllergame = ControllerGame()
tournament = controllergame.tournament


class ControllerMenuHome:
    """This controller display the main menu [Chess tournament Home menu]."""

    def __call__(self):
        while True:
            user_answer = ViewMenu.menu_home()
            # (1) - Player management.
            if user_answer == "1":
                return ControllerMenuPlayer()
            # (2) - Tournament management.
            if user_answer == "2":
                return ControllerMenuTournament()
            # (3) - Reports management.
            if user_answer == "3":
                return ControllerMenuReport()
            # (q) - Quit.
            if user_answer in ("q", "Q"):
                return ControllerMenuQuit()


class ControllerMenuPlayer:
    """This controller display the menu [Player management]."""

    def __call__(self):
        while True:
            ControllerPlayer.players_display()
            user_answer = ViewMenu.menu_player()
            if user_answer in ControllerPlayer.options_sort:
                ControllerPlayer.players_sort_by(user_answer)
            # (1) - Add players
            if user_answer == "1":
                ControllerPlayer.player_add()
                return ControllerMenuPlayer()
            # (2) - Update players
            if user_answer == "2":
                ControllerPlayer.player_update()
                return ControllerMenuPlayer()
            # (3) - Delete players
            if user_answer == "3":
                ControllerPlayer.player_delete()
                return ControllerMenuPlayer()
            # (4) - Import players
            if user_answer == "4":
                ControllerPlayer.player_import()
                return ControllerMenuPlayer()
            # (q) - Back
            if user_answer in ("q", "Q"):
                return ControllerMenuHome()


class ControllerMenuTournament:
    """This controller display the menu [Tournament Management]."""

    def __call__(self):
        while True:
            ControllerTournament.tournaments_display()
            user_answer = ViewMenu.menu_tournament()
            if user_answer in ControllerTournament.options_sort:
                ControllerTournament.tournaments_sort_by(user_answer)
            # (1) - Display or run a tournament / Run or update a tournament
            if user_answer == "1":
                controllergame.select_tournament()
                if tournament.status == "not started":
                    return ControllerMenuAddPlayersToTournament()
                if tournament.status == "started":
                    ControllerReport.display_tournament_all(controllergame)
                    return ControllerMenuAddScore()
                if tournament.status == "ended":
                    ControllerReport.display_tournament_all(controllergame)
                    return ControllerMenuTournament()
            # (2) - Add tournaments
            if user_answer == "2":
                ControllerTournament.tournament_add()
                return ControllerMenuTournament()
            # (3) - Update tournaments list
            if user_answer == "3":
                ControllerTournament.tournament_update()
                return ControllerMenuTournament()
            # (4) - Delete tournaments
            if user_answer == "4":
                ControllerTournament.tournament_delete()
                return ControllerMenuTournament()
            # (q) - Back
            if user_answer in ("q", "Q"):
                return ControllerMenuHome()


class ControllerMenuAddPlayersToTournament:
    """This controller display the menu [Add players to a tournament]."""

    def __call__(self):
        while True:
            ControllerPlayer.players_display(tournament)
            user_answer = ViewMenu.menu_add_players_to_tournament(tournament.__dict__)
            if user_answer in ControllerPlayer.options_sort:
                ControllerPlayer.players_sort_by(user_answer)
            # (1) - Change tournament
            if user_answer == "1":
                ControllerTournament.tournaments_display()
                controllergame.select_tournament()
                return ControllerMenuAddPlayersToTournament()
            # (2) - Add or remove players to selected tournament with a *
            if user_answer == "2":
                controllergame.add_or_remove_players()
                return ControllerMenuAddPlayersToTournament()
            # (3) - Remove all players with a *
            if user_answer == "3":
                controllergame.remove_all_players()
                return ControllerMenuAddPlayersToTournament()
            # (4) - Start the tournament
            if user_answer == "4":
                controllergame.start_tournament()
                if tournament.status == "not started":
                    return ControllerMenuAddPlayersToTournament()
                if tournament.status == "started":
                    return ControllerMenuAddScore()
            # (q) - Back
            if user_answer in ("q", "Q"):
                return ControllerMenuTournament()
        return


class ControllerMenuAddScore:
    """This controller display the menu [Add scores]."""

    def __call__(self):
        while True:
            controllergame.display_last_round()
            user_answer = ViewMenu.menu_add_scores()
            # (1) - Add scores
            if user_answer == "1":
                controllergame.add_scores()
                return ControllerMenuAddScore()
            # (2) - Round validation
            if user_answer == "2":
                controllergame.round_validation()
                if tournament.status == "started":
                    return ControllerMenuAddScore()
                if tournament.status == "ended":
                    return ControllerMenuTournament()
            # (q) - Back
            if user_answer in ("q", "Q"):
                return ControllerMenuTournament()
        return


class ControllerMenuReport:
    """This controller display the menu [Reports Management]."""

    def __call__(self):
        while True:
            user_answer = ViewMenu.menu_report()
            # (1) - Display all players
            if user_answer == "1":
                return ControllerMenuReportPlayers()
            # (2) - Display all tournaments
            if user_answer == "2":
                return ControllerMenuReportTournaments()
            # (3) - Display summarize of a tournament
            if user_answer == "3":
                return ControllerMenuReportTournamentSummarize()
            # (4) - Display a list of tournament players
            if user_answer == "4":
                return ControllerMenuReportTournamentPlayers()
            # (5) - Display a list of all tournament rounds and all round matches
            if user_answer == "5":
                return ControllerMenuReportTournamentRoundsMmatches()
            # (6) - Display all of a tournament
            if user_answer == "6":
                return ControllerMenuReportTournamentAll()
            # (q) - Back
            if user_answer in ("q", "Q"):
                return ControllerMenuHome()


class ControllerMenuReportPlayers:
    """This controller display the menu [ReportPlayer]."""

    def __call__(self):
        while True:
            ControllerPlayer.players_display()
            user_answer = ViewMenu.menu_back()
            if user_answer in ControllerPlayer.options_sort:
                ControllerPlayer.players_sort_by(user_answer)
            # (q) - Back
            if user_answer in ("q", "Q"):
                return ControllerMenuReport()


class ControllerMenuReportTournaments:
    """This controller display the menu [Report Tournament]."""

    def __call__(self):
        while True:
            ControllerTournament.tournaments_display()
            user_answer = ViewMenu.menu_back()
            if user_answer in ControllerTournament.options_sort:
                ControllerTournament.tournaments_sort_by(user_answer)
            if user_answer in ("q", "Q"):
                return ControllerMenuReport()


class ControllerMenuReportTournamentSummarize:
    """This controller display the menu [Report Tournament Summarize]."""

    def __call__(self):
        while True:
            ControllerTournament.tournaments_display()
            user_answer = ViewMenu.menu_select_tournament()
            if user_answer in ControllerTournament.options_sort:
                ControllerTournament.tournaments_sort_by(user_answer)
            # (1) - Select a tournament
            if user_answer == "1":
                controllergame.select_tournament()
                ControllerReport.display_tournament_summarize(tournament)
                ViewGame.display_message()
            if user_answer in ("q", "Q"):
                return ControllerMenuReport()


class ControllerMenuReportTournamentPlayers:
    """This controller display the menu [Report Tournament Players]."""

    def __call__(self):
        while True:
            ControllerTournament.tournaments_display()
            user_answer = ViewMenu.menu_select_tournament()
            if user_answer in ControllerTournament.options_sort:
                ControllerTournament.tournaments_sort_by(user_answer)
            # (1) - Select a tournament
            if user_answer == "1":
                controllergame.select_tournament()
                ControllerReport.display_tournament_players(tournament)
                ViewGame.display_message()
            if user_answer in ("q", "Q"):
                return ControllerMenuReport()


class ControllerMenuReportTournamentRoundsMmatches:
    """This controller display the menu [Report Tournament Rounds & Matches]."""

    def __call__(self):
        while True:
            ControllerTournament.tournaments_display()
            user_answer = ViewMenu.menu_select_tournament()
            if user_answer in ControllerTournament.options_sort:
                ControllerTournament.tournaments_sort_by(user_answer)
            # (1) - Select a tournament
            if user_answer == "1":
                controllergame.select_tournament()
                ViewGame.clear_screen()
                ControllerReport.display_tournament_rounds_matches(tournament)
                ViewGame.display_message()
            if user_answer in ("q", "Q"):
                return ControllerMenuReport()


class ControllerMenuReportTournamentAll:
    """This controller display the menu [Report Tournament all]."""

    def __call__(self):
        while True:
            ControllerTournament.tournaments_display()
            user_answer = ViewMenu.menu_select_tournament()
            if user_answer in ControllerTournament.options_sort:
                ControllerTournament.tournaments_sort_by(user_answer)
            # (1) - Select a tournament
            if user_answer == "1":
                controllergame.select_tournament()
                ViewGame.clear_screen()
                ControllerReport.display_tournament_all(controllergame)
            if user_answer in ("q", "Q"):
                return ControllerMenuReport()


class ControllerMenuQuit:
    """This controller display the Menu [Quit the Chess Tournament]"""

    def __call__(self):
        while True:
            user_answer = ViewMenu.menu_quit()
            # (1) - Yes
            if user_answer in ("y", "Y"):
                return None
            # (2) - NO
            if user_answer in ("n", "N"):
                return ControllerMenuHome()
