from typing import TypeVar, Self, Callable

DataType = TypeVar("DataType")
ErrorTypes = TypeVar("ErrorTypes", bound=Exception)


class Optional[DataType, ErrorTypes]:
    data: DataType | None = None
    error: ErrorTypes | None = None


def build(data: DataType = None, error: ErrorTypes = None):
    obj = Optional[DataType, ErrorTypes]()
    obj.error = error
    obj.data = data
    return obj
