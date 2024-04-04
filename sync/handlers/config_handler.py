import os
import configparser

class ConfigHandler:
    def __init__(self, config_file=None):
        if config_file is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # get parent directory
            config_file = os.path.join(base_dir, 'config', 'config.ini')  # adjust path
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        self.config.read(self.config_file)

    def get_config(self):
        return self.config

    def get_section(self, section):
        return self.config[section]

    def get_value(self, section, key):
        try:
            return self.config[section][key]
        except KeyError:
            raise Exception(f"La clave '{key}' no se encuentra en la sección '{section}' del archivo de configuración.")