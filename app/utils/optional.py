from typing import TypeVar, Self, Callable

DataType = TypeVar("DataType")
ErrorTypes = TypeVar("ErrorTypes", bound=Exception)


class Optional[DataType, ErrorTypes]:
    data: DataType | None = None
    error: ErrorTypes | None = None

    def unwrap(self):
        if self.error:
            raise self.error
        return self.data


def build(data: DataType = None, error: ErrorTypes = None) -> Optional[DataType, ErrorTypes]:
    obj = Optional[DataType, ErrorTypes]()
    obj.error = error
    obj.data = data
    return obj
