from datetime import datetime
from datetime import timedelta
from utils.utils import clear_screen
from utils.utils import print_section
from utils.utils import limit_str
from utils.utils import Check
from utils.utils import SECTION_CHAR


SECTION_WIDTH = 80


class ViewPlayer:
    """This class represents a menu interface for managing players"""

    def add_player():
        """This method prompts the user for player information and returns the entered values as a tuple."""
        clear_screen()
        print_section("| Add a player |", SECTION_CHAR, 60)
        print()

        while True:
            sex = input("Sex (M/F): ").strip().upper()
            if Check.is_sex(sex):
                break
            print('Please, the input "Sex" must be either "M" or "F".')

        while True:
            first_name = input("First name: ").strip().capitalize()
            if Check.is_name(first_name) and Check.is_string_limit(first_name):
                break
            print(
                "Invalid input for 'First name'.\n"
                "Please enter only alphabets, separator space, appropriate hyphens and up to 60 characters."
            )

        while True:
            last_name = input("Last name: ").strip().capitalize()
            if Check.is_name(last_name) and Check.is_string_limit(last_name):
                break
            print(
                "Invalid input for 'Last name'.\n"
                "Please enter only alphabets, separator space, appropriate hyphens and up to 60 characters."
            )

        while True:
            country_code = input("Country code (3 caracters): ").strip().upper()
            if Check.is_country_code(country_code):
                break
            print("please, enter a correct country code with 3 digits.")

        while True:
            date_of_birth = input("Date of birth (yyyy-mm-dd): ")
            if Check.is_valid_date(date_of_birth):
                date_obj = datetime.strptime(date_of_birth, "%Y-%m-%d")
                if datetime.now() - timedelta(days=36525) < date_obj < datetime.now():
                    date_of_birth = date_obj.strftime("%Y-%m-%d")
                    break
            print(
                "Please enter a valid date of birth (yyyy-mm-dd), and that is no older than 100 years old."
            )

        while True:
            rating = input("Rating: ").strip()
            if Check.is_rating(rating):
                break
            print("please, enter a number between 1 and 4000 max.")

        while True:
            id = input("Id chess: ").strip().upper()
            # check if id is unique and has a valid format
            if Check.is_id_chess(id):
                if not Check.is_id_chess_exists(id):
                    break
                print(
                    "Please, the national chess identifier already exist, enter a unique ID."
                )
            else:
                print(
                    "Please, enter a valid national chess identifier, two letters followed by five digits."
                )
        print("\n")

        rank = "00"

        return sex, first_name, last_name, country_code, date_of_birth, rating, rank, id

    def display_player_details(player_dict):
        """This method displays the details of a player from a dictionary"""
        print()
        print_section("| Player Détails |", SECTION_CHAR, 60)
        print()
        print(
            f"Sex: {player_dict.get('sex', '')}\n"
            f"First name: {str.capitalize(player_dict.get('first_name', ''))}\n"
            f"Last name: {str.upper(player_dict.get('last_name', ''))}\n"
            f"Country code: {player_dict.get('country_code', '')}\n"
            f"Date of birth: {player_dict.get('date_of_birth', '')}\n"
            f"Rating: {player_dict.get('rating', '')}\n"
            f"Id chess: {player_dict.get('id', '')}\n"
        )
        print("This information has been saved in the database.\n")

    def display_players_list(players_list, tournament, file_name):
        """This method displays a list of players with their details."""
        clear_screen()
        if file_name:
            print_section(
                f"| Players List imported: {file_name})|",
                SECTION_CHAR,
            )
        else:
            print_section(
                "| Players List |",
                SECTION_CHAR,
            )
        print()
        if not players_list:
            print("The player list is currently empty.\n")
            return
        print(
            f"{'#':<4}"
            f"{'':<2}"
            f"{'SEX':<4}"
            f"{'FIRST NAME':<30}"
            f"{'LAST NAME':<30}"
            f"{'COUNTRY':<8}"
            f"{'DATE OF BIRTH':<15}"
            f"{'RATING':<8}"
            f"{'RANK':<6}"
            f"{'ID CHESS':<8}"
        )
        print_section()
        for i, player in enumerate(players_list, start=1):
            selected = ""
            if tournament:
                check_id = player.get("id", "") in tournament.players_list
                if check_id:
                    selected = "*"
            print(
                f"{str(i):<4}"
                f"{selected:<2}"
                f"{player.get('sex', ''):<4}"
                f"{limit_str(str.capitalize(player.get('first_name', ''))):<30}"
                f"{limit_str(str.upper(player.get('last_name', ''))):<30}"
                f"{player.get('country_code', ''):<8}"
                f"{player.get('date_of_birth', ''):<15}"
                f"{player.get('rating', ''):<8}"
                f"{player.get('rank', ''):<6}"
                f"{player.get('id', ''):<8}"
            )
        if len(players_list) < 2:
            print()
            return
        print_section()
        print(
            "Sort by: default (z), "
            "sex(a), "
            "first name(b), "
            "last name(c), "
            "country(d), "
            "date of birth(e), "
            "rating(f), "
            "rank(g), "
            "id chess(h)"
        )
        print()

    def select_players_to_delete(players_list):
        """
        This method prompts the user to select players to delete from a list and
        returns the selected players as a list.
        """
        if not players_list:
            print("The player list is currently empty.")
        num_of_players = len(players_list)
        while True:
            line_nums_input = input(
                f"Enter the line numbers to delete (separated by commas) (1-{num_of_players}) or press "
                "Enter"
                " to cancel: "
            )
            if not line_nums_input:
                break
            try:
                # extract the desired lines numbers to delete, "takes numbers only in range"
                lines_numbers = [
                    int(num.strip())
                    for num in line_nums_input.split(",")
                    if int(num) >= 1 and int(num) <= num_of_players
                ]
                lines_numbers = list(
                    {item for item in lines_numbers}
                )  # Remove duplicates lines_numbers
                if not lines_numbers:
                    raise ValueError()
                players_list_selected = [
                    players_list[line_number - 1] for line_number in lines_numbers
                ]

                # Display selected players list
                print(
                    f"\n{'SEX':<6}"
                    f"{'FIRST NAME':<30}"
                    f"{'LAST NAME':<30}"
                    f"{'DATE OF BIRTH':<15}"
                )
                for player in players_list_selected:
                    print(
                        f"{player.get('sex', ''):<6}"
                        f"{str.capitalize(player.get('first_name', '')):<30}"
                        f"{str.upper(player.get('last_name', '')):<30}"
                        f"{player.get('date_of_birth', ''):<15}"
                    )

                return players_list_selected
            except ValueError:
                print(
                    f"Please enter numbers between (1-{num_of_players}) and separated by commas only."
                )

    def select_players_to_update(players_list):
        """
        This method prompts the user to select players to update from a list and
        returns the selected players as a list.
        """
        if not players_list:
            print("The player list is currently empty.")
        num_of_players = len(players_list)
        while True:
            line_nums_input = input(
                f"Enter the line numbers to update (separated by commas) (1-{num_of_players}) or "
                'press "Enter" to cancel: '
            )
            if not line_nums_input:
                break
            try:
                # extract the desired line numbers to update, "takes numbers only in range"
                lines_numbers = [
                    int(num.strip())
                    for num in line_nums_input.split(",")
                    if int(num) >= 1 and int(num) <= num_of_players
                ]
                lines_numbers = list(
                    {item for item in lines_numbers}
                )  # Remove duplicates lines_numbers
                if not lines_numbers:
                    raise ValueError()
                player_list_selected = [
                    players_list[line_number - 1] for line_number in lines_numbers
                ]
                return player_list_selected
            except ValueError:
                print(
                    f"Please enter numbers between (1-{num_of_players}) and separated by commas only."
                )

    def select_players_to_add(players_list):
        """
        This method prompts the user to select players to add to the tournament and
        returns the selected players as a list.
        """
        if not players_list:
            print("The player list is currently empty.")
        num_of_players = len(players_list)
        while True:
            line_nums_input = input(
                f"Enter line numbers to select/deselect players (1-{num_of_players}), separated by commas, or "
                'press "Enter" to cancel: '
            )
            if not line_nums_input:
                break
            try:
                lines_numbers = [
                    int(num.strip())
                    for num in line_nums_input.split(",")
                    if int(num) >= 1 and int(num) <= num_of_players
                ]
                lines_numbers = list(
                    {item for item in lines_numbers}
                )  # Remove duplicates lines_numbers
                if not lines_numbers:
                    raise ValueError()
                players_selected_to_add = [
                    players_list[line_number - 1] for line_number in lines_numbers
                ]
                return players_selected_to_add
            except ValueError:
                print(
                    f"Please enter numbers between (1-{num_of_players}) and separated by commas only."
                )

    def update_player(player_dic):
        """This method prompts the user to update a player's information and returns the updated player dictionary."""
        clear_screen()
        print_section("| Update a player |", SECTION_CHAR, )
        print()
        print(
            f"{'SEX':<6}"
            f"{'FIRST NAME':<30}"
            f"{'LAST NAME':<30}"
            f"{'COUNTRY':<8}"
            f"{'DATE OF BIRTH':<15}"
            f"{'RATING':<8}"
            f"{'RANK':<6}"
            f"{'ID CHESS':<8}"
        )
        print(
            f"{player_dic.get('sex', ''):<6}"
            f"{limit_str(str.capitalize(player_dic.get('first_name', ''))):<30}"
            f"{limit_str(str.upper(player_dic.get('last_name', ''))):<30}"
            f"{player_dic.get('country_code', ''):<8}"
            f"{player_dic.get('date_of_birth', ''):<15}"
            f"{player_dic.get('rating', ''):<8}"
            f"{player_dic.get('rank', ''):<6}"
            f"{player_dic.get('id', ''):<8}"
        )
        print("\n")

        while True:
            sex = input(f"Sex ({player_dic.get('sex', '')}): ").strip().upper()
            if not sex:
                break
            if Check.is_sex(sex):
                player_dic["sex"] = sex
                break
            print('Please, the input "Sex" must be either "M" or "F".')

        while True:
            first_name = (
                input(
                    f"First name ({str.capitalize(player_dic.get('first_name', ''))}): "
                )
                .strip()
                .capitalize()
            )
            if not first_name:
                player_dic["first_name"] = player_dic["first_name"].strip().capitalize()
                break
            if Check.is_name(first_name) and Check.is_string_limit(first_name):
                player_dic["first_name"] = first_name
                break
            print(
                "Invalid input for 'First name'.\n"
                "Please enter only alphabets, separator space, appropriate hyphens and up to 60 characters."
            )

        while True:
            last_name = (
                input(f"Last name ({str.upper(player_dic.get('last_name', ''))}): ")
                .strip()
                .capitalize()
            )
            if not last_name:
                player_dic["last_name"] = player_dic["last_name"].strip().capitalize()
                break
            if Check.is_name(last_name) and Check.is_string_limit(last_name):
                player_dic["last_name"] = last_name
                break
            print(
                "Invalid input for 'First name'.\n"
                "Please enter only alphabets, separator space, appropriate hyphens and up to 60 characters."
            )

        while True:
            country_code = (
                input(f"Country code ({player_dic.get('country_code', '')}): ")
                .strip()
                .upper()
            )
            if not country_code:
                player_dic["country_code"] = player_dic["country_code"].strip().upper()
                break
            if Check.is_country_code(country_code):
                player_dic["country_code"] = country_code
                break
            print("please, enter a correct country code with 3 digits.")

        while True:
            date_of_birth = input(
                f"Date of birth ({player_dic.get('date_of_birth', '')}): "
            )
            if not date_of_birth:
                break
            if Check.is_valid_date(date_of_birth):
                date_obj = datetime.strptime(date_of_birth, "%Y-%m-%d")
                if datetime.now() - timedelta(days=36525) < date_obj < datetime.now():
                    player_dic["date_of_birth"] = date_obj.strftime("%Y-%m-%d")
                    break
            print(
                "Please enter a valid date of birth (yyyy-mm-dd), and that is no older than 100 years old."
            )

        while True:
            rating = input(f"Rating ({player_dic.get('rating', '')}): ").strip()
            if not rating:
                break
            if Check.is_rating(rating):
                player_dic["rating"] = rating
                break
            print("please, enter a number between 1 and 4000 max.")

        while True:
            id = input(f"Id chess ({player_dic.get('id', '')}): ").strip().upper()
            if not id:
                player_dic["id"] = player_dic["id"].strip().upper()
                break
            # checks if the id is unique apart from the current id and has a valid format
            if Check.is_id_chess(id):
                if not Check.is_id_chess_exists(id) or player_dic["id"] == id:
                    player_dic["id"] = id
                    break
                print(
                    "Please, the national chess identifier already exist, enter a unique ID."
                )
            else:
                print(
                    "Please, enter a valid national chess identifier, two letters followed by five digits."
                )
        print()
        return player_dic

    def get_yes_or_no_update_next_player():
        """This method prompts prompts the user for a yes or no for updating the next player and returns the answer."""
        message = "Do you want to update the next player (y/n)?"
        return ViewPlayer.get_yes_or_no(message)

    def get_yes_or_no_delete_players():
        """This method prompts the user for a yes or no for deleting selected players and returns the answer."""
        message = "\nDo you want to delete selected players (y/n)?"
        return ViewPlayer.get_yes_or_no(message)

    def get_yes_or_no_add_another_player():
        """This method Prompts the user for a yes or no afor adding another player and returns the answer."""
        message = "Do you want to add another player (y/n)?"
        return ViewPlayer.get_yes_or_no(message)

    def get_yes_or_no(message):
        """This method prompts the user for a yes or no answer to a given message and returns the answer."""
        while True:
            user_answer = input(message).lower()
            if user_answer in ("y", "n"):
                break
            print("please, enter " "y" " or " "n" ".")
        return user_answer

    def get_continue():
        """This method prompts the user to press a key to continue."""
        input("\nPress a key to exit the pause.")
