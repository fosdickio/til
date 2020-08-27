# Python Snippets

## Basics
```bash
pip3 install -r requirements.txt
```

```python
#!/usr/bin/env python

if __name__ == "__main__":
    main()
```

---

## Parsing Arguments
```python
from argparse import ArgumentParser, FileType

def parse_args():
    """
    Retrieve args from the command line.
    """
    parser = ArgumentParser(
        description="Text to display before the argument help.",
        epilog="Text to display after the argument help.",
    )
    parser.add_argument(
        "output", type=FileType("w"), nargs="?", default=stdout
    )
    parser.add_argument(
        "-n",
        "--numofitems",
        type=int,
        default=5,
        help="number of items in output",
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        default="WARNING",
        help="Only output log messages of this severity or above. Writes to stderr. (default: %(default)s)",
    )
    return parser.parse_args()

args = parse_args()
print(args.numofitems)
```

---

## API Calls

### Make API Calls
```python
import requests

class APIWrapper:
    def __init__(self, api_key = None):
        self.api_key = api_key

    def make_api_call(self, url, **kwargs):
        """
        Helper function to perform API requests.

        url : string - the URL being requested
        """
        response = requests.get(url, params=kwargs, timeout=60)
        status = response.status_code

        if status == 200:
            return response.text
        elif status == 400:
            raise errors.APIInsufficientArguments(url, kwargs)
        elif status == 404:
            raise errors.APIMethodUnavailable(url)
        elif status == 503:
            raise errors.APITimeoutError()
        else:
            raise errors.BaseError(msg=response.reason)
```

### Handle API Call Errors
```python
class BaseError(Exception):
    """
    Generic error wrapper.
    """
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return repr(self._msg)

class APIInsufficientArguments(BaseError):
    def __init__(self, query = None, params = None):
        self._msg = "HTTP 400: Insufficient arguments for \"{0}\". Parameters provided: {1}".format(query, params)

class APIAuthenticationError(BaseError):
    def __init__(self, api_key = None):
        self._msg = "HTTP 403: Authentication error caused by API key \"{}\".".format(api_key)

class APIMethodUnavailable(BaseError):
    def __init__(self, method_url = None):
        self._msg = "HTTP 404: \"{}\" is an unsupported/discontinued API method.".format(method_url)

class APITimeoutError(BaseError):
    def __init__(self):
        self._msg = "HTTP 503: Timeout error."
```

---

## Logging
```python
import logging
logger = logging.getLogger('my_logger')
logger.setLevel(args.loglevel)
```

---

## JSON to YAML
```python
import yaml # pyyaml in requirements.txt
yaml.dump(json_data, output_file)
```

---

## Travis CI
```
language: python

python:
  - "3.4"
  - "3.5"
  - "3.6"
  - "3.7"
  - "3.8"

install: pip install -r requirements.txt

script: python3 setup.py install && python3 tests.py
```
