
from nose.tools import assert_raises
import pather
import pather.error


def test_full_parse():
    """Simple full parse"""

    pattern = 'project/{entity}/{task}/{family}'
    path = 'project/john/rigging/review'
    data = pather.parse(pattern, path)

    assert data == {'entity': 'john',
                    'task': 'rigging',
                    'family': 'review'}


def test_invalid_parse():
    """Test invalid parse"""

    pattern = 'project/{entity}/{task}/{family}'

    with assert_raises(pather.error.ParseError):
        path = 'project/john/review'
        pather.parse(pattern, path)

    with assert_raises(pather.error.ParseError):
        path = 'a'
        pather.parse(pattern, path)

    with assert_raises(pather.error.ParseError):
        path = 'a/entity/task/family'
        pather.parse(pattern, path)

    with assert_raises(pather.error.ParseError):
        path = 'a/entity/task/family/and/more'
        pather.parse(pattern, path)


def test_format_and_parse():
    """Ensure format and parse are reversable"""

    pattern = 'project/{entity}/{task}/output/{family}'
    data = {'entity': 'john',
            'task': 'rigging',
            'family': 'review'}

    formatted = pather.format(pattern, data)
    parsed = pather.parse(pattern, formatted)
    assert data == parsed

    formatted_again = pather.format(pattern, parsed)
    assert formatted == formatted_again