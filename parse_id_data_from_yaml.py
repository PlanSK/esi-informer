import os
from dataclasses import dataclass

from settings import esi_data_dir, logger, unique_names_file, regions_id_filename, constellations_id_filename, solar_system_id_filename
from utils import decode_yaml, write_json


@dataclass
class GroupData:
    json_file_name: str
    group_id: int
    parsed_list: list


regions_data = GroupData(
    json_file_name=regions_id_filename, group_id=3, parsed_list=[]
)
constellations_data = GroupData(
    json_file_name=constellations_id_filename, group_id=4, parsed_list=[]
)
solar_systems_data = GroupData(
    json_file_name=solar_system_id_filename, group_id=5, parsed_list=[]
)


def append_dict_to_list(item_data: dict, group: GroupData):
    try:
        included_dict = {
            "id": item_data["itemID"],
            "item_name": item_data["itemName"],
        }
    except KeyError as exception:
        logger.error(f"Key error in {id}. Key: {exception}.")
    else:
        group.parsed_list.append(included_dict)


def parse_obj_structure(parsed_data: list[dict]) -> None:
    logger.info("Parsing object structure")
    tuple_to_write = (regions_data, constellations_data, solar_systems_data)
    for item in parsed_data:
        for group in tuple_to_write:
            if item["groupID"] == group.group_id:
                append_dict_to_list(item, group)
    logger.info("Dump and write json files.")
    for group in tuple_to_write:
        write_json(
            os.path.join(esi_data_dir, group.json_file_name), group.parsed_list
        )
    logger.info("End of the parsing.")


if __name__ == "__main__":
    result_data = decode_yaml(os.path.join(esi_data_dir, unique_names_file))
    parse_obj_structure(result_data)
