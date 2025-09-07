from loguru import logger

logger.add(
    "debug_parsing.log", format="{time}: {level} {message}", level="INFO"
)

ESI_DATA_DIR = ".esi_data"
UNIQUE_NAMES_FILE = "invUniqueNames.yaml"
ITEMS_FILE = "invItems.yaml"

REGIONS_ID_FILENAME = "region_ids.json"
CONSTELLATIONS_ID_FILENAME = "constellation_ids.json"
SOLAR_SYSTEM_ID_FILENAME = "solar_system_ids.json"

JSON_REGIONS_LIST_FILENAME = "regions_data.json"
JSON_CONSTELLATIONS_LIST_FILENAME = "constellation_data.json"
JSON_SOLAR_SYSTEMS_LIST_FILENAME = "solar_systems_data.json"

AMARR_REGION_ID_LIST = [
    10000054,
    10000065,
    10000052,
    10000043,
    10000049,
    10000020,
    10000036,
    10000038,
    10000067,
]
MINMATAR_REGION_ID_LIST = [10000042, 10000030, 10000028, 10000001]
CALDARI_REGION_ID_LIST = [10000033, 10000016, 10000069, 10000002]
GALLENTE_REGION_ID_LIST = [
    10000048,
    10000064,
    10000068,
    10000044,
    10000037,
    10000032,
]
