from loguru import logger

logger.add(
    "debug_parsing.log", format="{time}: {level} {message}", level="INFO"
)

esi_data_dir = ".esi_data"
unique_names_file = "invUniqueNames.yaml"
items_file = "invItems.yaml"

regions_id_filename = "region_ids.json"
constellations_id_filename = "constellation_ids.json"
solar_system_id_filename = "solar_system_ids.json"

json_regions_list_filename = "regions_data.json"
json_constellations_list_filename = "constellation_data.json"
json_solar_systems_list_filename = "solar_systems_data.json"
