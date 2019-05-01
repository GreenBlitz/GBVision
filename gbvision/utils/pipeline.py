import functools


class PipeLine:
    """
    a class representing a pipeline of function
    each function receives one input, which is the output of the previous function in the pipeline
    pipelines are great for representing a long computer vision function (which is why such functions
    are called pipelines)
    the PipeLine class can also be used as a function decorator
    for example, creating a pipeline that adds 1 to it's output can be done in two ways:
    inc = PipeLine(lambda x: x + 1)
    or
    @PipeLine
    def inc(x):
        return x + 1
    when inheriting from the PipeLine class (to make a pipeline factory), the subclass cannot have any attributes or methods
    so for example, to create a pipeline factory that generates adding functions:
    this will not work:
    class Adder(PipeLine):
        def __init__(self, num):
            self.num = num
            PipeLine.__init__(self, self.adding_func)
        def adding_func(self, item):
            return item + self.num
    instead we will implement it as follows:
    class Adder(PipeLine):
        def __init__(self, num):
            def adding_func(item):
                return item + num
            PipeLine.__init__(self, adding_func)
    """
    def __init__(self, *functions):
        """
        initializes this pipeline
        :param functions: a tuple of functions to run one after the other as a pipeline
        """
        self.functions = list(functions)

    def __call__(self, image):
        """
        activate this pipeline and return the result
        :param image: the input to the first function in the pipeline (also the input to the entire pipeline)
        doesn't have to be an image, can be anything
        :return: the output of the last function in the pipeline, can be data type
        """
        return functools.reduce(lambda x, f: f(x), self.functions, image)

    def __add__(self, other):
        """
        creates a new pipeline which uses the output of this pipeline as input to the other pipeline
        :param other: the second pipeline
        :return: a new pipeline, and calling this pipeline with the parameter image is similar to
        performing other(self(image))
        """
        if isinstance(other, PipeLine):
            return PipeLine(*self.functions + other.functions)
        return PipeLine(*self.functions + [other])

    def __radd__(self, other):
        """
        adds this PipeLine to another function that isn't a PipeLine
        :param other: the function
        :return: a new PipeLine which performs self(other(image)) on the parameter image
        """
        return PipeLine(other) + self

    def __iadd__(self, fun):
        """
        adds a function or pipeline to the end of this pipeline (changes this pipeline, doesn't return a new one)
        :param fun: the function or pipeline
        """
        if isinstance(fun, PipeLine):
            self.functions += fun.functions
        self.functions.append(fun)
        return self

    def __getitem__(self, item):
        """
        gets the function at index item
        :param item: the index
        :return: the item
        """
        return self.functions[item]

    def __setitem__(self, key, value):
        """
        sets the function at index key to the new function value
        :param key: the index
        :param value: the new function
        """
        self.functions[key] = value

    def __iter__(self):
        """
        :return: an iterator that iterates through all functions in this pipeline
        """
        return iter(self.functions)
