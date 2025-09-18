# Python Code Style Guide

This project follows the [PEP 8](https://peps.python.org/pep-0008/) Python code style guide.  
Below are the key conventions to follow:

## 1. Imports
- Standard library imports first, then third-party, then local imports.
- Each group separated by a blank line.

```python
import os
import sys

import requests

from . import mymodule
```

## 2. Naming Conventions
- Classes: `CamelCase`
- Functions & variables: `snake_case`
- Constants: `ALL_CAPS`

## 3. Indentation
- Use 4 spaces per indentation level.

## 4. Line Length
- Limit all lines to a maximum of 79 characters.

## 5. Docstrings
- Use triple double quotes for docstrings.
- Include a docstring for all public modules, functions, classes, and methods.

```python
def my_function(param1, param2):
    """
    Brief description of the function.

    Args:
        param1 (type): Description.
        param2 (type): Description.

    Returns:
        type: Description.
    """
    pass
```

## 6. Spacing
- Use blank lines to separate functions and classes.
- No extra spaces inside parentheses, brackets, or braces.

## 7. Type Hints
- Use type hints for function arguments and return types.

```python
def add(a: int, b: int) -> int:
    return a + b
```

## 8. Error Handling
- Use exceptions appropriately.
- Prefer specific exception types.

## 9. Main Entry Point
- Use the following pattern for executable scripts:

```python
if __name__ == "__main__":
    main()
```

## 10. Linting
- Use tools like `flake8` or `black` to check and format code.
