import os
import tempfile
import shutil
import errno

from nose.tools import assert_raises
import pather


class TestLs(object):

    @classmethod
    def setup_class(cls):

        cls.directory = tempfile.mkdtemp()
        cls.pattern = 'project/assets/{item}/{task}/published/{version}/'

        # Set current root directory
        os.chdir(cls.directory)

        paths = ['project/assets/ben/modeling/published/v01/',
                 'project/assets/ben/modeling/published/v02/',
                 'project/assets/ben/modeling/published/v03/',
                 'project/assets/ben/animation/published/v01/',
                 'project/assets/ben/animation/published/v02/',
                 'project/assets/ben/rigging/published/v01/',

                 'project/assets/joe/modeling/published/v01/',
                 'project/assets/joe/modeling/published/v02/',
                 'project/assets/joe/groom/published/v01/',

                 'project/assets/claire/modeling/published/v01/',
                 'project/assets/claire/modeling/work/maya/',
                 'project/assets/claire/modeling/data/what/is/in/here/',
                 'project/assets/claire/modeling/published/v02/']

        for path in paths:
            full_tree = os.path.join(cls.directory, path)
            if not os.path.exists(full_tree):
                os.makedirs(full_tree)

    @classmethod
    def teardown_class(cls):
        pass
        # try:
        #     shutil.rmtree(cls.directory)
        # except OSError as exc:
        #     # ENOENT - no such file or directory
        #     if exc.errno != errno.ENOENT:
        #         raise  # re-raise exception

    def _in_tmpdir(self, paths):
        paths = [os.path.join(self.directory, path) for path in paths]
        paths = [os.path.realpath(path) for path in paths]
        return paths

    def test_ls_no_data(self):
        """Ls full query without any data provided to the pattern"""

        expected_matches = [
            'project/assets/ben/modeling/published/v01/',
            'project/assets/ben/modeling/published/v02/',
            'project/assets/ben/modeling/published/v03/',
            'project/assets/ben/animation/published/v01/',
            'project/assets/ben/animation/published/v02/',
            'project/assets/ben/rigging/published/v01/',

            'project/assets/joe/modeling/published/v01/',
            'project/assets/joe/modeling/published/v02/',
            'project/assets/joe/groom/published/v01/',

            'project/assets/claire/modeling/published/v01/',
            'project/assets/claire/modeling/published/v02/'
        ]
        expected_matches = self._in_tmpdir(expected_matches)

        matches = pather.ls(self.pattern)

        # Compare on contents: http://stackoverflow.com/q/8866652/1838864
        assert set(expected_matches) == set(matches)

    def test_ls_data(self):
        """Ls a set of queries with different data provided"""

        # match only item 'claire'
        expected_matches = [
            'project/assets/claire/modeling/published/v01/',
            'project/assets/claire/modeling/published/v02/'
        ]
        expected_matches = self._in_tmpdir(expected_matches)

        matches = pather.ls(self.pattern,
                            include={'item': 'claire'})
        assert set(expected_matches) == set(matches)

        # match only item 'claire' and version 'v02'
        expected_matches = [
            'project/assets/claire/modeling/published/v02/'
        ]
        expected_matches = self._in_tmpdir(expected_matches)

        matches = pather.ls(self.pattern,
                            include={'item': 'claire',
                                     'version': 'v02'})
        assert set(expected_matches) == set(matches)

        # no match
        matches = pather.ls(self.pattern,
                            include={'item': 'd'})
        assert matches == []

        # no match (empty string)
        matches = pather.ls(self.pattern,
                            include={'item': ''})
        assert matches == []

    def test_ls_data_type_exception(self):
        """Ls invalid data values type exception raised"""

        with assert_raises(TypeError):
            pather.ls(self.pattern,
                      include={'item': None})

        with assert_raises(TypeError):
            pather.ls(self.pattern,
                      include={'item': True})

        with assert_raises(TypeError):
            pather.ls(self.pattern,
                      include={'item': 1})

        with assert_raises(TypeError):
            pather.ls(self.pattern,
                      include={'item': object()})


class TestLsDotted(object):

    @classmethod
    def setup_class(cls):

        cls.directory = tempfile.mkdtemp()
        cls.pattern = 'test/{a}.dotted.{b}/{c}.{d}.{e}/{f}.{ext}'

        # Set current root directory
        os.chdir(cls.directory)

        paths = ['test/folder.dotted.here/so.many.dots/testing.extension']

        for path in paths:
            full_tree = os.path.join(cls.directory, path)
            if not os.path.exists(full_tree):
                os.makedirs(full_tree)

    @classmethod
    def teardown_class(cls):
        pass
        # try:
        #     shutil.rmtree(cls.directory)
        # except OSError as exc:
        #     # ENOENT - no such file or directory
        #     if exc.errno != errno.ENOENT:
        #         raise  # re-raise exception

    def _in_tmpdir(self, paths):
        paths = [os.path.join(self.directory, path) for path in paths]
        paths = [os.path.realpath(path) for path in paths]
        return paths

    def test_ls_dotted(self):
        """Ls dotted"""

        expected_matches = [
            'test/folder.dotted.here/so.many.dots/testing.extension'
        ]
        expected_matches = self._in_tmpdir(expected_matches)

        matches = pather.ls(self.pattern)
        assert set(expected_matches) == set(matches)

    def test_ls_dotted_data_full(self):
        """Ls dotted with data full"""

        expected_matches = [
            'test/folder.dotted.here/so.many.dots/testing.extension'
        ]
        expected_matches = self._in_tmpdir(expected_matches)

        include = {'a': 'folder',
                   'b': 'here',
                   'c': 'so',
                   'd': 'many',
                   'e': 'dots',
                   'f': 'testing',
                   'ext': 'extension'}

        matches = pather.ls(self.pattern, include=include)

        assert set(expected_matches) == set(matches)

    def test_ls_dotted_data_partial(self):
        """Ls dotted with data partial"""

        expected_matches = [
            'test/folder.dotted.here/so.many.dots/testing.extension'
        ]
        expected_matches = self._in_tmpdir(expected_matches)

        include = {'a': 'folder',
                   'b': 'here',
                   'd': 'many',
                   'e': 'dots',
                   'f': 'testing'}

        matches = pather.ls(self.pattern, include=include)

        assert set(expected_matches) == set(matches)

    def test_ls_dotted_with_matches(self):
        """Ls dotted with matches"""

        results = pather.ls(self.pattern, with_matches=True)
        path, match_data = results[0]

        expected_data = {'a': 'folder',
                         'b': 'here',
                         'c': 'so',
                         'd': 'many',
                         'e': 'dots',
                         'f': 'testing',
                         'ext': 'extension'}

        assert expected_data == match_data