from flask import Flask
import argparse

import socket
import signal
import tornado
import threading

from web_scrapper.utils.utils import *
from web_scrapper.scrapper.scrapper import scrapper
from web_scrapper.controller.scrapper_controller import scrapper_controller
from pattern_matcher.controller.pattern_matcher_controller import pattern_matcher_controller
from web_scrapper.websocket.ws_server import *

app = Flask(__name__)

# Setup logging config
setup_logging()
CONFIG = get_scrapper_config()
LOGGER = logging.getLogger(__name__)

def start_server(args):
	if bool(args.websocket):
		start_websocket_server(bool(args.logging))

	backend_api_thread = threading.Thread(target=start_api_server, args=[args,])
	backend_api_thread.start()

def start_api_server(args):
	if bool(args.scraper):
		app.register_blueprint(scrapper_controller, url_prefix='/api/v0/scraper')
	if bool(args.matcher):
		app.register_blueprint(pattern_matcher_controller, url_prefix='/api/v0/matcher')
	
	app.run(host=CONFIG['SERVER']['HOST'], 
			port=CONFIG['SERVER']['PORT'], 
			threaded=True,
			debug=False)

def start_websocket_server(is_logging):
	ws_ip = CONFIG['WEBSOCKET_SERVER']['HOST']
	ws_route = CONFIG['WEBSOCKET_SERVER']['ROUTE']
	ws_port = CONFIG['WEBSOCKET_SERVER']['PORT']

	application = WSServer([(ws_route, WSHandler)])
	application.listen(ws_port)

	LOGGER.info('Websocket Server Started at ws://{}:{}{}'.format(ws_ip, ws_port, ws_route))
	scrapper_thread = threading.Thread(target=application.scrape, args=[is_logging])
	tornado_thread = threading.Thread(target=tornado.ioloop.IOLoop.instance().start)
	
	scrapper_thread.start()
	tornado_thread.start()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Stock news webscrapper & sentiment analysis')
	parser.add_argument('--websocket', metavar='WEBSOCKET', default=1, type=int, help='Determine if websocket for auto_scraper module will be started')
	parser.add_argument('--scraper', metavar='SCRAPPER', default=1, type=int, help='Determine if scraper module will be started')
	parser.add_argument('--matcher', metavar='MATCHER', default=1, type=int, help='Determine if pattern matcher module will be started')
	parser.add_argument('--logging', metavar='LOGGING', default=0, type=int, help='Log scrapping outputs into logs/*.json')
	args = parser.parse_args()

	# Start service
	start_server(args)