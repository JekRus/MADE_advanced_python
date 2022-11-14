import logging
import logging.config
import yaml


def init_logger(config: str, name: str) -> logging.Logger:
    with open(config, "r") as f_in:
        dict_config = yaml.safe_load(f_in)
    logging.config.dictConfig(dict_config)
    logger = logging.getLogger(name)
    return logger
