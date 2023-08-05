import ctypes
import sys
from typing import TypeVar, Union

from _pointers import add_ref, remove_ref

from .base_pointers import BaseObjectPointer, BasePointer
from .exceptions import InvalidSizeError

T = TypeVar("T")


class Pointer(BaseObjectPointer[T]):
    def __repr__(self) -> str:
        return f"<pointer to {self.type.__name__} object at {str(self)}>"  # noqa

    def __rich__(self):
        return f"<pointer to [green]{self.type.__name__}[/green] object at [cyan]{str(self)}[/cyan]>"  # noqa

    def move(
        self,
        target: Union[T, "BasePointer[T]"],
        *,
        unsafe: bool = False,
    ):
        data = target if isinstance(target, BasePointer) else to_ptr(target)

        if not isinstance(data, BaseObjectPointer):
            raise ValueError(
                "pointer is not pointing to an object",
            )

        if data.type is not self.type:
            raise TypeError(
                f"target object is not the same type (pointer looks at {self.type.__name__}, target is {data.type.__name__})",  # noqa
            )

        deref_a: T = ~data  # type: ignore
        deref_b: T = ~self

        size_a: int = sys.getsizeof(deref_a)
        size_b: int = sys.getsizeof(deref_b)

        if (self._origin_size < size_a) and (not unsafe):
            raise InvalidSizeError(
                f"target size may not exceed current size ({size_a} < {size_b})",  # noqa
            )

        bytes_a = (ctypes.c_ubyte * size_a).from_address(data.ensure())
        bytes_b = (ctypes.c_ubyte * size_b).from_address(self.ensure())

        self.assign(~data)
        ctypes.memmove(bytes_b, bytes_a, len(bytes_a))

    @classmethod
    def make_from(cls, obj: T) -> "Pointer[T]":
        return Pointer(
            id(obj),
            type(obj),
            True,
        )


def to_ptr(obj: T) -> Pointer[T]:
    """Convert an object to a pointer."""
    add_ref(obj)
    ptr = Pointer.make_from(obj)
    remove_ref(obj)
    return ptr
