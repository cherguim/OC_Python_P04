import platform
import subprocess
import re
from datetime import datetime
from models.players_model import Player

SECTION_WIDTH = 160
SECTION_CHAR = "="

PATTERN_NAME = re.compile(r"^[A-Za-z]+(?:[\s-][A-Za-z]+)*$")

PATTERN_ID_CHESS = re.compile(r"^[A-Z]{2}\d{5}$")

COUNTRY_CODE = {"AFG", "ALB", "DZA", "ASM", "AND", "AGO", "AIA", "ATA", "ATG", "ARG",
                "ARM", "ABW", "AUS", "AUT", "AZE", "BHS", "BHR", "BGD", "BRB", "BLR",
                "BEL", "BLZ", "BEN", "BMU", "BTN", "BOL", "BIH", "BWA", "BRA", "IOT",
                "VGB", "BRN", "BGR", "BFA", "MMR", "BDI", "KHM", "CMR", "CAN", "CPV",
                "CYM", "CAF", "TCD", "CHL", "CHN", "CXR", "CCK", "COL", "COM", "COG",
                "COD", "COK", "CRI", "HRV", "CUB", "CUW", "CYP", "CZE", "DNK", "DJI",
                "DMA", "DOM", "TLS", "ECU", "EGY", "SLV", "GNQ", "ERI", "EST", "ETH",
                "FLK", "FRO", "FJI", "FIN", "FRA", "PYF", "GAB", "GMB", "GEO", "DEU",
                "GHA", "GIB", "GRC", "GRL", "GRD", "GUM", "GTM", "GGY", "GIN", "GNB",
                "GUY", "HTI", "HND", "HKG", "HUN", "ISL", "IND", "IDN", "IRN", "IRQ",
                "IRL", "IMN", "ISR", "ITA", "CIV", "JAM", "JPN", "JEY", "JOR", "KAZ",
                "KEN", "KIR", "XKX", "KWT", "KGZ", "LAO", "LVA", "LBN", "LSO", "LBR",
                "LBY", "LIE", "LTU", "LUX", "MAC", "MKD", "MDG", "MWI", "MYS", "MDV",
                "MLI", "MLT", "MHL", "MRT", "MUS", "MYT", "MEX", "FSM", "MDA", "MCO",
                "MNG", "MNE", "MSR", "MAR", "MOZ", "NAM", "NRU", "NPL", "NLD", "ANT",
                "NCL", "NZL", "NIC", "NER", "NGA", "NIU", "MNP", "PRK", "NOR", "OMN",
                "PAK", "PLW", "PSE", "PAN", "PNG", "PRY", "PER", "PHL", "PCN", "POL",
                "PRT", "PRI", "QAT", "REU", "ROU", "RUS", "RWA", "BLM", "WSM", "SMR",
                "STP", "SAU", "SEN", "SRB", "SYC", "SLE", "SGP", "SXM", "SVK", "SVN",
                "SLB", "SOM", "ZAF", "KOR", "SSD", "ESP", "LKA", "SHN", "KNA", "LCA",
                "MAF", "SPM", "VCT", "SDN", "SUR", "SJM", "SWZ", "SWE", "CHE", "SYR",
                "TWN", "TJK", "TZA", "THA", "TGO", "TKL", "TON", "TTO", "TUN", "TUR",
                "TKM", "TCA", "TUV", "ARE", "UGA", "GBR", "UKR", "URY", "USA", "UZB",
                "VUT", "VAT", "VEN", "VNM", "VIR", "WLF", "ESH", "YEM", "ZMB", "ZWE"}


def clear_screen():
    if platform.system() == "Windows":
        subprocess.run("cls", shell=True)
    elif platform.system() == "Darwin" or "Linux":
        subprocess.run("clear", shell=True)


def print_section(title="", section_char="=", section_width=125):
    """print a section for views with title or not."""
    section = f"{section_char*5}{title}{section_char*5}" if title else section_char * section_width
    padding = max(0, section_width - len(section))
    section += f"{section_char}" * padding
    print(section)


def serializations(object_list):
    """ Serialisation of objects list -> list of dict"""
    list_dict = []
    for object_ in object_list:
        list_dict.append(object_.__dict__)
    return list_dict


# Vérifier si cette fonction est utilisé!


def limit_str(input_str, nb_car=26):
    if (len(input_str)) > nb_car:
        input_str = input_str[:nb_car] + "..."
    return input_str


class Check:
    def is_id_chess(id_chess):
        return bool(PATTERN_ID_CHESS.match(id_chess))

    def is_id_chess_exists(id_chess):
        return id_chess in [player.id for player in Player().load_all()]

    def is_rating(rating):
        return rating.isnumeric() and 0 < int(rating) <= 4000

    def is_sex(sex):
        return sex.upper() in ["M", "F"]

    def is_name(first_name):
        return bool(PATTERN_NAME.match(first_name))

    def is_valid_date(date_str):
        """Check if the given string can be converted to a valid date."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def is_string_limit(input_str, limit=60):
        return len(input_str) <= limit

    def is_country_code(check_country_code):
        return check_country_code in COUNTRY_CODE
