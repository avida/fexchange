import logging
import logging.config
import yaml

LOGGER_CONFIG_FILE = 'config/logger.yaml'

with open(LOGGER_CONFIG_FILE) as conf:
	config = yaml.safe_load(conf.read())
	print(config)
	logging.config.dictConfig(config)

logger = logging.getLogger("fexchange")
