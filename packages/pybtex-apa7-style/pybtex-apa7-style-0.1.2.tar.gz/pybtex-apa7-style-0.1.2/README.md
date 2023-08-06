# APA7 Style for Pybtex

*This is a fork of [naeka's pybtex-apa-style](https://github.com/naeka/pybtex-apa-style)*.

[Pybtex](https://pybtex.org/) provides Python support for interacting with bibtex-formatted
bibliography information. Style plugins are required to format a bibliography in a given 
style, similar to the role that `csl` files play for LaTeX.

This plugin provides APA7 style.

## Installation

```
$ pip install pybtex pybtex-apa7-style
```

## Usage

Pybtex uses [Python's plugin system](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/).
To use APA7, load it as a plugin.

```python3
from pybtex.plugin import find_plugin
from pybtex.database import parse_file
APA = find_plugin('pybtex.style.formatting', 'apa7')()
HTML = find_plugin('pybtex.backends', 'html')()

def bib_to_apa7_html(bibfile):
    bibliography = parse_file(bibfile, 'bibtex')
    formatted_bib = APA.format_bibliography(bibliography)
    return "<br>".join(entry.text.render(HTML) for entry in formatted_bib)
```
