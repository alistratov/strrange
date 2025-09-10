The `strrange` is a Python library that helps produce sequences of strings given the _first_ and _last_ element. It is designed to cover common practical cases like file names, numeric identifiers, and alphanumeric codes.

## Table of contents
* [Installation](#installation)
* [Example](#example)
* [Description](#description)
* [Alphabet class](alphabet.md)
* [License](license.md)


## Installation
Requires Python version 3.10 or higher. To install the package, run:
```bash
pip install strrange
```


## Example
```python
from strrange import range as srange

print(list('AA' + srange('QM', 'QZ') + srange('XA', 'XZ') + 'ZZ'))
# Output: list of ISO 3166-1 alpha-2 codes for private use, total 42 items.
```

## Description
The main function is `strrange.range(start: str, stop: str)`, which generates strings from `start` to `stop`, inclusive.

 - The function attempts to “guess” the progression by analyzing numeric parts, repeated substrings, and alphanumeric regions (`0–9 A–Z a–z`).
 - If start and stop share a common prefix or suffix, it is preserved where possible.
 - If an integer is detected in the pattern, and it begins with `0` or a space, the generated numbers are padded accordingly .
 - If stop is less than start (in some alphabet or as numbers), the sequence is generated in reverse (from stop to start).
 - If both start and stop are empty strings, the result is an empty sequence.
 - If start and stop are equal, the result contains exactly one element.
 - If no obvious pattern is found, it simply yields `[start, stop]`.

The padding style is determined by the `start` string only:
```python
list(srange('img001.png', 'img5.png'))
# ['img001.png', 'img002.png', 'img003.png', 'img004.png', 'img005.png']
```

Signs and underscores in numeric literals are recognized, but may be ignored in the output:
```python
list(srange('1_000.png', '+1002.png'))
# ['1000.png', '1001.png', '1002.png']
```

Ambiguities are inevitable: the algorithm is “magical” in the sense that it tries to guess the intended sequence, but sometimes this magic does not work. For example, after the sequence `'A8', 'A9'` should the next element be `'AA'`, `'A10'`, `'BA'`, or `'B0'`?

For fine-grained control, you may use the underlying [Alphabet](alphabet.md) class.

Actually, `strrange.range` returns not a plain generator, but a special range object that is iterable and also supports concatenation with:

- Other `strrange.range` objects  
- Lists of strings  
- Single strings (treated as scalar values, not iterables)

This allows you to build composite sequences easily.

The development status is **alpha**; algorithms are heuristic and may change. If you encounter results that seem unexpected, please share examples — even if they won’t always lead to changes (what is unexpected for one user may be the intended logic for another), they help us understand real-world cases. 

Examples are welcome as issue reports or pull requests.
