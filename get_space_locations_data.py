import json
import os
from dataclasses import asdict, dataclass

from settings import (
    CONSTELLATIONS_ID_FILENAME,
    ESI_DATA_DIR,
    ITEMS_FILE,
    JSON_CONSTELLATIONS_LIST_FILENAME,
    JSON_REGIONS_LIST_FILENAME,
    JSON_SOLAR_SYSTEMS_LIST_FILENAME,
    REGIONS_ID_FILENAME,
    SOLAR_SYSTEM_ID_FILENAME,
    logger,
)
from utils import decode_yaml, write_json


@dataclass
class GroupData:
    json_file_name: str
    group_id: int
    parsed_list: list


@dataclass
class RegionData:
    id: int
    name: str
    included_constellation_id_list: list[int]


@dataclass
class ConstellationData:
    id: int
    name: str
    region_id: int
    included_solar_systems_id_list: list[int]


@dataclass
class SolarSystemData:
    id: int
    name: str
    constellation_id: int
    region_id: int


def get_regions_dict() -> dict:
    logger.info("Get regions info from file.")
    with open(os.path.join(ESI_DATA_DIR, REGIONS_ID_FILENAME)) as json_file:
        region_dicts_list: list[dict] = json.load(json_file)

    regions_dict = {
        region.get("id"): RegionData(
            id=region.get("id"),
            name=region.get("item_name"),
            included_constellation_id_list=[],
        )
        for region in region_dicts_list
    }

    return regions_dict


def get_constellation_dict() -> dict:
    logger.info("Get constellations info from file.")
    with open(
        os.path.join(ESI_DATA_DIR, CONSTELLATIONS_ID_FILENAME)
    ) as json_file:
        constellation_dicts_list: list[dict] = json.load(json_file)

    constellation_dict = {
        constellation.get("id"): ConstellationData(
            id=constellation.get("id"),
            name=constellation.get("item_name"),
            region_id=0,
            included_solar_systems_id_list=[],
        )
        for constellation in constellation_dicts_list
    }

    return constellation_dict


def get_solar_system_dict() -> dict:
    logger.info("Get solar systems info from file.")
    with open(
        os.path.join(ESI_DATA_DIR, SOLAR_SYSTEM_ID_FILENAME)
    ) as json_file:
        solar_systems_dicts_list: list[dict] = json.load(json_file)

    solar_system_dict = {
        solar_system.get("id"): SolarSystemData(
            id=solar_system.get("id"),
            name=solar_system.get("item_name"),
            constellation_id=0,
            region_id=0,
        )
        for solar_system in solar_systems_dicts_list
    }

    return solar_system_dict


def analyze_yaml_file_data(yaml_data: list[dict]):
    regions_dict = get_regions_dict()
    constellations_dict = get_constellation_dict()
    solar_system_dict = get_solar_system_dict()
    logger.info("Try parsing location data.")
    for item in yaml_data:
        if item.get("itemID") in solar_system_dict.keys():
            solar_system_dict[item.get("itemID")].constellation_id = item.get(
                "locationID"
            )
            constellations_dict[
                item.get("locationID")
            ].included_solar_systems_id_list.append(item.get("itemID"))
        elif item.get("itemID") in constellations_dict.keys():
            constellations_dict[item.get("itemID")].region_id = item.get(
                "locationID"
            )
            regions_dict[
                item.get("locationID")
            ].included_constellation_id_list.append(item.get("itemID"))
    logger.info("Load regions info to solar system dict.")
    for _, solar_system in solar_system_dict.items():
        try:
            region_id = constellations_dict[
                solar_system.constellation_id
            ].region_id
        except KeyError:
            region_id = 0
        else:
            solar_system.region_id = region_id
    logger.info("Done. Writing json files.")
    write_json(
        os.path.join(ESI_DATA_DIR, JSON_REGIONS_LIST_FILENAME),
        [asdict(region) for _, region in regions_dict.items()],
    )
    write_json(
        os.path.join(ESI_DATA_DIR, JSON_CONSTELLATIONS_LIST_FILENAME),
        [asdict(const) for _, const in constellations_dict.items()],
    )
    write_json(
        os.path.join(ESI_DATA_DIR, JSON_SOLAR_SYSTEMS_LIST_FILENAME),
        [asdict(system) for _, system in solar_system_dict.items()],
    )
    logger.info("Extraction data from yaml file successfully completed.")


if __name__ == "__main__":
    loaded_yaml = decode_yaml(os.path.join(ESI_DATA_DIR, ITEMS_FILE))
    analyze_yaml_file_data(loaded_yaml)
