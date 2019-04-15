import functools


class PipeLine:
    def __init__(self, *functions):
        self.functions = list(functions)

    def __call__(self, image):
        return functools.reduce(lambda x, f: f(x), self.functions, image)

    def __add__(self, other):
        if isinstance(other, PipeLine):
            return PipeLine(*self.functions + other.functions)
        return PipeLine(*self.functions + [other])

    def __iadd__(self, fun):
        if isinstance(fun, PipeLine):
            self.functions += fun.functions
        self.functions.append(fun)

    def __getitem__(self, item):
        return self.functions[item]

    def __setitem__(self, key, value):
        self.functions[key] = value
