from typing import Any, Callable, Iterable, Optional
import functools


class PipeLine:
    """
    A class representing a pipeline of function
    each function receives one input, which is the output of the previous function in the pipeline
    pipelines are great for representing a long computer vision function (which is why such functions
    are called pipelines).
    the PipeLine class can also be used as a function decorator
    for example, creating a pipeline that adds 1 to it's output can be done in two ways:
    Example::
        inc = PipeLine(lambda x: x + 1)
        three = inc(2)

    or
    Example::
        @PipeLine
        def inc(x):
            return x + 1
        three = inc(2)


    You can create a PipeLine from multiple functions:
    Example::
        open_and_read_file = PipeLine(open, lambda x: x.read())
        text = open_and_read_file("file.txt")

    You can also inherit from the PipeLine class to make a PipeLine factory:
    Example::
        class Adder(PipeLine):
            def __init__(self, num):
                self.num = num
                PipeLine.__init__(self, self.adding_func)
            def adding_func(self, item):
                return item + self.num

    You can also do it like this:
    Example::
        class Adder(PipeLine):
            def __init__(self, num):
                def adding_func(item):
                    return item + num

                PipeLine.__init__(self, adding_func)

    You can use combine a few PipeLines together to create function composition:
    Example::
        multiply_by_2_then_add_3 = PipeLine(lambda x: x * 2) + PipeLine(lambda x: x + 3)

    :param functions: A tuple of functions to run one after the other as a pipeline
    :param qualname: Optional. A string that will be the __qualname__ of the pipeline object
    :param module: Optional. A string that will be the __module__ of the pipeline object
    """
    __NO_DOCS = '\n\tNo Docs :('

    @staticmethod
    def __get_qual_name(func: Callable[[Any], Any]) -> str:
        return func.__qualname__ if hasattr(func, '__qualname__') else 'Unknown Function'

    def __init__(self, *functions: Callable[[Any], Any], qualname: Optional[str] = None, module: Optional[str] = None):
        self.functions = []
        for f in functions:
            if isinstance(f, PipeLine):
                self.functions += f.functions
            else:
                self.functions.append(f)

        # set qual name
        if qualname is not None:
            self.__qualname__ = qualname
        if len(functions) == 1:
            if hasattr(functions[0], '__qualname__'):
                self.__qualname__ = functions[0].__qualname__
        elif len(functions) > 1:
            self.__qualname__ = ' + '.join(self.__get_qual_name(func) for func in functions) or None

        # set module
        if module is not None:
            self.__module__ = module
        if len(functions) == 1:
            if hasattr(functions[0], '__module__'):
                self.__module__ = functions[0].__module__
        elif len(functions) > 1:
            all_modules = set(x.__module__ for x in functions if hasattr(x, '__module__'))
            if len(all_modules) == 1:
                self.__module__ = next(iter(all_modules))

        # set doc
        if len(functions) == 1:
            self.__doc__ = functions[0].__doc__
        elif len(functions) > 1:
            all_docs = []
            for i, func in enumerate(functions):
                all_docs.append(f'{i}. {self.__get_qual_name(func)}\n{func.__doc__ or self.__NO_DOCS}')
            self.__doc__ = '\n\n'.join(all_docs)

    def __call__(self, image: Any) -> Any:
        """
        Activate this pipeline and return the result

        :param image: The input to the first function in the pipeline (also the input to the entire pipeline) \
        doesn't have to be an image, can be anything
        :return: The output of the last function in the pipeline, can be data type
        """
        return functools.reduce(lambda x, f: f(x), self.functions, image)

    def __add__(self, other: Callable[[Any], Any]) -> 'PipeLine':
        """
        Creates a new pipeline which uses the output of this pipeline as input to the other pipeline

        :param other: The second pipeline
        :return: A new pipeline, and calling this pipeline with the parameter image is similar to \
        performing other(self(image))
        """
        if isinstance(other, PipeLine):
            return PipeLine(*self.functions + other.functions)
        return PipeLine(*self.functions + [other])

    def __radd__(self, other: Callable[[Any], Any]) -> 'PipeLine':
        """
        Adds this PipeLine to another function that isn't a PipeLine

        :param other: The function
        :return: A new PipeLine which performs self(other(image)) on the parameter image
        """
        return PipeLine(other) + self

    def __getitem__(self, item: int) -> Callable[[Any], Any]:
        """
        Gets the function at index item

        :param item: The index
        :return: The item
        """
        return self.functions[item]

    def __setitem__(self, key: int, value: Callable[[Any], Any]) -> None:
        """
        Sets the function at index key to the new function value

        :param key: The index
        :param value: The new function
        """
        self.functions[key] = value

    def __iter__(self) -> Iterable[Callable[[Any], Any]]:
        """
        :return: An iterator that iterates through all functions in this pipeline
        """
        return iter(self.functions)

    def __len__(self):
        """
        :return: The amount of functions in this pipeline
        """
        return len(self.functions)
