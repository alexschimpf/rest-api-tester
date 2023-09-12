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
        actual = utils.json_remove(j={
            'a': {
                'b': {
                    'c': 1
                }
            }
        }, path='a.b.c')
        self.assertDictEqual({
            'a': {
                'b': {}
            }
        }, actual)

    def test_json_remove__3_keys_1_index(self) -> None:
        actual = utils.json_remove(j={
            'a': {
                'b': {
                    'c': [1, 2]
                }
            }
        }, path='a.b.c.[1]')
        self.assertDictEqual({
            'a': {
                'b': {
                    'c': [1]
                }
            }
        }, actual)

    def test_json_remove__3_keys_2_indices(self) -> None:
        actual = utils.json_remove(j={
            'a': {
                'b': {
                    'c': [1, [2, 3]]
                }
            }
        }, path='a.b.c.[1].[1]')
        self.assertDictEqual({
            'a': {
                'b': {
                    'c': [1, [2]
                          ]
                }
            }
        }, actual)

    def test_json_remove__1_index(self) -> None:
        actual = utils.json_remove(j=[1, 2, 3], path='[0]')
        self.assertListEqual([2, 3], actual)

    def test_json_remove__1_index_1_key(self) -> None:
        actual = utils.json_remove(j=[
            {
                'a': 1,
                'b': 2
            },
            2,
            3
        ], path='[0].a')
        self.assertListEqual([
            {
                'b': 2
            },
            2,
            3
        ], actual)

    def test_json_remove__star_key(self) -> None:
        actual = utils.json_remove(j=[
            {
                'a': 1,
                'b': 2
            },
            {
                'a': 3
            },
            4,
            {
                'c': 5
            }
        ], path='*a')
        self.assertListEqual([
            {
                'b': 2
            },
            {},
            4,
            {
                'c': 5
            }
        ], actual)

    def test_json_remove__1_index_star_key(self) -> None:
        actual = utils.json_remove(j=[
            100, [
                {
                    'a': 1,
                    'b': 2
                },
                {
                    'a': 3
                },
                4,
                {
                    'c': 5
                }
            ]
        ], path='[1].*a')
        self.assertListEqual([
            100,
            [
                {
                    'b': 2
                },
                {},
                4,
                {
                    'c': 5
                }
            ]
        ], actual)

    def test_json_remove__1_key_star_key(self) -> None:
        actual = utils.json_remove(j={
            'z': [
                {
                    'a': 1,
                    'b': 2
                },
                {
                    'a': 3
                },
                4,
                {
                    'c': 5
                }
            ],
            'y': 4
        }, path='z.*a')
        self.assertDictEqual({
            'z': [
                {
                    'b': 2
                },
                {},
                4,
                {
                    'c': 5
                }
            ],
            'y': 4
        }, actual)

    def test_json_remove__1_key_star_index(self) -> None:
        actual = utils.json_remove(j={
            'z': [
                [1, 2],
                [3, 4],
                4,
                {
                    'c': 5
                }
            ],
            'y': 4
        }, path='z.*[0]')
        self.assertDictEqual({
            'z': [
                [2],
                [4],
                4,
                {
                    'c': 5
                }
            ],
            'y': 4
        }, actual)

    def test_json_remove__key_with_list(self) -> None:
        actual = utils.json_remove(j=[1, 2, 3], path='a')
        self.assertListEqual([1, 2, 3], actual)

    def test_json_remove__index_with_dict(self) -> None:
        actual = utils.json_remove(j={'a': 1}, path='[0]')
        self.assertDictEqual({'a': 1}, actual)

    def test_json_update__empty_dict(self) -> None:
        actual = utils.json_update(j={}, path='a.b.c', value=123)
        self.assertDictEqual({}, actual)

    def test_json_update__empty_dict_updated(self) -> None:
        actual = utils.json_update(j={}, path='a', value=123)
        self.assertDictEqual({'a': 123}, actual)

    def test_json_update__1_key(self) -> None:
        actual = utils.json_update(j={'a': 1}, path='a', value=2)
        self.assertDictEqual({'a': 2}, actual)

    def test_json_update__3_keys(self) -> None:
        actual = utils.json_update(j={
            'a': {
                'b': {
                    'c': 1
                }
            }
        }, path='a.b.c', value=2)
        self.assertDictEqual({
            'a': {
                'b': {
                    'c': 2
                }
            }
        }, actual)

    def test_json_update__3_keys_1_index(self) -> None:
        actual = utils.json_update(j={
            'a': {
                'b': {
                    'c': [1, 2]
                }
            }
        }, path='a.b.c.[1]', value=3)
        self.assertDictEqual({
            'a': {
                'b': {
                    'c': [1, 3]
                }
            }
        }, actual)

    def test_json_update__3_keys_2_indices(self) -> None:
        actual = utils.json_update(j={
            'a': {
                'b': {
                    'c': [1, [2, 3]]
                }
            }
        }, path='a.b.c.[1].[1]', value=4)
        self.assertDictEqual({
            'a': {
                'b': {
                    'c': [1, [2, 4]]
                }
            }
        }, actual)

    def test_json_update__1_index(self) -> None:
        actual = utils.json_update(j=[1, 2, 3], path='[0]', value=0)
        self.assertListEqual([0, 2, 3], actual)

    def test_json_update__1_index_1_key(self) -> None:
        actual = utils.json_update(j=[
            {
                'a': 1,
                'b': 2
            },
            2, 3
        ], path='[0].a', value=4)
        self.assertListEqual([
            {
                'a': 4,
                'b': 2
            },
            2,
            3
        ], actual)

    def test_json_update__star_key(self) -> None:
        actual = utils.json_update(j=[
            {
                'a': 1,
                'b': 2
            },
            {
                'a': 3
            },
            4,
            {
                'c': 5
            }
        ], path='*a', value=123)
        self.assertListEqual([
            {
                'a': 123,
                'b': 2
            },
            {
                'a': 123
            },
            4,
            {
                'c': 5,
                'a': 123
            }
        ], actual)

    def test_json_update__star_key_2(self) -> None:
        actual = utils.json_update(j=[
            {
                'a': 1
            },
            {
                'a': 2
            }
        ], path='*b', value=123)
        self.assertListEqual([
            {
                'a': 1,
                'b': 123
            },
            {
                'a': 2,
                'b': 123
            }
        ], actual)

    def test_json_update__1_index_star_key(self) -> None:
        actual = utils.json_update(j=[
            100,
            [
                {
                    'a': 1,
                    'b': 2
                },
                {
                    'a': 3
                },
                4,
                {
                    'c': 5
                }
            ]
        ], path='[1].*a', value=123)
        self.assertListEqual([
            100,
            [
                {
                    'a': 123,
                    'b': 2
                },
                {
                    'a': 123
                },
                4,
                {
                    'c': 5,
                    'a': 123
                }
            ]
        ], actual)

    def test_json_update__1_key_star_key(self) -> None:
        actual = utils.json_update(j={
            'z': [
                {
                    'a': 1,
                    'b': 2
                },
                {
                    'a': 3
                },
                4,
                {
                    'c': 5
                }
            ],
            'y': 4
        }, path='z.*a', value=123)
        self.assertDictEqual({
            'z': [
                {
                    'a': 123,
                    'b': 2
                },
                {
                    'a': 123
                },
                4,
                {
                    'c': 5,
                    'a': 123
                }
            ],
            'y': 4
        }, actual)

    def test_json_update__1_key_star_index(self) -> None:
        actual = utils.json_update(j={
            'z': [
                [1, 2],
                [3, 4],
                4,
                {
                    'c': 5
                }
            ],
            'y': 4
        }, path='z.*[0]', value=123)
        self.assertDictEqual({
            'z': [
                [123, 2],
                [123, 4],
                4,
                {
                    'c': 5
                }
            ],
            'y': 4
        }, actual)

    def test_json_update__1_missing_key_star_key(self) -> None:
        actual = utils.json_update(j={
            'a': [
                {
                    'b': 1
                }
            ]
        }, path='c.*a', value=123)
        self.assertDictEqual({
            'a': [
                {
                    'b': 1
                }
            ]
        }, actual)

    def test_json_update__key_with_list(self) -> None:
        actual = utils.json_update(j=[1, 2, 3], path='a', value=4)
        self.assertListEqual([1, 2, 3], actual)

    def test_json_update__index_with_dict(self) -> None:
        actual = utils.json_update(j={'a': 1}, path='[0]', value=2)
        self.assertDictEqual({'a': 1}, actual)
