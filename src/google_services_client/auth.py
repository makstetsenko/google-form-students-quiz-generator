from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.app_env import get_app_env

SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
]


def get_forms_service():
    app_env = get_app_env()

    credentials = None

    if app_env.google_services_client_token_path.exists():
        credentials = Credentials.from_authorized_user_file(
            app_env.google_services_client_token_path,
            SCOPES,
        )

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                app_env.google_services_client_secret_json_path,
                SCOPES,
            )

            credentials = flow.run_local_server(port=0)

        app_env.google_services_client_token_path.write_text(
            credentials.to_json(),
            encoding="utf-8",
        )

    return build(
        "forms",
        "v1",
        credentials=credentials,
    )
