from typing import Any
import ujson


def json_remove(j: Any, path: str) -> Any:
    """
    Removes elements of JSON that match a specific path.
    This returns a brand new JSON object.

    If there are no matches, nothing is removed and no exception is raised.

    Examples:
    - "a" => Removes j['a']
    - "[1]" => Removes j[1]
    - "a.[1]" => Removes j['a'][1]
    - "[1].[a]" => Removes j[1]['a']
    - "a.b" => Removes j['a']['b']
    - "a.*b" => Removes x['b'] from all elements x of j['a']
        - Note that x must be a dict
    - "a.*[1]" => Removes x[1] for all elements x of j['a']
        - Note that x must be a list

    :param j:
        json (list or dict)
    :param path:
        A string that specifies what should be removed from the JSON
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
                break
        elif token.startswith('*'):
            raise Exception('* must only be used as the final token of a path')
        else:
            try:
                j = j[token]
            except Exception:
                break
    else:
        token = tokens[-1]
        if token.startswith('['):
            i = int(token[1:-1])
            try:
                if isinstance(j, list):
                    del j[i]
            except Exception:
                pass
        elif token.startswith('*'):
            if isinstance(j, list):
                if token[1] == '[':
                    i = int(token[2:-1])
                    for item in j:
                        try:
                            if isinstance(item, list):
                                del item[i]
                        except Exception:
                            pass
                else:
                    token = token[1:]
                    for item in j:
                        if isinstance(item, dict):
                            if token in item:
                                del item[token]
        else:
            try:
                del j[token]
            except Exception:
                pass

    return orig


def json_update(j: Any, path: str, value: Any) -> Any:
    """
    Updates elements of JSON that match a specific path.
    This returns a brand new JSON object.

    If there are no matches, nothing is updated/added and no exception is raised.

    Examples:
    - "a" => Updates j['a'] or adds if it doesn't exist
    - "[1]" => Updates j[1]
    - "a.[1]" => Updates j['a'][1]
    - "[1].a" => Updates j[1]['a'] or adds if it doesn't exist
        - Note that j[1] will not get added automatically if it does not exist
    - "a.b" => Updates j['a']['b'] or adds if it doesn't exist
        - Note that j['a'] will not get added automatically if it does not exist
    - "a.*b" => Update x['b'] (or adds if it doesn't exist) for all elements x of j['a']
        - Note that x must be a dict
    - "a.*[1]" => Updates x[1] for all elements x of j['a']
        - Note that x must be a list

    :param j:
        json (list or dict)
    :param path:
        A string that specifies what should be removed from the JSON
    :param value:
        The value to set for the element(s) specified by `path`
    :return:
        new JSON object with elements updated
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
                break
        elif token.startswith('*'):
            raise Exception('* must only be used as the final token of a path')
        else:
            try:
                j = j[token]
            except Exception:
                break
    else:
        token = tokens[-1]
        if token.startswith('['):
            i = int(token[1:-1])
            try:
                if isinstance(j, list):
                    j[i] = value
            except Exception:
                pass
        elif token.startswith('*'):
            if isinstance(j, list):
                if token[1] == '[':
                    i = int(token[2:-1])
                    for item in j:
                        try:
                            if isinstance(item, list):
                                item[i] = value
                        except Exception:
                            pass
                else:
                    token = token[1:]
                    for item in j:
                        if isinstance(item, dict):
                            item[token] = value
        else:
            try:
                j[token] = value
            except Exception:
                pass

    return orig
