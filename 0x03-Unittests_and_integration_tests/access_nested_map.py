def access_nested_map(nested_map : dict , path : tuple) -> int :
    current = nested_map
    for key in path:
        if not isinstance(current, dict) or key not in current:
            raise KeyError(key)
        elif key in current:
            current = current[key]
        else:
            raise KeyError(key)
    return current
