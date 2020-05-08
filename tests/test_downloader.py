"""
This file tests the functionality of BetfairHistoricDownloader.
"""
import os
from datetime import datetime
from getpass import getpass

import pytest

from betfairHistorical import BetfairHistoricDownloader
from betfairHistorical.exceptions import MissingArguments

# Setup of credentials
USERNAME = os.environ.get('BETFAIR_USERNAME')
PASSWORD = os.environ.get('BETFAIR_PASSWORD')
APP_KEY = os.environ.get('APP_KEY')
CERT_PATH = os.environ.get('CERT_PATH')

if not USERNAME:
	USERNAME = input("Betfair username:")

if not PASSWORD:
	PASSWORD = getpass("Betfair password:")

if not APP_KEY:
	APP_KEY = getpass("Betfair application key:")

if not CERT_PATH:
	CERT_PATH = input("Path to certs:")

CORE_CREDS = {
	"username": USERNAME,
	"password": PASSWORD,
	"app_key": APP_KEY,
	"cert_path": CERT_PATH
	}


downloader = BetfairHistoricDownloader(
				sport="Soccer",
				plan="Basic Plan",
				from_date=datetime(2020, 1, 1),
				to_date=datetime(2020, 1, 2),
				**CORE_CREDS
			)

class TestBetfairHistoricDownloader:
	def test_args_validation_complete_args(self):
		assert downloader._validate_args() is None

	def test_args_validation_missing_all_required(self):
		bad_downloader = BetfairHistoricDownloader(
				**CORE_CREDS
			)
		with pytest.raises(MissingArguments):
			bad_downloader._validate_args()

	def test_args_validation_missing_some_required(self):
		bad_downloader = BetfairHistoricDownloader(
				from_date=datetime(2020, 1, 1),
				to_date=datetime(2020, 1, 2),
				**CORE_CREDS
			)
		with pytest.raises(MissingArguments):
			bad_downloader._validate_args()

	def test_args_validation_missing_one_required(self):
		bad_downloader = BetfairHistoricDownloader(
				sport="Soccer",
				plan="Basic Plan",
				from_date=datetime(2020, 1, 1),
				**CORE_CREDS
			)
		with pytest.raises(MissingArguments):
			bad_downloader._validate_args()

	def test_correct_available_data(self):
		for purchase in downloader.available_data:
			if (purchase['sport'] == 'Soccer'
			and purchase['plan'] == 'Basic Plan' 
			and purchase['forDate'] =='2019-01-01T00:00:00'):
				expected_purchase = purchase
				break

		assert expected_purchase

	def test_collection_options_keys(self):
		keys = downloader.collection_options().keys()
		assert 'countriesCollection' in keys
		assert 'fileTypeCollection' in keys
		assert 'marketTypesCollection' in keys

	def test_basket_size_keys(self):
		keys = downloader.basket_size().keys()
		assert 'totalSizeMB' in keys
		assert 'fileCount' in keys

	def test_file_list(self):
		"""
		No hardcoded file paths as they could move on Betfair server.
		"""
		file_list = downloader.file_list(
			market_types_collection=["MATCH_ODDS"],
			countries_collection=["GB"],
			file_type_collection=["M"]
			)
		assert len(file_list) >= 1

	def test_download_single_file(self):
		file_list = downloader.file_list(
			market_types_collection=["MATCH_ODDS"],
			countries_collection=["GB"],
			file_type_collection=["M"]
			)
		downloaded_file = False
		downloader.download_file(file_path=file_list[0], local_dir=os.getcwd())
		for f in os.listdir(os.getcwd()):
			if f.endswith('.bz2'):
				downloaded_file = True

		assert downloaded_file

	@classmethod
	def teardown_class(cls):
		for f in os.listdir(os.getcwd()):
			if f.endswith('.bz2'):
				os.remove(f)
