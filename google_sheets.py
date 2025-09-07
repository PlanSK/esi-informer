import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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

    try:
        service = build("sheets", "v4", credentials=creds)

        result = (
            service.spreadsheets()
            .values()
            .get(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range="Cyno Assets Regions!B2:C2",
            )
            .execute()
        )
        rows = result.get("values", [])
        print(f"{len(rows)} rows retrieved")
        print(result)
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == "__main__":
    main()
