import functools


class PipeLine:
    """
    a class representing a pipeline of function
    each function receives one input, which is the output of the previous function in the pipeline
    pipelines are great for representing a long computer vision function (which is why such functions
    are called pipelines)
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

    def __iadd__(self, fun):
        """
        adds a function or pipeline to the end of this pipeline (changes this pipeline, doesn't return a new one)
        :param fun: the function or pipeline
        """
        if isinstance(fun, PipeLine):
            self.functions += fun.functions
        self.functions.append(fun)

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
