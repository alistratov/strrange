# strrange
Generate inclusive lexicographic ranges of strings.

[![PyPI - Version](https://img.shields.io/pypi/v/strrange)](https://pypi.org/project/strrange/) [![codecov](https://codecov.io/gh/alistratov/strrange/graph/badge.svg?token=MSJLFL8XFD)](https://codecov.io/gh/alistratov/strrange) [![Documentation Status](https://readthedocs.org/projects/strrange/badge/?version=latest)](https://strrange.readthedocs.io/en/latest/?badge=latest) [![PyPI - Downloads](https://img.shields.io/pypi/dm/strrange)](https://pypistats.org/packages/strrange)


## Synopsis
```bash
pip install strrange
```

```pycon
>>> from strrange import range as srange

>>> list(srange('a', 'm'))
['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']

>>> list(srange('file001.txt', 'file004.txt'))
['file001.txt', 'file002.txt', 'file003.txt', 'file004.txt']

>>> list(srange('A', 'XFD'))
# A complete list of all column names in Excel. 

>>> list(srange('i)', 'iii)'))
['i)', 'ii)', 'iii)']

>>> list('AA' + srange('QM', 'QZ') + srange('XA', 'XZ') + 'ZZ')
# Output: list of ISO 3166-1 alpha-2 codes for private use
```


## Overview
The `strrange` is a Python library that helps produce sequences of strings given the _first_ and _last_ element. It is designed to cover common practical cases like file names, numeric identifiers, and alphanumeric codes.

It attempts to “guess” the progression by analyzing numeric parts, repeated substrings, and alphanumeric regions (`0–9A–Za–z`). If no obvious pattern is found, it simply yields `[start, stop]`.

⚠️ **Alpha version:** algorithms are heuristic and may change.

If you encounter results that seem unexpected, please share examples or — even if they won’t always lead to changes (what is unexpected for one user may be the intended logic for another), they help us understand real-world cases.

Examples are welcome as issue reports or pull requests.

## Documentation
Read the full documentation at [Read the docs](https://strrange.readthedocs.io/en/latest/).


## License
Copyright 2025 Oleh Alistratov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0).

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
