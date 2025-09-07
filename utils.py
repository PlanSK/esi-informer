import yaml
import json
import os

from settings import logger


def decode_yaml(file_name: str) -> list[dict]:
    logger.info(f"Get data from yaml file {file_name}.")
    with open(file_name) as yaml_file:
        parsed_file: list[dict] = yaml.safe_load(yaml_file)
    return parsed_file


def write_json(file_name: str, writeble_data: list):
    logger.info(f"Try to write {file_name}.")
    with open(os.path.join(file_name), "w", encoding="utf-8") as json_file:
        json.dump(writeble_data, fp=json_file, indent=4, ensure_ascii=False)
    logger.info(f"{file_name} has been written.")
