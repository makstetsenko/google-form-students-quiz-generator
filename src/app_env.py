import os
import pathlib

from dotenv import load_dotenv
from pydantic import BaseModel


class AppEnv(BaseModel):
    google_services_client_secret_json_path: pathlib.Path
    google_services_client_token_path: pathlib.Path


class EnvStore(BaseModel):
    app_env: AppEnv | None


ENV_STORE = EnvStore(app_env=None)


def get_path(env_name: str) -> pathlib.Path:
    env_value = os.getenv(env_name)

    if env_value is None or env_value == "":
        raise ValueError(f"{env_name} is required")

    return pathlib.Path(env_value)


def get_app_env() -> AppEnv:
    global ENV_STORE

    if ENV_STORE is None:
        ENV_STORE = EnvStore(app_env=None)

    if ENV_STORE.app_env is not None:
        return ENV_STORE.app_env

    load_dotenv()

    app_env = AppEnv(
        google_services_client_secret_json_path=get_path("GOOGLE_SERVICES_CLIENT_SECRET_JSON_PATH"),
        google_services_client_token_path=get_path("GOOGLE_SERVICES_CLIENT_TOKEN_PATH"),
    )

    ENV_STORE.app_env = app_env

    return app_env
