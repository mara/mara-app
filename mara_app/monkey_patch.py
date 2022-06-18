"""
Functions for monkey patching functions in other modules. See https://en.wikipedia.org/wiki/Monkey_patch

There are other excellent libraries for this, which unfortunately don't excactly match our use case:

- https://github.com/christophercrouzet/gorilla
- https://github.com/iki/monkeypatch
- https://github.com/theatlantic/python-monkey-business
- https://bitbucket.org/schesis/ook
"""

import functools
import sys
import typing

REPLACED_FUNCTIONS: {str: str} = {}
"""
A list of all functions that have been replaced or wrapped by other functions, for documentation purposes
The dictionary maps the module and name of the original function to a tuple  to the module and name of the new function
"""


def patch(original_function: typing.Callable) -> typing.Callable:
    """
    A decorator for replacing a function in another module

    Examples:
        >>> # in some_package.some_module:
        ... def some_function(x):
        ...     return x + 1

        >>> some_package.some_module.some_function(1)
        2

        >>> @patch(some_package.some_module.some_function)
        ... def new_function(x):
        ...      return x + 2

        >>> some_package.some_module.some_function(1)
        3

        >>> # equivalent:
        >>> patch(some_package.some_module.some_function)(lambda x: x + 2)

    Args:
        original_function: The function or method to patch

    Returns:
        The replaced function
    """

    def decorator(new_function):
        if not isinstance(original_function, typing.Callable):
            raise TypeError("Argument passed to @patch decorator must be a Callable")

        # record function replacement for inspection purposes
        REPLACED_FUNCTIONS[f'{sys.modules[original_function.__module__].__name__}.{original_function.__name__}'] \
            = f'{sys.modules[new_function.__module__].__name__}.{new_function.__name__}'

        # copy properies such as __doc__, __module__ from original_function to new_function
        functools.update_wrapper(new_function, original_function)

        # replace function
        setattr(sys.modules[original_function.__module__], original_function.__name__, new_function)
        return new_function

    return decorator


def wrap(original_function: typing.Callable) -> typing.Callable:
    """
    A decorator for wrapping a function in another module

    Examples:
        >>> # in some_package.some_module:
        ... def some_function(x):
        ...     return x + 1

        >>> some_package.some_module.some_function(1)
        2

        >>> @wrap(some_package.some_module.some_function)
        ... def new_function(original_function, x):
        ...      return original_function(x) + 1

        >>> some_package.some_module.some_function(1)
        3

    Args:
        original_function: The function or method to wrap

    Returns:
        The wrapped function
    """

    def decorator(new_function):
        if not isinstance(original_function, typing.Callable):
            raise TypeError("Argument passed to @wrap decorator must be a Callable")

        # record function replacement for inspection purposes
        REPLACED_FUNCTIONS[f'{sys.modules[original_function.__module__].__name__}.{original_function.__name__}'] \
            = f'{sys.modules[new_function.__module__].__name__}.{new_function.__name__}'

        # supply orginal_function as first argument to new_function
        def wrapper(*args, **kwargs):
            return new_function(original_function, *args, **kwargs)

        # copy properies such as __doc__, __module__ from original_function to wrapper
        functools.update_wrapper(wrapper, original_function)

        # replace function
        setattr(sys.modules[original_function.__module__], original_function.__name__, wrapper)
        return wrapper

    return decorator
