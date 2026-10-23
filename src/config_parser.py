import json
import os


class ConfigParser:
    """Loads and validates the scraper's JSON configuration."""

    def __init__(self, config_path):
        self.config_path = config_path

    def load_config(self):
        if not os.path.isfile(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as file:
            config = json.load(file)

        required_fields = [
            "start_url",
            "pagination_selector",
            "item_container_selector",
            "item_data_selectors",
        ]
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required config field: {field}")

        selectors = config["item_data_selectors"]
        if not isinstance(selectors, dict) or not selectors.get("name") or not selectors.get("price"):
            raise ValueError("item_data_selectors must contain non-empty 'name' and 'price' selectors.")

        print(f"Configuration loaded: {self.config_path}")
        print("Configuration validated.")
        return config
