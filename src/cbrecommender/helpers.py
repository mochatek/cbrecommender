from functools import wraps


def ensure_type(expected_type_classes: list, instance_method=False) -> callable:
    """
    Decorator to raise error if function arguments is not of expected type

    Args:
        `expected_type_classes` (list): List of expected type class

        `instance_method` (bool): Specifies whether decorator is applied on instance method or not. Default if False.

    Raises:
        TypeError: In case of conflict in expected and actual type
    """

    def decorate(function: callable) -> callable:
        @wraps(function)
        def wrapper(*args):
            # Skip first argument (self) if applied on instance method
            for arg, type_class in zip(args if not instance_method else args[1:], expected_type_classes):
                if not isinstance(arg, type_class):
                    raise TypeError(
                        f"Expected type '{type_class.__name__}', got '{arg.__class__.__name__}' instead.")
            return function(*args)
        return wrapper
    return decorate


def remove_spaces(value):
    """
    Removes white spaces from string

    Args:
        value (str): Input string
    """

    return value.lower().replace(' ', '')
