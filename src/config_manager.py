import configparser
import os

class ConfigManager:
    def __init__(self, config_path: str = None):
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, 'config', 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    @property
    def url(self) -> str:
        return self.config['DEFAULT'].get('url', 'https://www.stocktitan.net')

    @property
    def time_zone(self) -> str:
        return self.config['DEFAULT'].get('time_zone', 'Europe/Berlin')
