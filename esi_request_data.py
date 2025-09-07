import http.client
import json

CONNECTION = http.client.HTTPSConnection("esi.evetech.net")
DEFAULT_HEADER = {
    "Accept-Language": "",
    "If-None-Match": "",
    "X-Compatibility-Date": "2020-01-01",
    "X-Tenant": "",
    "Accept": "application/json",
}


def get_esi_request_data_dict(
    url: str,
    method: str = "GET",
    headers: dict = DEFAULT_HEADER,
    connection: http.client.HTTPSConnection = CONNECTION,
    payload: list | None = None,
):
    connection.request(method=method, url=url, headers=headers, body=payload)
    http_response = connection.getresponse()
    if http_response.status == 200:
        data = http_response.read()
        return json.loads(data.decode("utf-8"))
    raise


def get_esi_ids_by_name(item_names_list: list) -> dict:
    names_str = ", ".join(f'"{item}"' for item in item_names_list)
    payload = f"[\n  {names_str}\n]"

    headers = DEFAULT_HEADER
    headers["Content-Type"] = "application/json"

    requested_dict = get_esi_request_data_dict(
        connection=CONNECTION,
        headers=headers,
        method="POST",
        url="/universe/ids",
        payload=payload,
    )

    return requested_dict


def get_solar_system_info(system_id: int):
    system_data_dict = get_esi_request_data_dict(
        f"/universe/systems/{system_id}"
    )
    constellation_id = system_data_dict.get("constellation_id", 0)

    connstelation_data_dict = get_esi_request_data_dict(
        f"/universe/constellations/{constellation_id}"
    )
    region_id = connstelation_data_dict.get("region_id", 0)
    region_data_dict = get_esi_request_data_dict(
        f"/universe/regions/{region_id}"
    )
    print(
        f'The system {system_data_dict.get("name")} / '
        f'{connstelation_data_dict.get("name")} / '
        f'{region_data_dict.get("name")}.'
    )


if __name__ == "__main__":
    solar_systems_names_list = ["Ragnarg", "Mai", "Rancer"]
    esi_search_result_dict = get_esi_ids_by_name(solar_systems_names_list)

    for system_info_dict in esi_search_result_dict.get("systems"):
        get_solar_system_info(system_info_dict.get("id"))
