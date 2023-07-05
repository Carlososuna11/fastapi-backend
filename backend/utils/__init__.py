import os
import copy
import operator
import secrets
import re
from typing import Any, Union

empty = object()


def get_env(name: str, default: Any = None) -> str:
    """
    Get environment variable.
    :param name: Name of the environment variable.
    :param default: Default value if environment variable is not set.
    :return: Value of environment variable.
    """
    if name in os.environ:
        return os.environ[name]
    return default


def password_file(
        file_env_name: str,
        env_name: str,
        default: Any = None
) -> str:
    """
    Get password from file or environment variable.
    :param file_env_name: Name of the environment variable.
    :param env_name: Name of the environment variable.
    :param default: Default value if environment variable is not set.
    :return: Value of environment variable.
    """
    if file_env_name in os.environ:
        file_name = os.environ[file_env_name]
        if os.path.exists(file_name) and os.access(file_name, os.R_OK):
            with open(file_name, 'r') as f:
                return f.read().strip()
    return get_env(env_name, default)


def bool_from_str(value: str) -> Union[bool, None]:
    """
    Convert string to boolean.
    :param value: String to convert.
    :return: Boolean value.
    """
    if value is None:
        return None
    if value.lower() in ['true', '1', 'yes', 'y', 't', 'True']:
        return True
    elif value.lower() in ['false', '0', 'no', 'n', 'f', 'False']:
        return False
    return None


def unpickle_lazyobject(wrapped):
    """
    Used to unpickle lazy objects. Just return its argument, which will be the
    wrapped object.
    """
    return wrapped


def new_method_proxy(func):
    def inner(self, *args):
        if self._wrapped is empty:
            self._setup()
        return func(self._wrapped, *args)
    return inner


class LazyObject:
    """
    A wrapper for another class that can be used to delay instantiation of the
    wrapped class.

    By subclassing, you have the opportunity to intercept and alter the
    instantiation. If you don't need to do that, use SimpleLazyObject.
    """

    # Avoid infinite recursion when tracing __init__ (#19456).
    _wrapped = None

    def __init__(self):
        # Note: if a subclass overrides __init__(), it will likely need to
        # override __copy__() and __deepcopy__() as well.
        self._wrapped = empty

    __getattr__ = new_method_proxy(getattr)

    def __setattr__(self, name, value):
        if name == "_wrapped":
            # Assign to __dict__ to avoid infinite __setattr__ loops.
            self.__dict__["_wrapped"] = value
        else:
            if self._wrapped is empty:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == "_wrapped":
            raise TypeError("can't delete _wrapped.")
        if self._wrapped is empty:
            self._setup()
        delattr(self._wrapped, name)

    def _setup(self):
        """
        Must be implemented by subclasses to initialize the wrapped object.
        """
        raise NotImplementedError(
            'subclasses of LazyObject must provide a _setup() method')

    # Because we have messed with __class__ below, we confuse pickle as to what
    # class we are pickling. We're going to have to initialize the wrapped
    # object to successfully pickle it, so we might as well just pickle the
    # wrapped object since they're supposed to act the same way.
    #
    # Unfortunately, if we try to simply act like the wrapped object, the ruse
    # will break down when pickle gets our id(). Thus we end up with pickle
    # thinking, in effect, that we are a distinct object from the wrapped
    # object, but with the same __dict__. This can cause problems (see #25389).
    #
    # So instead, we define our own __reduce__ method and custom unpickler. We
    # pickle the wrapped object as the unpickler's argument, so that pickle
    # will pickle it normally, and then the unpickler simply returns its
    # argument.
    def __reduce__(self):
        if self._wrapped is empty:
            self._setup()
        return (unpickle_lazyobject, (self._wrapped,))

    def __copy__(self):
        if self._wrapped is empty:
            # If uninitialized, copy the wrapper. Use type(self), not
            # self.__class__, because the latter is proxied.
            return type(self)()
        else:
            # If initialized, return a copy of the wrapped object.
            return copy.copy(self._wrapped)

    def __deepcopy__(self, memo):
        if self._wrapped is empty:
            # We have to use type(self), not self.__class__, because the
            # latter is proxied.
            result = type(self)()
            memo[id(self)] = result
            return result
        return copy.deepcopy(self._wrapped, memo)

    __bytes__ = new_method_proxy(bytes)
    __str__ = new_method_proxy(str)
    __bool__ = new_method_proxy(bool)

    # Introspection support
    __dir__ = new_method_proxy(dir)

    # Need to pretend to be the wrapped class, for the sake of objects that
    # care about this (especially in equality tests)
    __class__ = property(new_method_proxy(operator.attrgetter("__class__")))
    __eq__ = new_method_proxy(operator.eq)
    __lt__ = new_method_proxy(operator.lt)
    __gt__ = new_method_proxy(operator.gt)
    __ne__ = new_method_proxy(operator.ne)
    __hash__ = new_method_proxy(hash)

    # List/Tuple/Dictionary methods support
    __getitem__ = new_method_proxy(operator.getitem)
    __setitem__ = new_method_proxy(operator.setitem)
    __delitem__ = new_method_proxy(operator.delitem)
    __iter__ = new_method_proxy(iter)
    __len__ = new_method_proxy(len)
    __contains__ = new_method_proxy(operator.contains)


def set_next_prev_url(
    count: int,
    url: str,
    page: int = 0,
    page_size: int = 10,
):
    """
    Set the next and previous urls for a paginated response.
    :param count: Total number of items.
    :param url: Base url.
    :param page: Current page.
    :param page_size: Page size.
    """

    url = str(url).split('?')[0]

    if page > 0:
        prev_page = page - 1
        prev_url = f'{url}?page={prev_page}&page_size={page_size}'
    else:
        prev_url = None
    if page * page_size < count:
        next_page = page + 1
        next_url = f'{url}?page={next_page}&page_size={page_size}'
    else:
        next_url = None
    return prev_url, next_url


RANDOM_STRING_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'  # noqa: E501


def get_random_string(length, allowed_chars=RANDOM_STRING_CHARS):
    """
    Return a securely generated random string.

    The bit length of the returned value can be calculated with the formula:
        log_2(len(allowed_chars)^length)

    For example, with default `allowed_chars` (26+26+10), this gives:
      * length: 12, bit length =~ 71 bits
      * length: 22, bit length =~ 131 bits
    """
    return ''.join(secrets.choice(allowed_chars) for i in range(length))


def validate_url(value: str) -> Union[bool, None]:

    regex = re.compile(
        r'^(?:http)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'    # noqa: E501
        r'localhost|web|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if value is None:
        return None

    if re.match(regex, value) is not None:
        if value.endswith('/'):
            value = value[:-1]
        return value

    raise ValueError(
        'Invalid URL: {}'.format(value),
        'Valid URL examples: http://example.com, https://example.com, '
    )


def path_join(*paths):
    return os.path.join(
        *paths
    )
