
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


def test_parse_filename_full_path():
    """Parse filename full path"""

    pattern = 'project/{entity}/{task}/{family}/{instance}_{category}.{ext}'
    path = 'project/john/rigging/review/bob_model.ma'
    data = pather.parse(pattern, path)

    assert data == {'entity': 'john',
                    'task': 'rigging',
                    'family': 'review',
                    'instance': 'bob',
                    'category': 'model',
                    'ext': 'ma'}


def test_parse_filename_full_path_static_end():
    """Parse filename full path static end"""

    pattern = 'project/{entity}/{task}/{family}/{instance}_static.{ext}'
    path = 'project/john/rigging/review/bob_static.ma'
    data = pather.parse(pattern, path)

    assert data == {'entity': 'john',
                    'task': 'rigging',
                    'family': 'review',
                    'instance': 'bob',
                    'ext': 'ma'}


def test_parse_filename_static_end():
    """Parse filename static end"""

    pattern = '{instance}_static.{ext}'
    path = 'bob_static.ma'
    data = pather.parse(pattern, path)

    assert data == {'instance': 'bob',
                    'ext': 'ma'}


def test_parse_filename_static_image_sequence():
    """Parse filename static image sequence"""

    pattern = '{name}.0001.{ext}'
    path = 'image_sequence.0001.exr'
    data = pather.parse(pattern, path)

    assert data == {'name': 'image_sequence',
                    'ext': 'exr'}


def test_parse_filename_dynamic_image_sequence():
    """Parse filename dynamic image sequence"""

    pattern = '{name}.{frame}.{ext}'
    path = 'image_sequence.0001.exr'
    data = pather.parse(pattern, path)

    assert data == {'name': 'image_sequence',
                    'frame': '0001',
                    'ext': 'exr'}