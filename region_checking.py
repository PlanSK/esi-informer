import json
import os

from get_space_locations_data import analyze_yaml_file_data
from parse_id_data_from_yaml import parse_obj_structure
from settings import (
    AMARR_REGION_ID_LIST,
    CALDARI_REGION_ID_LIST,
    CONSTELLATIONS_ID_FILENAME,
    ESI_DATA_DIR,
    GALLENTE_REGION_ID_LIST,
    ITEMS_FILE,
    JSON_CONSTELLATIONS_LIST_FILENAME,
    JSON_REGIONS_LIST_FILENAME,
    JSON_SOLAR_SYSTEMS_LIST_FILENAME,
    MINMATAR_REGION_ID_LIST,
    REGIONS_ID_FILENAME,
    SOLAR_SYSTEM_ID_FILENAME,
    UNIQUE_NAMES_FILE,
)
from utils import decode_yaml

REQUIRED_SDE_FILES_LIST = (UNIQUE_NAMES_FILE, ITEMS_FILE)
REQUIRED_IDS_FILES = (
    REGIONS_ID_FILENAME,
    CONSTELLATIONS_ID_FILENAME,
    SOLAR_SYSTEM_ID_FILENAME,
)
REQUIRED_JSON_FILES_LIST = (
    JSON_REGIONS_LIST_FILENAME,
    JSON_CONSTELLATIONS_LIST_FILENAME,
    JSON_SOLAR_SYSTEMS_LIST_FILENAME,
)


def check_file_exists_list(files_list: list[str]) -> bool:
    return all(
        [
            os.path.exists(os.path.join(ESI_DATA_DIR, filename))
            for filename in files_list
        ]
    )


if check_file_exists_list(REQUIRED_SDE_FILES_LIST):
    if not check_file_exists_list(REQUIRED_IDS_FILES):
        names_file_data = decode_yaml(
            os.path.join(ESI_DATA_DIR, UNIQUE_NAMES_FILE)
        )
        parse_obj_structure(names_file_data)
    if not check_file_exists_list(REQUIRED_JSON_FILES_LIST):
        items_file_data = decode_yaml(os.path.join(ESI_DATA_DIR, ITEMS_FILE))
        analyze_yaml_file_data(items_file_data)
else:
    raise Exception("SDE files not found.")


# Form region dict
with open(os.path.join(ESI_DATA_DIR, JSON_REGIONS_LIST_FILENAME)) as json_file:
    regions_list: list[dict] = json.load(json_file)
regions_data_dict = {
    region.get("id"): region.get("name") for region in regions_list
}
# Form solar system list
with open(
    os.path.join(ESI_DATA_DIR, JSON_SOLAR_SYSTEMS_LIST_FILENAME)
) as json_file:
    solar_system_list: list[dict] = json.load(json_file)
solar_system_data_dict = {
    system.get("name"): system for system in solar_system_list
}

system_list = [
    "98Q-8O",
    "B-9C24",
    "Gultratren",
    "Isie",
    "LSC4-P",
    "M-MD3B",
    "X-7OMU",
    "Meunvon",
    "Sujarento",
    "Tararan",
    "Ahbazon",
    "A-1CON",
    "Adeel",
    "Aedald",
    "Egbinger",
    "G-0Q86",
    "G8AD-C",
    "Goinard",
    "Lantorn",
    "MN5N-X",
    "PVH8-0",
    "QFEW-K",
    "Rakapas",
    "Serpentis Prime",
    "Turnur",
    "Utopia",
    "UW9B-F",
    "XX9-WV",
    "YZ-LQL",
]
default_color_prefix = "\033[0m"

for system_name in system_list:
    system_data = solar_system_data_dict.get(system_name)
    region_name = regions_data_dict.get(system_data.get("region_id"))

    if system_data.get("region_id") in CALDARI_REGION_ID_LIST:
        first_color_prefix = "\033[1;36m"
    elif system_data.get("region_id") in AMARR_REGION_ID_LIST:
        first_color_prefix = "\033[1;33m"
    elif system_data.get("region_id") in GALLENTE_REGION_ID_LIST:
        first_color_prefix = "\033[1;32m"
    elif system_data.get("region_id") in MINMATAR_REGION_ID_LIST:
        first_color_prefix = "\033[1;31m"
    else:
        first_color_prefix = "\033[0m"

    print(
        f"{first_color_prefix}{system_name} located "
        f"in {region_name}.{default_color_prefix}"
    )
