import bz2
import json
import os
import pkg_resources
from typing import Dict, List, Union

import jsonschema

from betfairHistorical.exceptions import InvalidMarket, InvalidMarketChange
from betfairHistorical.globals import SUPPORTED_MARKETS, SUPPORTED_PLANS

class BetfairHistoricalFileParser:
	def __init__(
		self,
		local_path: str,
		sport: str,
		plan: str,
		market: str,
		recursive: bool=False,
		validate: bool=True,
		validation_schema: Dict=None
	):
		"""
		This class is used to parse the bz2 files retrieved from Betfair. 
		Due to the nature of these files, only SUPPORTED_MARKETS and SUPPORTED_PLANS are implemented for validation.
		Other files will be added in future versions, or can be used without the in-built validation.

		This will allow the user to extract the id, marketDefinition, runnerChanges and timestamps for each event by passing only the raw bz2 file location.

		:param local_path: The local path to the file(s)
		:param sport: Sport to parse files. Must be one of keys in SUPPORTED_MARKETS if validation is used.
		:param plan: Plan to parse files. Must be in SUPPORTED_PLANS
		:param market: Market to parse files. Must be one of values in SUPPORTED_MARKETS if validation is used.
		:param recursive: Parse all files contained within local path.
		:param validate: Validates file contents using a jsonschema.
		:param validation_schema: The jsonschema to be used for validation. If None and validate is True will use files in validation_schemas.
		"""
		self.local_path = local_path
		self.sport = sport.lower()
		self.plan = plan.lower()
		self.market = market.lower()
		self.recursive = recursive
		self.validate = validate
		self.validation_schema = validation_schema

		if not os.path.exists(self.local_path):
			raise FileExistsError('File path does not exist')

		if not self.sport in SUPPORTED_MARKETS.keys() and self.validate:
			raise NotImplementedError(f'{self.sport} not currently implemented.')

		if not self.plan in SUPPORTED_PLANS and self.validate:
			raise NotImplementedError(f'{self.plan} not currently implemented')

		if not self.market in SUPPORTED_MARKETS[self.sport] and self.validate:
			raise NotImplementedError(f'{self.market} not currently implemented')

		if os.path.isdir(self.local_path):
			self.data = self._read_files()

		else:
			self.data = list(self._read_file(self.local_path))

	def _read_file(self, file_path: str) -> List[bytes]:
		"""
		Reads a single bz2 file contained within file_path and returns the file contents as a bytes
		"""
		with bz2.open(file_path) as f:
			_data = f.readlines()
			
			if self.validate:
				self._validate_schema(contents=_data)

		return _data

	def _read_files(self) -> List[List[bytes]]:
		"""
		Reads all bz2 files contained within a single directory.
		"""
		if self.recursive:
			_file_paths = [os.path.join(root, file) for root, subdirs, files in os.walk(self.local_path) for file in files]
			return [self._read_file(f) for f in _file_paths]
		else:
			return [self._read_file(os.path.join(self.local_path, f)) for f in os.listdir(self.local_path)]

	def _validate_schema(self, contents: bytes):
		"""
		Used to validate the bytes content of the bz2 files against a jsonschema object.
		The jsonschema can either be set in the class init, or placed in the validation_schemas folder.
		"""
		default_schema = f"validation_schemas/{self.sport}/{self.market}.json"
		default_schema_path = pkg_resources.resource_filename(__name__, default_schema)
		if self.validation_schema:
			schema = self.validation_schema
		elif os.path.exists(default_schema_path):
			with open(default_schema_path) as schema_json:
				schema = json.load(schema_json)
		else:
			raise NoValidationSchema("No validation schema available in defaults or provided.")
		for _line in contents:
			if not isinstance(_line, bytes):
			jsonschema.validate(instance=json.loads(_line), schema=schema)
		return

	def get_market_change_id(sef, market_change: Dict) -> str:
		"""
		Returns the id of a single market change event. 
		This is always returned as a string as should be complete for usage as a primary key.
		"""
		market_change_id = market_change.get('id')
		if not market_change_id:
			raise InvalidMarketChange("Market change has no valid id key.")
		return str(market_change_id)


	def get_market_definition(self, market_change: Dict) -> Union[Dict, None]:
		"""
		Returns the market definition from a single market change event.
		Not all market changes have a market definition so this may return None.
		"""
		return market_change.get('marketDefinition')

	def get_runner_change(self, market_change: Dict) -> Union[Dict, None]:
		"""
		Returns the runner changes from a single market change event.
		Not all market changes have a runner change so this may return None.
		"""
		return market_change.get('rc')


	def get_published_time(self, market: Dict) -> int:
		"""
		Returns the published time of a single market.
		"""
		published_time = market.get('pt')
		if not published_time:
			raise InvalidMarket("No published time available.")
		return published_time
