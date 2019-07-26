import json
import logging


class CSVConverter:
    def __init__(self, config_json=None, config_file=None, config_dict=None):
        self.config = config_dict if config_json else json.loads(config_json) if config_json else None
        if not self.config:
            with open(config_file) as json_file:
                self.config = json.load(json_file)
        assert self.config
        logging.debug(f"Using config: {self.config}")


