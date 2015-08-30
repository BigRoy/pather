
__all__ = ['parse', 'ls', 'ls_iter', 'format']

import os
import re
import string
import glob

from .error import ParseError

# Regex pattern that matches valid file
# TODO: Implement complete pattern if required
RE_FILENAME = '[-\w.,; \[\]]'


def format(pattern, data, allow_partial=True):
    """Format a pattern with a set of data"""

    assert isinstance(data, dict)

    if not all(isinstance(value, str) for value in data.values()):
        raise TypeError("The values in the data "
                        "dictionary must be strings")

    if allow_partial:
        return _partial_format(pattern, data)
    else:
        return pattern.format(**data)


def parse(pattern, path):
    """Parse data from a path based on a pattern

    Example:
    >>> pattern = "root/{task}/{version}/data/"
    >>> path = "root/modeling/v001/data/"
    >>> path_parse(pattern, path)
    >>> # {'task': 'modeling', 'version': 'v001'}
    """

    pattern = os.path.normpath(pattern)
    path = os.path.normpath(path)

    # force forward slashes
    path = path.replace('\\', '/')
    pattern = pattern.replace('\\', '/')

    # Escape characters in path that are regex patterns so they are
    # excluded by the regex searches. Exclude '{' and '}' in escaping.
    pattern = re.escape(pattern)
    pattern = pattern.replace('\{', '{').replace('\}', '}')

    keys = re.findall(r'{(%s+)}' % RE_FILENAME,
                      pattern)
    if not keys:
        return []

    # find the corresponding values
    value_pattern = re.sub(r'{(%s+)}' % RE_FILENAME,
                           r'(%s+)' % RE_FILENAME,
                           pattern)
    match_values = re.match(value_pattern, path)

    if not match_values:
        raise ParseError("Path doesn't match with pattern. No values parsed")

    values = match_values.groups()

    return dict(zip(keys, values))


def ls_iter(pattern, data=None, with_matches=False):
    """Yield all matches for the given pattern.

    If the pattern starts with a relative path (or a dynamic key) the search
    will start from the current working directory, defined by os.path.realpath.

    Arguments:
        pattern (str): The pattern to match and search against.
        data (dict): A dictionary of data to format the pattern by before
            starting the query. With this you can reduce or point the query
            to a specific subset of the rule.

    Example:
    >>> import os
    >>> data = {"root": os.path.expanduser("~"), "content": "cache"}
    >>> path_ls("{root}/{project}/data/{content}/")
    """

    # format rule by data already provided to reduce query
    if data is not None:
        pattern = format(pattern, data, allow_partial=True)

    pattern = os.path.expandvars(pattern)
    pattern = os.path.realpath(pattern)

    glob_pattern = re.sub(r'([/\\]{\w+}[/\\])', '/*/', pattern)     # folder
    glob_pattern = re.sub(r'({\w+})', '*', glob_pattern)          # filename

    for path in glob.iglob(glob_pattern):
        path = os.path.realpath(path)
        if with_matches:
            data = parse(pattern, path)
            yield path, data
        else:
            yield path


def ls(pattern, data=None, with_matches=False):
    return list(ls_iter(pattern, data, with_matches=with_matches))


def _partial_format(s, data):
    """Return string `s` formatted by `data` allowing a partial format

    Arguments:
        s (str): The string that will be formatted
        data (dict): The dictionary used to format with.

    Example:
    >>> partial_format("{d} {a} {b} {c} {d}", {'b': "and", 'c': "left"})
    >>> # "left {a} and {c} left"
    """

    class FormatDict(dict):
        def __missing__(self, key):
            return "{" + key + "}"

    formatter = string.Formatter()
    mapping = FormatDict(**data)
    return formatter.vformat(s, (), mapping)