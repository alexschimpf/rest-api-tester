from typing import Any
import ujson


def json_remove(j: Any, path: str, raise_on_no_match: bool = False) -> Any:
    """
    Removes elements of JSON that match a specific path.
    This returns a brand new JSON object.

    :param j:
        json (list or dict)
    :param path:
        A string that specifies what should be removed from the JSON.
        Examples:
            - "a" => Removes j['a']
            - "[1]" => Removes j[1]
            - "a.[1]" => Removes j['a'][1]
            - "[1].[a]" => Removes j[1]['a']
            - "a.b" => Removes j['a']['b']
            - "a.*b" => Removes the key "b" from all elements of j['a']
    :param raise_on_no_match:
        If no element is found that matches the path, an exception will be raised
    :return:
        new JSON object with elements removed
    """

    if not path:
        raise Exception('Path cannot be empty')

    tokens = path.split('.')

    j = ujson.loads(ujson.dumps(j))
    orig = j

    for token in tokens[:-1]:
        if token.startswith('['):
            i = int(token[1:-1])
            try:
                j = j[i]
            except Exception:
                if raise_on_no_match:
                    raise Exception(f'No matches on path: {path}')
                break
        elif token.startswith('*'):
            raise Exception('* must only be used as the final token of a path')
        else:
            try:
                j = j[token]
            except Exception:
                if raise_on_no_match:
                    raise Exception(f'No matches on path: {path}')
                break
    else:
        token = tokens[-1]
        if token.startswith('['):
            i = int(token[1:-1])
            try:
                del j[i]
            except Exception:
                if raise_on_no_match:
                    raise Exception(f'No matches on path: {path}')
        elif token.startswith('*'):
            matched = False
            token = token[1:]
            for item in j:
                if isinstance(item, dict):
                    if token in item:
                        matched = True
                        del item[token]
            if not matched:
                raise Exception(f'No matches on path: {path}')
        else:
            try:
                del j[token]
            except Exception:
                if raise_on_no_match:
                    raise Exception(f'No matches on path: {path}')

    return orig
