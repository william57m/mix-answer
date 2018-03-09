import configparser
import io
import os


def parse_config(config_file, overwrites_enabled=True):
    config = configparser.ConfigParser(os.environ)
    config_files = [config_file]
    if overwrites_enabled:
        config_files.append(config_file + ".overwrites")
    source_files = config.read(config_files)
    config.set("DEFAULT", "_sourcefiles_", ";".join(source_files))
    return config
