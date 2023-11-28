from datetime import datetime
from utils.utils import clear_screen
from utils.utils import print_section
from utils.utils import Check
from utils.utils import SECTION_CHAR

DEFAULT_ROUNDS_MAX = "4"
ROUNDS_MAX = "10"
SECTION_WIDTH = 147


class ViewTournament:
    """This class represents a menu interface for managing tournaments"""

    def add_tournament():
        """
        This method prompts the user for input to add a tournament and
        returns a dictionary containing the tournament details.
        """
        clear_screen()
        print_section("| Add a tournament |", SECTION_CHAR, 60)
        print()

        while True:
            name = input("name: ").strip().capitalize()
            if name and Check.is_string_limit(name):
                break
            print(
                "Invalid input for 'name'.\nPlease enter only alphabets, spaces,"
                "appropriate hyphens and up to 60 characters."
            )

        while True:
            description = input("description: ").strip().capitalize()
            if description and Check.is_string_limit(description):
                break
            print(
                "Invalid input for 'description'.\nPlease enter only alphabets, spaces,"
                "appropriate hyphens and up to 60 characters."
            )

        while True:
            location = input("location: ").strip().capitalize()
            if location and Check.is_string_limit(location):
                break
            print(
                "Invalid input for 'description'.\nPlease enter only alphabets, spaces,"
                "appropriate hyphens and up to 60 characters."
            )

        while True:
            date_begin = input("Enter start date (yyyy-mm-dd): ")
            if Check.is_valid_date(date_begin):
                date_begin = datetime.strptime(date_begin, "%Y-%m-%d").strftime("%Y-%m-%d")
                break
            print(
                "Invalid date format. Please enter a valid date in yyyy-mm-dd format."
            )

        while True:
            date_end = input("Enter end date (yyyy-mm-dd): ")
            if Check.is_valid_date(date_end):
                if datetime.strptime(date_end, "%Y-%m-%d") >= datetime.strptime(date_begin, "%Y-%m-%d"):
                    date_end = datetime.strptime(date_end, "%Y-%m-%d").strftime("%Y-%m-%d")
                    break
            print(
                "Invalid end date. Please enter a valid date in yyyy-mm-dd format that is the same or"
                "after the start date."
            )

        while True:
            rounds_max = input(
                f"number of rounds (default: {DEFAULT_ROUNDS_MAX}): "
            ).strip()
            if not rounds_max:
                rounds_max = DEFAULT_ROUNDS_MAX
                break
            try:
                if 1 <= int(rounds_max) <= int(ROUNDS_MAX):
                    break
                else:
                    print(
                        f"Enter a number between 1 and {int(ROUNDS_MAX)} (default: {int(DEFAULT_ROUNDS_MAX)})."
                    )
            except ValueError:
                print("Enter a valid number.")
        print()

        round_actual = "0"
        status = "not started"
        rounds_list = []
        players_list = []
        id = ""

        return {
            'name': name,
            'description': description,
            'location': location,
            'date_begin': date_begin,
            'date_end': date_end,
            'round_actual': round_actual,
            'rounds_max': rounds_max,
            'status': status,
            'rounds_list': rounds_list,
            'players_list': players_list,
            'id': id
        }

    def display_tournament_details(tournament_dict):
        """This method displays the details of a tournament."""
        print_section("| Tournament Détails |", SECTION_CHAR, SECTION_WIDTH)
        print(
            "\n"
            f"Name: {str.capitalize(tournament_dict.get('name', ''))}\n"
            f"Description: {str.capitalize(tournament_dict.get('description', ''))}\n"
            f"Location: {str.capitalize(tournament_dict.get('location', ''))}\n"
            f"Date_begin: {tournament_dict.get('date_begin', '')}\n"
            f"Date_end: {tournament_dict.get('date_end', '')}\n"
            f"Rounds_max: {tournament_dict.get('rounds_max', '')}"
        )

    def get_yes_or_no_add_another_tournament():
        """
        This method prompts the user for input to add another tournament and
        returns the user's answer.
        """
        print("\nThis information has been saved in the database.\n")
        while True:
            user_answer = input("Do you want to add another tournament (y/n)?").lower()
            if user_answer in ("y", "n"):
                break
            print("please, enter " "y" " or " "n" ".")
        return user_answer

    def display_tournaments(tournaments_list):
        """This method displays a list of tournaments."""
        clear_screen()
        print_section("| Tournament list |", SECTION_CHAR, SECTION_WIDTH)
        print()
        if not tournaments_list:
            print("The tournament list is currently empty.\n")
            return
        print(
            f"{'#':<6}"
            f"{'NAME':<30}"
            f"{'DESCRIPTION NAME':<30}"
            f"{'LOCATION':<30}"
            f"{'STATUS':<13}"
            f"{'START DATE':<12}"
            f"{'END DATE':<12}"
            f"{'ROUNDS':<7}"
            f"{'PLAYER':<7}"
        )
        print_section(section_width=SECTION_WIDTH)
        for i, tournament in enumerate(tournaments_list, start=1):
            print(
                f"{str(i):<6}"
                f"{str.capitalize(tournament.get('name', '')):<30}"
                f"{str.capitalize(tournament.get('description', '')):<30}"
                f"{str.capitalize(tournament.get('location', '')):<30}"
                f"{str.capitalize(tournament.get('status', '')):<13}"
                f"{tournament.get('date_begin', ''):<12}"
                f"{tournament.get('date_end', ''):<12}"
                f"{tournament.get('round_actual', '')}/{tournament.get('rounds_max', ''):<7}"
                f"{tournament.get('players_list', '').__len__():<7}"
            )
        if len(tournaments_list) < 2:
            print()
            return
        print_section(section_width=SECTION_WIDTH)
        print(
            "Sort by: default(z), name(a), description(b), location(c), status(d), start date(e), end date(f)"
        )
        print()

    def select_tournaments_to_delete(tournaments_list):
        """This method prompts the user to select tournaments to delete and returns the selected tournaments."""
        if not tournaments_list:
            print("The tournament list is currently empty.")
        num_of_tournaments = len(tournaments_list)
        while True:
            line_nums_input = input(
                f"Enter the line numbers of tournaments to delete (1-{num_of_tournaments}),"
                'separated by commas, or press "Enter" to cancel: '
            )
            if not line_nums_input:
                break
            try:
                lines_numbers = [
                    int(num.strip())
                    for num in line_nums_input.split(",")
                    if int(num) >= 1 and int(num) <= num_of_tournaments
                ]
                lines_numbers = list({item for item in lines_numbers})  # Remove duplicates lines_numbers
                if not lines_numbers:
                    raise ValueError()
                tournaments_list_selected = [
                    tournaments_list[line_number - 1] for line_number in lines_numbers
                ]

                # Display selected tournaments list
                print(
                    "\n"
                    f"{'NAME':<30}"
                    f"{'DESCRIPTION NAME':<30}"
                    f"{'LOCATION':<30}"
                    f"{'STATUS':<15}"
                    f"{'START DATE':<15}"
                )
                for tournament in tournaments_list_selected:
                    print(
                        f"{tournament['name']:<30}"
                        f"{tournament['description']:<30}"
                        f"{tournament['location']:<30}"
                        f"{tournament['status']:<15}"
                        f"{tournament['date_begin']:<15}"
                    )

                return tournaments_list_selected
            except ValueError:
                print(
                    "Invalid input format. Please enter a comma-separated list of"
                    f"integers between 1 and {num_of_tournaments}, e.g. '1, 3, 5'."
                )

    def select_tournaments_to_update(tournaments_list):
        """This method prompts the user to select tournaments to update and returns the selected tournaments."""
        if not tournaments_list:
            print("The tournament list is currently empty.")
        num_of_tournaments = len(tournaments_list)
        while True:
            line_nums_input = input(
                f"Enter the line numbers of tournaments to update (1-{num_of_tournaments}),"
                'separated by commas, or press "Enter" to cancel: '
            )
            if not line_nums_input:
                break
            try:
                # extract the desired line numbers to update, taking only numbers within the range of the list
                lines_numbers = [
                    int(num.strip())
                    for num in line_nums_input.split(",")
                    if int(num) >= 1 and int(num) <= num_of_tournaments
                ]
                lines_numbers = list({item for item in lines_numbers})  # Remove duplicates lines_numbers
                if not lines_numbers:
                    raise ValueError()
                tournaments_selected_to_update = [
                    tournaments_list[line_number - 1] for line_number in lines_numbers
                ]
                return tournaments_selected_to_update
            except ValueError:
                print(
                    "Invalid input format. Please enter a comma-separated list of"
                    f"integers between 1 and {num_of_tournaments}, e.g. '1, 3, 5'."
                )

    def select_tournament(tournaments_list):
        """This method prompts the user to select a tournament and returns the selected tournament."""
        if not tournaments_list:
            print("The tournament list is currently empty.")
            return None
        num_of_tournaments = len(tournaments_list)
        prompt_str = f"Enter the line number of the tournament to select (1-{num_of_tournaments}): "
        while True:
            try:
                line_number = int(input(prompt_str))
                if line_number < 1 or line_number > num_of_tournaments:
                    raise ValueError()
                tournament_selected = tournaments_list[line_number - 1]
                return tournament_selected
            except ValueError:
                print(
                    f"Invalid input format. Please enter an integer between 1 and {num_of_tournaments}."
                )

    def update_tournament(tournament_dic):
        """
        This method prompts the user for input to update a tournament and
        returns an updates the tournament dictionary.
        """
        clear_screen()
        print_section("| Update a tournament |", SECTION_CHAR, SECTION_WIDTH)
        print()

        print(
            f"{'NAME':<30}"
            f"{'DESCRIPTION NAME':<30}"
            f"{'LOCATION':<30}"
            f"{'START DATE':<15}"
            f"{'END DATE':<15}"
            f"{'ROUNDS':<4}"
        )
        print(
            f"{str.capitalize(tournament_dic.get('name', '')):<30}"
            f"{str.capitalize(tournament_dic.get('description', '')):<30}"
            f"{str.capitalize(tournament_dic.get('location', '')):<30}"
            f"{tournament_dic.get('date_begin', ''):<15}"
            f"{tournament_dic.get('date_end', ''):<15}"
            f"{tournament_dic.get('rounds_max', ''):<4}"
        )
        print()

        while True:
            name = (
                input(f"name ({str.capitalize(tournament_dic.get('name', ''))}): ").strip().capitalize()
            )
            if not name:
                tournament_dic["name"] = tournament_dic["name"].strip().capitalize()
                break
            if name and Check.is_string_limit(name):
                tournament_dic["name"] = name
                break
            print(
                "Invalid input for 'name'.\nPlease enter only alphabets, spaces,"
                "appropriate hyphens and up to 60 characters."
            )

        while True:
            description = (
                input(f"description ({str.capitalize(tournament_dic.get('description', ''))}): ")
                .strip().capitalize()
            )
            if not description:
                tournament_dic["description"] = tournament_dic["description"].strip().capitalize()
                break
            if description and Check.is_string_limit(description):
                tournament_dic["description"] = description
                break
            print(
                "Invalid input for 'description'.\nPlease enter only alphabets, spaces,"
                "appropriate hyphens and up to 60 characters."
            )

        while True:
            location = (
                input(f"location ({str.capitalize(tournament_dic.get('location', ''))}): ")
                .strip().capitalize()
            )
            if not location:
                tournament_dic["location"] = tournament_dic["location"].strip().capitalize()
                break
            if location and Check.is_string_limit(location):
                tournament_dic["location"] = location
                break
            print(
                "Invalid input for 'description'.\nPlease enter only alphabets, spaces,"
                "appropriate hyphens and up to 60 characters."
            )

        while True:
            date_begin = input(f"start date ({tournament_dic.get('date_begin', '')}): ")
            if not date_begin:
                break
            if Check.is_valid_date(date_begin):
                tournament_dic["date_begin"] = datetime.strptime(date_begin, "%Y-%m-%d").strftime("%Y-%m-%d")
                break
            print(
                "Invalid date format. Please enter a valid date in yyyy-mm-dd format."
            )

        while True:
            date_end = input(f"end date ({tournament_dic.get('date_end', '')}): ")
            if not date_end:
                break
            if Check.is_valid_date(date_end):
                date_begin = tournament_dic.get('date_begin', '')
                if datetime.strptime(date_end, "%Y-%m-%d") >= datetime.strptime(date_begin, "%Y-%m-%d"):
                    tournament_dic["date_end"] = datetime.strptime(date_end, "%Y-%m-%d").strftime("%Y-%m-%d")
                    break
            print(
                "Invalid date format. Please enter a valid date in yyyy-mm-dd format"
                "that is the same or after the start date."
            )

        while True:
            rounds_max_input = input(
                f"number of rounds ({tournament_dic.get('rounds_max', '')}): "
            ).strip()
            if not rounds_max_input:
                break
            try:
                if 1 <= int(rounds_max_input) <= int(ROUNDS_MAX):
                    tournament_dic["rounds_max"] = rounds_max_input
                    break
                else:
                    print(
                        f"Enter a number between 1 and {int(ROUNDS_MAX)}."
                    )
            except ValueError:
                print("Enter a valid number.")
        print()
        return tournament_dic

    def get_yes_or_no_update_next_tournament():
        """This method getting user input to update the next tournament."""
        while True:
            user_answer = input("Do you want to update the next tournament (y/n)? ").lower()
            if user_answer in ("y", "n"):
                break
            print("please, enter 'y' or 'n'.")
        return user_answer

    def get_yes_or_no_delete_tournaments():
        """This method Getting user input to delete tournaments."""
        while True:
            user_answer = input("\nDo you want to delete selected tournaments (y/n)?").lower()
            if user_answer in ("y", "n"):
                break
            print("please, enter ""y"" or ""n"".")
        return user_answer

    def get_exit_pause():
        """This method getting user input to exit the pause."""
        input("\nPress a key to exit the pause")
