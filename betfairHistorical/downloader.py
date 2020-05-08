import logging
from datetime import datetime
from typing import Dict, List

import betfairlightweight

from betfairHistorical.exceptions import MissingArguments

"""
This is a wrapper around the betfairlightweight library from liampauling 
(https://github.com/liampauling/betfair).

This will apply the relevant functions to all files contained within 
the provided date range for the provided sport and plan.
"""

logger = logging.getLogger()
logging.basicConfig(
            format='[%(asctime)s][%(threadName)s][%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')


class BetfairHistoricDownloader:
	def __init__(
		self,
		username: str,
		password: str, 
		app_key: str, 
		cert_path: str,
		sport: str=None,
		plan: str=None,
		from_date: datetime=None,
		to_date: datetime=None
		):
		"""
		Creates an instance to allow for interaction with the betfairlightweight API.
		Optional arguments are required for all functions other than getting available data.
		Once known parameters are known these must be passed to use other functions.

		:param username: Betfair username
		:param password: Betfair password
		:param app_key: Application key for Betfair account
		:param cert_path: Directory to certificates
		::param sport: Betfair sport
		:param plan: Betfair plan
		:param from_date: Datetime of earliest date to collect
		:param to_date: Datetime of latest date to collect
		"""

		self.username = username
		self.cert_path = cert_path

		self.sport = sport
		self.plan = plan
		self.from_date = from_date
		self.to_date = to_date

		self.trading = betfairlightweight.APIClient(
			username=username,
			password=password,
			app_key=app_key,
			certs=cert_path
			)
		self.trading.login()

		self.available_data = self.trading.historic.get_my_data()

	def _validate_args(self):
		"""
		Ensures that arguments are not None type.
		"""
		if not all([self.sport, self.plan, self.from_date, self.to_date]):
			raise MissingArguments("Require values for sport, plan, from_date, to_date.")
		return

	def collection_options(self):
		"""
		Returns the collection options available (allows filtering)
		"""
		self._validate_args()
		_collection_options = self.trading.historic.get_collection_options(
			sport=self.sport,
			plan=self.plan,
			from_day=self.from_date.day,
			from_month=self.from_date.month,
			from_year=self.from_date.year,
			to_day=self.to_date.day,
			to_month=self.to_date.month,
			to_year=self.to_date.year
			)
		return _collection_options

	def basket_size(self) -> Dict:
		"""
		Gets the advanced basket size.

		return: Dictionary containing details of basket size
		"""
		self._validate_args()
		_basket_size = self.trading.historic.get_data_size(
			sport=self.sport,
			plan=self.plan,
			from_day=self.from_date.day,
			from_month=self.from_date.month,
			from_year=self.from_date.year,
			to_day=self.to_date.day,
			to_month=self.to_date.month,
			to_year=self.to_date.year
			)
		return _basket_size

	def file_list(
		self,
		market_types_collection: List,
		countries_collection: List,
		file_type_collection: List
		) -> List:
		"""
		Gets the list of files contained within the parameters.

		:param market_types_collection: List of market types to collect
		:param countries_collection: List of countries to collect
		:param file_type_collection: List of file types to collect
		return: List of files contained within the parameters
		"""
		self._validate_args()
		_file_list = self.trading.historic.get_file_list(
			sport=self.sport,
			plan=self.plan,
			from_day=self.from_date.day,
			from_month=self.from_date.month,
			from_year=self.from_date.year,
			to_day=self.to_date.day,
			to_month=self.to_date.month,
			to_year=self.to_date.year,
			market_types_collection=market_types_collection,
			countries_collection=countries_collection,
			file_type_collection=file_type_collection
			)
		return _file_list

	def download_file(self, file_path: str, local_dir: str):
		"""
		Downloads a single file.

		:param file_path: Remote file path to be downloaded
		:param local_dir: Local directory to download file to
		"""
		logger.debug(f"Downloading {file_path}.")
		_downloaded_file = self.trading.historic.download_file(
			file_path=file_path,
			store_directory=local_dir
			)
		return _downloaded_file
