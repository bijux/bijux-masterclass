from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
from typing import Any, TypeVar


ClassT = TypeVar("ClassT", bound=type[Any])
_READY_ATTRIBUTE = "_surface_frozen_ready"


class FrozenSurfaceError(AttributeError):
    """Reject ordinary attribute rebinding or deletion after initialization."""


@dataclass(frozen=True, slots=True)
class FrozenSurfacePolicy:
    """The deliberately narrow promise installed by ``surface_frozen``."""

    blocks_rebinding: bool = True
    blocks_deletion: bool = True
    deeply_immutable: bool = False
    object_setattr_can_bypass: bool = True
    subclass_can_override_boundary: bool = True


def surface_frozen(cls: ClassT) -> ClassT:
    """Freeze ordinary instance attribute operations after successful initialization."""

    if "__surface_frozen__" in vars(cls) or _READY_ATTRIBUTE in vars(cls):
        raise TypeError(f"{cls.__name__} collides with surface_frozen state")
    if getattr(cls, "__dictoffset__", 0) == 0:
        raise TypeError("surface_frozen requires instances with a __dict__")

    original_init = cls.__init__
    original_setattr = cls.__setattr__
    original_delattr = cls.__delattr__

    @wraps(original_init)
    def initialize(self: object, *args: object, **kwargs: object) -> None:
        object.__setattr__(self, _READY_ATTRIBUTE, False)
        original_init(self, *args, **kwargs)
        object.__setattr__(self, _READY_ATTRIBUTE, True)

    def frozen_setattr(self: object, name: str, value: object) -> None:
        if vars(self).get(_READY_ATTRIBUTE, False):
            raise FrozenSurfaceError(
                f"{type(self).__name__} blocks attribute rebinding after initialization"
            )
        original_setattr(self, name, value)

    def frozen_delattr(self: object, name: str) -> None:
        if vars(self).get(_READY_ATTRIBUTE, False):
            raise FrozenSurfaceError(
                f"{type(self).__name__} blocks attribute deletion after initialization"
            )
        original_delattr(self, name)

    cls.__init__ = initialize  # type: ignore[method-assign]
    cls.__setattr__ = frozen_setattr  # type: ignore[method-assign]
    cls.__delattr__ = frozen_delattr  # type: ignore[method-assign]
    cls.__surface_frozen__ = FrozenSurfacePolicy()  # type: ignore[attr-defined]
    return cls
