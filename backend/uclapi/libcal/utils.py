import re

NO_CAMEL = ['seat_id']


def underscore(word):
    """
    Make an underscored, lowercase form from the expression in the string.

    Example::

        >>> underscore("DeviceType")
        'device_type'

    As a rule of thumb you can think of :func:`underscore` as the inverse of
    :func:`camelise`, though there are cases where that does not hold::

        >>> camelize(underscore("IOError"))
        'IoError'
    Source: https://github.com/jpvanhal/inflection
    """
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


def underscorer(data):
    """
    Convert all keys in a dictionary to underscore, does not work on recurisve dictionaries

    Example::

        >>> underscore({'deviceType': 'helloWorld'})
        {'device_type': 'helloWorld'}

    """
    if not isinstance(data, dict):
        return data

    new_data = {}
    for k, v in data.items():
        new_data[underscore(k) if isinstance(k, str) else k] = underscorer(
            v) if isinstance(v, dict) else v
    return new_data


def camelise(word, uppercase_first_letter=False):
    """
    Convert strings to CamelCase.

    Examples::

        >>> camelize("device_type")
        'deviceType'
        >>> camelize("device_type", True)
        'DeviceType'

    :func:`camelize` can be thought of as a inverse of :func:`underscore`,
    although there are some cases where that does not hold::

        >>> camelize(underscore("IOError"))
        'IoError'

    :param uppercase_first_letter: if set to `True` :func:`camelize` converts
        strings to UpperCamelCase. If set to `False` :func:`camelize` produces
        lowerCamelCase. Defaults to `False`.
    Source: https://github.com/jpvanhal/inflection
    """
    if uppercase_first_letter:
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), word)
    else:
        return word[0].lower() + camelise(word, True)[1:]


def cameliser(data, special=True):
    """
    Convert all keys in a dictionary to CamelCase (except some specific keys),
    does not work on recurisve dictionaries

    Example::

        >>> underscore({'device_type': 'hello_world'})
        {'deviceType': 'hello_world'}

    """
    if not isinstance(data, dict):
        return data

    new_data = {}
    for k, v in data.items():
        should_camel = isinstance(k, str) and (not special or k not in NO_CAMEL)
        new_data[camelise(k) if should_camel else k] = cameliser(v) if isinstance(v, dict) else v
    return new_data
