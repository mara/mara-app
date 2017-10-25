"""
Functions for monkey patching functions in other modules. See https://en.wikipedia.org/wiki/Monkey_patch

There are other excellent libraries for this, which unfortunately don't exactly match our use case:

- https://github.com/christophercrouzet/gorilla
- https://github.com/iki/monkeypatch
- https://github.com/theatlantic/python-monkey-business
- https://bitbucket.org/schesis/ook
"""

import functools
import inspect
import logging
import sys
import typing


# list of applied patches, used to later generate a 'report' of them
class Patch(typing.NamedTuple):
    replaces: bool
    original_module: str
    original_name: str
    description: str
    patcher_frame: typing.Any


__applied_patches = []

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def patch(original_function: typing.Callable, patch_description: str = '') -> typing.Callable:
    """
    A decorator for replacing a function in another module

    Example:
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

    Returns: The replaced function
    """
    logger.warning(
        f'function {original_function.__module__}.{original_function.__name__}'
        f'is being replaced (change: {patch_description})')
    __applied_patches.append(Patch(replaces=True,
                                   original_module=original_function.__module__,
                                   original_name=original_function.__name__,
                                   description=patch_description,
                                   patcher_frame=inspect.stack()[0]))

    def decorator(new_function):
        if not isinstance(original_function, typing.Callable):
            raise TypeError("Argument passed to @patch decorator must be a Callable")

        # copy properies such as __doc__, __module__ from original_function to new_function
        functools.update_wrapper(new_function, original_function)

        # replace function
        setattr(sys.modules[original_function.__module__], original_function.__name__, new_function)
        return new_function

    return decorator


def wrap(original_function: typing.Callable, wrap_description: str = '') -> typing.Callable:
    """
    A decorator for wrapping a function in another module

    Example:
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
        patch_description (optional): The description of the patch

    Returns: The wrapped function
    """
    logger.warning(
        f'function {original_function.__module__}.{original_function.__name__}'
        f'is being wrapped (change: {wrap_description})')
    __applied_patches.append(Patch(replaces=False,
                                   original_module=original_function.__module__,
                                   original_name=original_function.__name__,
                                   description=wrap_description,
                                   patcher_frame=inspect.stack()[0]))

    def decorator(new_function):
        if not isinstance(original_function, typing.Callable):
            raise TypeError("Argument passed to @wrap decorator must be a Callable")

        # supply original_function as first argument to new_function
        def wrapper(*args, **kwargs):
            return new_function(original_function, *args, **kwargs)

        # copy properties such as __doc__, __module__ from original_function to the wrapper
        functools.update_wrapper(wrapper, original_function)

        # replace function
        setattr(sys.modules[original_function.__module__], original_function.__name__, wrapper)
        return wrapper

    return decorator


def list_patches():
    """
    List the applied patches, for each one gives a named tuple containing:
     - whether the function was replaced or wrapped
     - name of the module containing the patched function
     - name of the patched function
     - the provided reason for the patch, if any
     - the frame of the caller
    :return:
    """
    return __applied_patches
