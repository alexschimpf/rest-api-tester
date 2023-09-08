import unittest

from rest_api_tester import utils


class TestUtils(unittest.TestCase):

    def test_json_remove__empty_dict(self) -> None:
        actual = utils.json_remove(j={}, path='a.b.c')
        self.assertDictEqual({}, actual)

    def test_json_remove__1_key(self) -> None:
        actual = utils.json_remove(j={'a': 1}, path='a')
        self.assertDictEqual({}, actual)

    def test_json_remove__3_keys(self) -> None:
        actual = utils.json_remove(j={'a': {'b': {'c': 1}}}, path='a.b.c')
        self.assertDictEqual({'a': {'b': {}}}, actual)

    def test_json_remove__3_keys_1_index(self) -> None:
        actual = utils.json_remove(j={'a': {'b': {'c': [1, 2]}}}, path='a.b.c.[1]')
        self.assertDictEqual({'a': {'b': {'c': [1]}}}, actual)

    def test_json_remove__3_keys_2_indices(self) -> None:
        actual = utils.json_remove(j={'a': {'b': {'c': [1, [2, 3]]}}}, path='a.b.c.[1].[1]')
        self.assertDictEqual({'a': {'b': {'c': [1, [2]]}}}, actual)

    def test_json_remove__1_index(self) -> None:
        actual = utils.json_remove(j=[1, 2, 3], path='[0]')
        self.assertListEqual([2, 3], actual)

    def test_json_remove__1_index_1_key(self) -> None:
        actual = utils.json_remove(j=[{'a': 1, 'b': 2}, 2, 3], path='[0].a')
        self.assertListEqual([{'b': 2}, 2, 3], actual)

    def test_json_remove__star_key(self) -> None:
        actual = utils.json_remove(j=[{'a': 1, 'b': 2}, {'a': 3}, 4, {'c': 5}], path='*a')
        self.assertListEqual([{'b': 2}, {}, 4, {'c': 5}], actual)

    def test_json_remove__1_index_star_key(self) -> None:
        actual = utils.json_remove(j=[100, [{'a': 1, 'b': 2}, {'a': 3}, 4, {'c': 5}]], path='[1].*a')
        self.assertListEqual([100, [{'b': 2}, {}, 4, {'c': 5}]], actual)

    def test_json_remove__1_key_star_key(self) -> None:
        actual = utils.json_remove(j={'z': [{'a': 1, 'b': 2}, {'a': 3}, 4, {'c': 5}], 'y': 4}, path='z.*a')
        self.assertDictEqual({'z': [{'b': 2}, {}, 4, {'c': 5}], 'y': 4}, actual)

    def test_json_remove__key_with_list(self) -> None:
        actual = utils.json_remove(j=[1, 2, 3], path='a')
        self.assertListEqual([1, 2, 3], actual)

    def test_json_remove__index_with_dict(self) -> None:
        actual = utils.json_remove(j={'a': 1}, path='[0]')
        self.assertDictEqual({'a': 1}, actual)

    def test_json_remove__raise_on_no_match(self) -> None:
        with self.assertRaises(Exception):
            utils.json_remove(j={'a': 1}, path='[0]', raise_on_no_match=True)
        with self.assertRaises(Exception):
            utils.json_remove(j=[1, 2, 3], path='a', raise_on_no_match=True)
        with self.assertRaises(Exception):
            utils.json_remove(j=[1, 2, 3], path='[3]', raise_on_no_match=True)
        with self.assertRaises(Exception):
            utils.json_remove(j={'a': 1}, path='b', raise_on_no_match=True)
        with self.assertRaises(Exception):
            utils.json_remove(j=[{'a': 1}, {'a': 2}], path='*b', raise_on_no_match=True)
