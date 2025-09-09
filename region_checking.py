import json
import os
import random

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


def get_regions_data_dict() -> dict:
    with open(
        os.path.join(ESI_DATA_DIR, JSON_REGIONS_LIST_FILENAME)
    ) as json_file:
        regions_list: list[dict] = json.load(json_file)
    regions_data_dict = {
        region.get("id"): region.get("name") for region in regions_list
    }
    return regions_data_dict


def get_constellations_data_dict() -> dict:
    with open(
        os.path.join(ESI_DATA_DIR, JSON_CONSTELLATIONS_LIST_FILENAME)
    ) as json_file:
        constellations_list: list[dict] = json.load(json_file)
    constellations_data_dict = {
        constellation.get("id"): constellation.get("name")
        for constellation in constellations_list
    }
    return constellations_data_dict


def get_solar_system_data_dict() -> dict:
    with open(
        os.path.join(ESI_DATA_DIR, JSON_SOLAR_SYSTEMS_LIST_FILENAME)
    ) as json_file:
        solar_system_list: list[dict] = json.load(json_file)
    solar_system_data_dict = {
        system.get("name"): system for system in solar_system_list
    }
    return solar_system_data_dict


def get_region_name_by_id(region_id: int) -> str:
    return get_regions_data_dict().get(region_id, "")


def get_solar_system_data(system_name: str) -> dict:
    solar_system_dict = get_solar_system_data_dict().get(system_name)
    if not solar_system_dict:
        raise NameError(f"{system_name} not found.")
    return solar_system_dict


def get_solar_system_names_with_region_id(
    solar_systems_list: list[str],
) -> list[tuple]:
    system_regions_list = []
    for solar_system_name in solar_systems_list:
        try:
            system_data = get_solar_system_data(solar_system_name)
        except NameError:
            continue
        else:
            system_regions_list.append(
                (solar_system_name, system_data.get("region_id"))
            )
    return system_regions_list


def console_color_output_systems_list(systems_list: list) -> None:
    default_color_prefix = "\033[0m"
    for system_name, region_id in get_solar_system_names_with_region_id(
        systems_list
    ):
        if region_id in CALDARI_REGION_ID_LIST:
            first_color_prefix = "\033[1;36m"
        elif region_id in AMARR_REGION_ID_LIST:
            first_color_prefix = "\033[1;33m"
        elif region_id in GALLENTE_REGION_ID_LIST:
            first_color_prefix = "\033[1;32m"
        elif region_id in MINMATAR_REGION_ID_LIST:
            first_color_prefix = "\033[1;31m"
        else:
            first_color_prefix = "\033[0m"
        print(
            f"{first_color_prefix}{system_name} located "
            f"in {get_region_name_by_id(region_id)}.{default_color_prefix}"
        )


if __name__ == "__main__":
    console_color_output_systems_list(
        random.choices([*get_solar_system_data_dict().keys()], k=5)
    )
