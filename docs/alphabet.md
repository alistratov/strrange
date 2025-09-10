## Alphabet

The `Alphabet` class represents a custom alphabet and allows conversion between 
words and ordinal numbers, as well as generating ranges of words.

It defines a positional numeral system over an arbitrary user-defined alphabet, and supports:

- Converting words into ordinal numbers (`ordinal`).
- Converting ordinal numbers back to words (`word`).
- Generating inclusive ranges of words (`range`).
- Calculating range lengths (`range_length`).


### Constructor
#### \_\_init__
```python
Alphabet(alphabet: str) -> Alphabet
```
Creates an alphabet with the given string of characters. Each character must be unique.

### Methods
#### ordinal
```python
ordinal(word: str) -> int
```
Convert a word into its ordinal index within this alphabet. The empty string maps to `0`.

Raises `ValueError` if the word contains characters not in the alphabet.

#### word
```python
word(n: int) -> str
```
Converts an ordinal number back into its corresponding word.

#### range
```python
range(start: str, stop: str) -> Iterator[str]
```
Generates an inclusive sequence of words between start and stop.

 - If `start <= stop`, the range is ascending.
 - If `start > stop`, the range is descending.

#### range_length
```python
range_length(start: str, stop: str) -> int:
```
Returns the number of elements in the inclusive range from start to stop.


### Examples
Constructing an alphabet:
```python
abc = Alphabet("abc")
print(abc.word(5))        # 'ab'
print(abc.ordinal("ab"))  # 5
```

Iterating over a range:
```python
abc = Alphabet("abc")
for word in abc.range("a", "ba"):
    print(word)

# Output: a, b, c, aa, ab, ac, ba
```

Range length:
```python
abc = Alphabet("abc")
print(abc.range_length("a", "ba"))  # 7
```
