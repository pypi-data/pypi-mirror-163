# exhaustion
A tiny library to help in exhaustive testing of Boolean functions in Python.

![Logo](logo.svg)

## Requirements

- Python 3.6 or newer

## Installation

Exhaustion can be installed using `pip`:

```sh
pip install exhaustion
```

## Usage

Usage is very straightforward, `exhaustion` is compatible with any testing library that supports assertions.

```python
import unittest

from exhaustion import exhaust

def _and(a: bool, b: bool):
    """ A simple wrapper over the Python `and` operator for demonstration purposes.

    Args:
        a (bool): The left-hand operand.
        b (bool): The right-hand operand.
    Returns:
        bool: The Boolean conjunction of the arguments provided.
    """
    return a and b

class TestAndAlgebraic(unittest.TestCase):
    """ Tests the algebraic properties of the _and function.
    """

    def test_and_commutative(self):
        """ Proves by exhaustion that the _and function is commutative.
        """
        # The lambda below will execute for every possible combination of Boolean arguments.
        exhaust(lambda a, b: self.assertTrue(_and(a, b) == _and(b, a)))
```

## Related Projects

This library is intentionally very minimal, and was designed to be so. If you're looking for a richer feature set, you might consider the following projects:

- [exhaust](https://github.com/letmaik/exhaust) - Not to be confused with this project, a library that supports exhastive enumeration of any finite set you can express using a generator function.

## License

[MIT](LICENSE) © [lambdacasserole](https://github.com/lambdacasserole).
