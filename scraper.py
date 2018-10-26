import time
import psycopg2
import krakenex
import logging.config
from requests import HTTPError, ConnectionError

from db_config import DATABASE
from config import PAIRS, LOGGING


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('scraper')


def get_last_update_time(pair):
	"""Look up unix timestamp of last scrape event.

	Parameters
	----------
	pair : str
		Crypto pair for which last scrape event time is queried.

	Returns
	-------
	int
		Unix timestamp of data scrape event. 0 if not found.

	"""

	conn = None
	update_time = 0
	query = """
		SELECT max(time) FROM ohlc
		WHERE pair = %s;
	"""

	try:
		conn = psycopg2.connect(**DATABASE)
		cursor = conn.cursor()
		cursor.execute(query, (pair,))
		response = cursor.fetchone()
		cursor.close()
		update_time = response[0]
		logger.info("Found last update time=%s for pair=%s.", update_time, pair)
	except (psycopg2.DatabaseError, IndexError):
		logger.error("Failed getting last update time for pair %s.", pair)
	finally:
		if conn:
			conn.close()

	return update_time


def db_insert(data, pair):
	"""Insert ohlc data for given currency pair into database.

	Parameters
	----------
	data : list of list
		List of ohlc data lists as returned from the kraken API.
	pair :  str
		Crypto pair for which insert is performed.

	"""

	conn = None
	insert_statement = """
		INSERT INTO ohlc (pair, time, open, high, low, close, vwap, volume, count)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
	"""

	for row in data:
		row.insert(0, pair)  # add pair label to data

	try:
		conn = psycopg2.connect(**DATABASE)
		cursor = conn.cursor()
		cursor.executemany(insert_statement, data)
		conn.commit()
		cursor.close()
		logger.info("Inserted %s rows for pair=%s.", len(data), pair)
	except psycopg2.DatabaseError:
		logger.error("Failed db insert for pair=%s.", pair)
	finally:
		if conn:
			conn.close()


def scraper(event=None, context=None):
	"""Target function for scheduled data scrape event.

	Parameters
	----------
	event : dict
		AWS Lambda uses this parameter to pass in event data to the handler.
	context : LambdaContext
		AWS Lambda uses this parameter to provide runtime information to your handler.

	"""

	kraken = krakenex.API()
	start_time = time.time()

	for pair in PAIRS:

		previous_update_unix = get_last_update_time(pair)

		try:
			response = kraken.query_public('OHLC', data={'pair': pair, 'since': previous_update_unix, 'interval': 1})
		except (HTTPError, ConnectionError):
			logger.error("Failed querying Kraken exchange for pair=%s", pair, exc_info=True)
			continue

		data = response.get('result', {}).get(pair)
		if data is None:
			logger.error("No data returned from kraken for pair=%s.", pair)
		else:
			db_insert(data[:-1], pair)  # last entry in data is uncommitted window

	logger.info("Finished executing handler, took %0.1f seconds.", time.time() - start_time)
