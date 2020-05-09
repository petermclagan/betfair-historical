# Running tests
## Downloader
*It should be noted that due to timeout errors on the server these may not all succeed. In this case, wait for a few minutes and try again.*

In order to run these tests certain criteria must be met.
- "Purchase" the **Basic Plan** for **Soccer** for the month of **January 2020** (this should be free).
- Ensure you have a valid **application key** (see [here](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Application+Keys) for instructions).
- Ensure you have correctly set up SSL certificates (see [here](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Non-Interactive+%28bot%29+login) for instructions).

The tests will require the application key and path to SSL certificates, as well as your Betfair username and password. These can be set by either:
1. Setting the environment variables **BETFAIR_USERNAME**, **BETFAIR_PASSWORD**, **APP_KEY** and **CERT_PATH**.
2. Running the tests with the `-s` flag and you will receive prompts.

These tests can be run using the command:
```bash
pytest test_downloader.py [-s]
```

## Parser
These tests should all run without any setup, with the command:
```bash
pytest test_parser.py [-s]
```