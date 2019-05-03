import configparser, os
import logging.config
import yaml

def setup_logging():
	path = os.path.join('conf', 'logging.yaml')
	env_key = os.getenv('LOG_CFG', None)
	if env_key:
		path = env_key
	if os.path.exists(path):
		with open(path, 'rt') as f:
			config = yaml.safe_load(f.read())
		logging.config.dictConfig(config)
	else:
		logging.basicConfig(level=default_level)

def get_scrapper_config():
	config = configparser.ConfigParser()
	dir_path = os.path.dirname(os.path.realpath(__file__))
	path = os.path.join(dir_path, '..', 'conf', 'config.ini')
	config.read(path)

	return config

def get_pattern_matcher_config():
	config = configparser.ConfigParser()
	dir_path = os.path.dirname(os.path.realpath(__file__))
	path = os.path.join(dir_path, '..', '..', '..', 'conf', 'config.ini')
	config.read(path)

	input = config._sections['INPUT']
	measurement = config._sections['MEASUREMENT']

	return {'input': input,
			'measurement': measurement}