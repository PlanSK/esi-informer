import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SAMPLE_SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]


def organize_creds():
    creds = None
    if os.path.exists(".secrets/token.json"):
        creds = Credentials.from_authorized_user_file(
            ".secrets/token.json", SCOPES
        )
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                ".secrets/secret.json", SCOPES
            )
            creds = flow.run_local_server(port=37817)
        with open(".secrets/token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_range_values(spreadsheet_id: str, range: str):
    creds = organize_creds()
    try:
        service = build("sheets", "v4", credentials=creds)

        result = (
            service.spreadsheets()
            .values()
            .get(
                spreadsheetId=spreadsheet_id,
                range=range,
            )
            .execute()
        )
        rows = result.get("values", [])
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
    else:
        return rows


def update_range_values(spreadsheet_id, range, value_input_option, _values):
    creds = organize_creds()
    try:
        service = build("sheets", "v4", credentials=creds)
        values = [
            [
                # Cell values ...
            ],
            # Additional rows ...
        ]
        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == "__main__":
    print(get_range_values(SAMPLE_SPREADSHEET_ID, "Cyno Assets List!A1:C40"))
