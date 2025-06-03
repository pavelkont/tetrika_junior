def strict(func):
    def output_func(*args):
        try:
            annotations = func.__annotations__
            param_names = func.__code__.co_varnames[:len(args)]

            for name, value in zip(param_names, args):
                expected_type = annotations.get(name)
                if expected_type and not isinstance(value, expected_type):
                    raise TypeError(f"Аргумент '{name}' должет быть {expected_type.__name__}, получен {type(value).__name__}.")
            return func(*args)
        except TypeError as e:
            print(e)
    return output_func

@strict
def sum_two(a: int, b: int) -> int:
    return a + b

print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
