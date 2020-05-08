"""
This file contains global variables used within the package.

SUPPORTED_PLANS - the plan types which have been implemented, of type tuple.
SUPPORTED_MARKETS - the markets for each sport that are supported
					A dictionary with supported sports as keys and their markets
					as a list of values.
"""

SUPPORTED_PLANS = ('basic')

SUPPORTED_MARKETS = {
	'soccer': [
		'match_odds'
		]
}
