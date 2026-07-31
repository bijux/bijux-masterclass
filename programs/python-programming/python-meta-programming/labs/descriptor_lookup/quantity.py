from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Mapping


@dataclass(frozen=True, slots=True)
class QuantitySpec:
    """Review surface for one installed quantity field."""

    name: str
    storage_name: str
    canonical_unit: str
    accepted_units: tuple[str, ...]
    minimum: float | None
    maximum: float | None

    def manifest(self) -> dict[str, object]:
        return {
            **asdict(self),
            "accepted_units": list(self.accepted_units),
        }


@dataclass(frozen=True, slots=True)
class QuantityValue:
    """One canonical quantity read with explicit conversion support."""

    canonical_value: float
    canonical_unit: str
    conversion_factors: tuple[tuple[str, float], ...]

    def in_unit(self, unit: str) -> float:
        factors = dict(self.conversion_factors)
        try:
            factor = factors[unit]
        except KeyError as error:
            raise ValueError(f"unsupported display unit: {unit}") from error
        return self.canonical_value / factor

    def manifest(self) -> dict[str, object]:
        return {
            "canonical_value": self.canonical_value,
            "canonical_unit": self.canonical_unit,
        }


class Quantity:
    """A data descriptor that stores one canonical numeric representation."""

    def __init__(
        self,
        canonical_unit: str,
        conversion_factors: Mapping[str, float],
        *,
        minimum: float | None = None,
        maximum: float | None = None,
    ) -> None:
        factors = dict(conversion_factors)
        if not canonical_unit:
            raise ValueError("canonical_unit cannot be blank")
        if factors.get(canonical_unit) != 1.0:
            raise ValueError("canonical unit must have a conversion factor of 1.0")
        if not factors or any(factor <= 0 for factor in factors.values()):
            raise ValueError("conversion factors must be positive")
        if minimum is not None and maximum is not None and minimum > maximum:
            raise ValueError("minimum cannot exceed maximum")
        self.canonical_unit = canonical_unit
        self.conversion_factors = tuple(factors.items())
        self.minimum = minimum
        self.maximum = maximum
        self.public_name = ""
        self.storage_name = ""

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.public_name = name
        self.storage_name = f"_{name}_canonical"

    def __get__(
        self,
        instance: object | None,
        owner: type[object] | None = None,
    ) -> QuantityValue | Quantity:
        if instance is None:
            return self
        try:
            value = vars(instance)[self.storage_name]
        except KeyError as error:
            raise AttributeError(f"{self.public_name} is unset") from error
        return QuantityValue(
            canonical_value=float(value),
            canonical_unit=self.canonical_unit,
            conversion_factors=self.conversion_factors,
        )

    def __set__(
        self,
        instance: object,
        value: float | int | tuple[float | int, str],
    ) -> None:
        magnitude, unit = self._separate_input(value)
        canonical_value = magnitude * dict(self.conversion_factors)[unit]
        if not math.isfinite(canonical_value):
            raise ValueError(f"{self.public_name} must be finite")
        if self.minimum is not None and canonical_value < self.minimum:
            raise ValueError(
                f"{self.public_name} must be >= {self.minimum} {self.canonical_unit}"
            )
        if self.maximum is not None and canonical_value > self.maximum:
            raise ValueError(
                f"{self.public_name} must be <= {self.maximum} {self.canonical_unit}"
            )
        vars(instance)[self.storage_name] = canonical_value

    def _separate_input(
        self,
        value: float | int | tuple[float | int, str],
    ) -> tuple[float, str]:
        if isinstance(value, tuple):
            if len(value) != 2:
                raise TypeError(
                    f"{self.public_name} expects a number or (number, unit)"
                )
            raw_magnitude, unit = value
        else:
            raw_magnitude, unit = value, self.canonical_unit
        if isinstance(raw_magnitude, bool) or not isinstance(
            raw_magnitude,
            (int, float),
        ):
            raise TypeError(f"{self.public_name} magnitude must be numeric")
        if unit not in dict(self.conversion_factors):
            raise ValueError(f"{self.public_name} does not accept unit {unit!r}")
        return float(raw_magnitude), unit

    def spec(self) -> QuantitySpec:
        return QuantitySpec(
            name=self.public_name,
            storage_name=self.storage_name,
            canonical_unit=self.canonical_unit,
            accepted_units=tuple(unit for unit, _ in self.conversion_factors),
            minimum=self.minimum,
            maximum=self.maximum,
        )
