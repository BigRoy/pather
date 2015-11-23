
from nose.tools import assert_raises
import pather
import pather.error


def test_format_full():
    """Format_full"""

    pattern = 'project/{entity}/{task}/{family}'
    data = {'entity': 'john',
            'task': 'rigging',
            'family': 'review'}

    formatted = pather.format(pattern, data)
    assert formatted == 'project/john/rigging/review'


def test_format_partial():
    """Format partial"""

    pattern = 'project/{entity}/{task}/{family}'
    data = {'entity': 'john',
            'family': 'review'}

    formatted = pather.format(pattern, data)
    assert formatted == 'project/john/{task}/review'


def test_format_invalid_type_exception():
    """Format invalid data value raises TypeError"""

    pattern = 'project/{entity}/{task}/{family}'
    data = {'entity': None}

    with assert_raises(TypeError):
        pather.format(pattern, data)


def test_format_unicode():
    """Format pattern and data allows unicode"""

    pattern = unicode('project/{entity}/{task}/{family}')
    data = {unicode('entity'): unicode('john'),
            unicode('family'): unicode('review')}

    formatted = pather.format(pattern, data)
    assert formatted == 'project/john/{task}/review'