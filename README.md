# Text Analyzer
This module implements APIs to analyze text for possible errors and provide suggestions against input dictionary
using Damerau-Levenshtein Distance algorithm. Here, Damerau-Levenshtein Distance is calculated by using Iterative Matrix method.


## Requirements
- Python2.x/Python3.x


## Installation
There are no external dependencies for this script. 

```
chmod +x text_analyzer.py
```


## Usage

```
text_analyzer.py [-h] [-t T] [-f F] [-d D]
optional arguments:
  -h, --help  show this help message and exit
  -t T        Input text to be analyzed
  -f F        Input file path containing text to be analyzed
  -d D        Input file path of dictionary to be used with analyzer. Each new
              word should be on new line.
```


## References
- https://en.wikipedia.org/wiki/Levenshtein_distance
- https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
