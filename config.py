

PAIRS = [
	'XXBTZEUR',  # bitcoin euro
	'XXBTZUSD',  # bitcoin usd
	'XETHZEUR',  # ethereum euro
	'XXRPZEUR',  # ripple euro
	'BCHEUR',  # bitcoin cash euro
	'EOSEUR',  # eos euro
	'XLTCZEUR',  # litecoin euro
	'XXMRZEUR',  # monero euro
	'DASHEUR',  # dash euro
	'XETCZEUR',  # ethereum classic euro
	'GNOEUR',  # gnosis euro
	'XZECZEUR',  # zcash euro
	'XXDGXXBT'  # doge coin bitcoin
]


LOGGING = {
	'disable_existing_loggers': False,
	'version': 1,
	'formatters': {
		'simple': {
			'format': '%(asctime)s - %(levelname)s - %(message)s'
		},
	},
	'handlers': {
		'console': {
			'level': 'DEBUG',
			'formatter': 'simple',
			'class': 'logging.StreamHandler',
		}
	},
	'loggers': {
		'scraper': {
			'handlers': ['console'],
			'level': 'INFO',
		}
	},
}
