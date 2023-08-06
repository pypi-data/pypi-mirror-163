## Flake type annotations plugin

[![Python Version](https://img.shields.io/pypi/pyversions/flake-type-annotations-plugin.svg)](https://pypi.org/project/flake-type-annotations-plugin/)
[![PyPI version](https://badge.fury.io/py/flake-type-annotations-plugin.svg)](https://pypi.org/project/flake-type-annotations-plugin/)
[![PyPI - License](https://img.shields.io/pypi/l/flake8-annotations?color=magenta)](https://github.com/sco1/flake8-annotations/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

The `flake8` plugin checking for correct usage of the Python type annotations.

Use with [flake8-annotations](https://pypi.org/project/flake8-annotations/) for even better results!

## Installation

Plugin requires `flake8 >3.0.0`

```bash
pip install flake-type-annotations-plugin
```

## Rules

### `TAN001`

This rule disallows usage of `Union` and `Optional` type annotations and expects user 
to use the new `|` operator syntax.

Example:

```python
# WRONG
from typing import Optional, Union

def func(arg: Optional[int]) -> Union[int, str]:  # violates TAN001
    return arg if arg is not None else "N/A"

# CORRECT
def func(arg: int | None) -> int | str:  # OK
    return arg if arg is not None else "N/A"
```

For Python versions `<3.10` a top-level module import 
`from __future__ import annotations` must be included in order to use this 
syntax.

More can be read in [PEP604](https://peps.python.org/pep-0604/).

### `TAN002`

This rule disallows usage of type annotations where built-in types can be used.

Example:

```python
# WRONG
from typing import List, Tuple

def func(arg: Tuple[int]) -> List[int]:  # violates TAN002
    return list(arg)

# CORRECT
def func(arg: tuple[int]) -> list[int]:  # OK
    return list(arg)
```

For Python versions `<3.9` a top-level module import
`from __future__ import annotations` must be included in order to use this
syntax.

More can be read in [PEP585](https://peps.python.org/pep-0585/).
