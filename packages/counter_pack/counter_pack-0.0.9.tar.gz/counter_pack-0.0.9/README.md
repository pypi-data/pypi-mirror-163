# Counter_pack

This is a simple package for counting unique characters in a string or text file.

# Software requirements

Python 3.8+
pip

# Installation

Counter_pack is available on PyPI and can be installed with pip.

`pip install counter_pack`

# License

Counter_pack is distributed under the terms of the MIT license.

# Running Counter_pack commands with CLI

usage: `your_code.py [-h] [-s STRING] [-f FILE]`

optional arguments:

  `-h,  --help                  ` show help message and exit

  `-s STRING,  --string STRING  ` some string for count unique characters

  `-f FILE,  --file FILE        ` some file for count unique characters


for example: `python main.py -f 'tests/test.txt'`
          or `python main.py -s 'another string'`


_main.py_
```
from counter_paсk import counter


if __name__ == '__main__':
    print(counter.main())

```