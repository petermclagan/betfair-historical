class InvalidMarket(Exception):
	"""
	Raised when the market passed to the parser is of an invalid structure.
	This should not be raised when using the default schemas and validation.
	"""
	pass

class InvalidMarketChange(Exception):
	"""
	Raised when the market_change point passed to the parser is of an invalid structure.
	This should not be raised when using the default schemas and validation.
	"""
	pass

class MissingArguments(Exception):
	"""
	Raised when values for sport, plan, from_date, to_date have not been set in BetfairHistoricDownloader.
	"""
	pass
