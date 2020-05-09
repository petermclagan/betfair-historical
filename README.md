
# betfairHistorical
Tooling for interacting with the Betfair API for historical data.

Two tools are available, `BetfairHistoricalDownloader` and `BetfairHistoricalFileParser`.

## BetfairHistoricalDownloader
*This is mainly a wrapper around [betfairlightweight](https://github.com/liampauling/betfair). All configuration and setup for that library should be followed. The main additions in this library are a cleaner interface when only interacting with historic data and making it as simple as possible to view and download available files for a range of dates.*

Example usage:
```python
from datetime import datetime

from betfairHistorical import BetfairHistoricDownloader

downloader = BetfairHistoricDownloader(
	username=<username>,
	password=<password>,
	app_key=<application_key>,
	cert_path=<local_path_to_ssl_certificates>,
	sport='Soccer',
	plan='Basic plan',
	from_date=datetime(2020, 1, 1),
	to_date=datetime(2020, 2, 1)
	)	
```
* To view available historic data to download:
	 ```python
	 downloader.available_data
	 ```
* To view collection options:
	```python
	downloader.collection_options()
	```
* To view basket_size:
	```python
	downloader.basket_size()
	```
* To view file list:
	```python
	file_list = downloader.file_list(
		market_types_collection=["MATCH_ODDS"],
		countries_collection=["GB"],
		file_type_collection=["M"]
		)
	```
* To download all available files:
	```python
	for f in file_list:
		downloader.download_file(
			file_path=f,
			local_dir=<local_download_dir>
			)
	```

## BetfairHistoricalFileParser
*This module will parse the downloaded bz2 files from BetfairHistoricalDownloader, perform schema validation if required, and extract the useful data. For further details of the file contents see [here](https://historicdata.betfair.com/Betfair-Historical-Data-Feed-Specification.pdf).*

Example:
```python
from betfairHistorical import BetfairHistoricalFileParser

parser = BetfairHistoricalFileParser(
	local_path=<path_to_file_or_dir>,
	sport="soccer",
	plan="basic",
	market="match_odds",
	recursive=True,
	validate=True,
	validation_schema=None
	)
```
#### Validation
The structure of the data contents can be validated with the `jsonschema` library (see [here](https://python-jsonschema.readthedocs.io/en/stable/)). Default schemas are provided for the implemented markets (currently only `match_odds` for `soccer`). Any valid custom schema can be passed with the `validation_schema` argument.

#### File Contents
* `id` - marketId Unique identifier for the market.
* `marketDefinition` - Fields containing details of the market -new market definition is published if any of these field change.
* `runnerChange` - a list of changes to runners.
* `publishedTime` - Published Time (in millis since epoch).

Other fields from the files are not extractable with this module.