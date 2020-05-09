"""
This file tests the functionality of BetfairHistoricalFileParser
"""
import bz2
import json
import os

import pytest
from jsonschema.exceptions import ValidationError

from betfairHistorical import BetfairHistoricalFileParser
from betfairHistorical.exceptions import InvalidMarket, InvalidMarketChange

TEST_DATA_LOCAL_DIR = os.path.join(os.getcwd(), 'sample_data')
TEST_DATA_LOCAL_FILE = os.path.join(TEST_DATA_LOCAL_DIR, 'football-basic-sample.bz2')

with bz2.open(TEST_DATA_LOCAL_FILE) as f:
	CONTENTS = f.readlines()

parser = BetfairHistoricalFileParser(
		local_path=TEST_DATA_LOCAL_DIR,
		sport="soccer",
		plan="basic",
		market="match_odds",
		recursive=True,
		validate=False
	)

event = parser.data[0][0]
market = json.loads(event.decode())
market_change = market.get('mc')[8]	# contains both marketDefinition and rc


class TestBetfairHistoricalFileParser:

	# Init tests
	def test_local_path_not_exists(self):
		with pytest.raises(FileExistsError):
			BetfairHistoricalFileParser(
				local_path="This is not a path",
				sport="soccer",
				plan="basic",
				market="match_odds"
			)

	def test_sport_not_in_supported_markets(self):
		with pytest.raises(NotImplementedError):
			BetfairHistoricalFileParser(
				local_path=TEST_DATA_LOCAL_DIR,
				sport="animals",
				plan="basic",
				market="match_odds",
				validate=True
			)

	def test_plan_not_in_supported_plans(self):
		with pytest.raises(NotImplementedError):
			BetfairHistoricalFileParser(
				local_path=TEST_DATA_LOCAL_DIR,
				sport="soccer",
				plan="imaginary",
				market="match_odds",
				validate=True
			)

	def test_market_not_in_supported_markets(self):
		with pytest.raises(NotImplementedError):
			BetfairHistoricalFileParser(
				local_path=TEST_DATA_LOCAL_DIR,
				sport="soccer",
				plan="basic",
				market="piegate",
				validate=True
			)

	# _read_files tests
	def test_read_files_returns_expected_data(self):
		assert parser._read_file(TEST_DATA_LOCAL_FILE) == CONTENTS

	def test_read_files_recursively_returns_data(self):
		assert parser.data == [CONTENTS]

	# _validate_schema tests
	def test_validate_schema_with_default(self):
		default_schema_parser = BetfairHistoricalFileParser(
			local_path=TEST_DATA_LOCAL_DIR,
			sport="soccer",
			plan="basic",
			market="match_odds",
			recursive=True,
			validate=False
			)
		assert not default_schema_parser._validate_schema(CONTENTS)

	def test_validate_schema_with_supplied_schema(self):
		passed_schema_parser = BetfairHistoricalFileParser(
			local_path=TEST_DATA_LOCAL_DIR,
			sport="soccer",
			plan="basic",
			market="match_odds",
			recursive=True,
			validate=False,
			validation_schema={}	# allows all valid dicts
			)
		assert not passed_schema_parser._validate_schema(CONTENTS)

	def test_validate_schema_fails_on_invalid(self):
		invalid_parser = BetfairHistoricalFileParser(
			local_path=TEST_DATA_LOCAL_DIR,
			sport="soccer",
			plan="basic",
			market="match_odds",
			recursive=True,
			validate=False,
			validation_schema={"type": "number"}
			)
		with pytest.raises(ValidationError):
			invalid_parser._validate_schema(CONTENTS)			

	# get_market_change_id tests
	def test_get_market_change_with_id(self):
		mc_id = parser.get_market_change_id(market_change)
		assert mc_id == "1.131162722"

	def test_get_market_change_no_id(self):
		with pytest.raises(InvalidMarketChange):
			parser.get_market_change_id({})

	# get_market_definition tests
	def test_get_market_definition_with_marketDefinition(self):
		md = parser.get_market_definition(market_change)
		expected_md = {
			'betDelay': 0,
			'bettingType': 'ODDS',
			'bspMarket': False,
			'bspReconciled': False,
			'complete': True,
			'countryCode': 'GB',
			'crossMatching': True,
			'discountAllowed': True,
			'eventId': '28202626',
			'eventName': 'Middlesbrough v Man City',
			'eventTypeId': '1',
			'inPlay': False,
			'marketBaseRate': 5.0,
			'marketTime': '2017-04-30T13:05:00.000Z',
			'marketType': 'HALF_TIME_FULL_TIME',
			'name': 'Half Time/Full Time',
			'numberOfActiveRunners': 9,
			'numberOfWinners': 1,
			'openDate': '2017-04-30T13:05:00.000Z',
			'persistenceEnabled': True,
			'regulators': ['MR_INT'],
			'runners': [
				{
					'id': 71080,
					'name': 'Middlesbrough/Middlesbrough',
					'sortPriority': 1,
					'status': 'ACTIVE'
				},
				{
					'id': 71079,
					'name': 'Middlesbrough/Draw',
					'sortPriority': 2,
					'status': 'ACTIVE'
				},
				{
					'id': 261273,
					'name': 'Middlesbrough/Man City',
					'sortPriority': 3,
					'status': 'ACTIVE'
				},
				{
					'id': 71081,
					'name': 'Draw/Middlesbrough',
					'sortPriority': 4,
					'status': 'ACTIVE'
				},
				{
					'id': 3710152,
					'name': 'Draw/Draw',
					'sortPriority': 5,
					'status': 'ACTIVE'
				},
				{
					'id': 69426,
					'name': 'Draw/Man City',
					'sortPriority': 6,
					'status': 'ACTIVE'
				},
				{
					'id': 3507812,
					'name': 'Man City/Middlesbrough',
					'sortPriority': 7,
					'status': 'ACTIVE'
				},
				{
					'id': 69424,
					'name': 'Man City/Draw',
					'sortPriority': 8,
					'status': 'ACTIVE'
				},
				{
					'id': 69423,
					'name': 'Man City/Man City',
					'sortPriority': 9,
					'status': 'ACTIVE'
				}
			],
			'runnersVoidable': False,
			'status': 'OPEN',
			'suspendTime': '2017-04-30T13:05:00.000Z',
			'timezone': 'Europe/London',
			'turnInPlayEnabled': True,
			'version': 1624812955
		}

		assert md == expected_md

	def test_get_market_definition_no_marketDefintion(self):
		md = parser.get_market_definition({})
		assert not md

	# get_runner_change tests
	def test_get_runner_change_with_rc(self):
		rc = parser.get_runner_change(market_change)
		assert rc == [{'ltp': 2.1, 'id': 69423}, {'ltp': 25.0, 'id': 71080}]

	def test_get_runner_change_no_rc(self):
		rc = parser.get_runner_change({})
		assert not rc
	
	# get_published_time tests
	def test_get_published_time_with_pt(self):
		pt = parser.get_published_time(market)
		assert pt == 1493129993643

	def test_get_published_time_no_pt(self):
		with pytest.raises(InvalidMarket):
			parser.get_published_time({})
