import os
from dotenv import load_dotenv
from pathlib import Path


class Config:

    def __init__(self):
        env_file = Path(".env")
        if env_file.is_file():
            load_dotenv(dotenv_path=".env")
        self.providers_dict = self.read_providers_from_env()

    def notifier_enabled(self):
        return os.environ['NOTIFIER_ENABLED'] == "1"

    def notifier_token(self):
        return os.environ['NOTIFIER_TOKEN']

    def notifier_message(self):
        return os.environ['NOTIFIER_MESSAGE']

    def notifier_chat_id(self):
        return os.environ['NOTIFIER_CHAT_ID']

    def database_store(self):
        return os.environ['DATABASE_STORE']

    def heroku_app_name(self):
        return os.environ['HEROKU_APP_NAME']

    def providers(self):
        return self.providers_dict

    def read_providers_from_env(self):
        # Filter provider keys
        provider_keys = {}
        for env_var_name, env_var_value in os.environ.items():
            if env_var_name.startswith("PROVIDER"):
                provider_keys[env_var_name] = env_var_value

        # Iterate over keys by provider number, and fill out provider objects
        i = 1
        providers_dict = {}
        while f"PROVIDER{i}_NAME" in provider_keys:
            if provider_keys[f"PROVIDER{i}_ENABLED"] != "1":
                i += 1
                continue
            j = 1
            sources = []
            while f"PROVIDER{i}_S{j}" in provider_keys:
                sources.append(provider_keys[f"PROVIDER{i}_S{j}"])
                j += 1
            provider = {
                'base_url': provider_keys[f"PROVIDER{i}_BASE_URL"],
                'sources': sources
            }
            if f"PROVIDER{i}_TIMEOUT" in provider_keys:
                provider['timeout'] = float(
                    provider_keys[f"PROVIDER{i}_TIMEOUT"])
            providers_dict[provider_keys[f"PROVIDER{i}_NAME"]] = provider
            i += 1

        return providers_dict
