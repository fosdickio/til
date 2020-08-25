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

## Logging
```python
import logging
logger = logging.getLogger('my_logger')
logger.setLevel(args.loglevel)
```

## JSON to YAML
```python
import yaml # pyyaml in requirements.txt
yaml.dump(json_data, output_file)
```

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
