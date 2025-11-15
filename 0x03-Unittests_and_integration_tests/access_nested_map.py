def access_nested_map(nested_map : dict , path : tuple) -> int :
    """Access a nested map using a tuple path and return the value.

    Args:
        nested_map (dict): The dictionary to access.
        path (tuple): Tuple of keys to follow in the nested map.

    Returns:
        The value found at the specified path.

    Raises:
        KeyError: If any key in the path is not found.
    """
    current = nested_map
    for key in path:
        if not isinstance(current, dict) or key not in current:
            raise KeyError(key)
        elif key in current:
            current = current[key]
        else:
            raise KeyError(key)
    return current
