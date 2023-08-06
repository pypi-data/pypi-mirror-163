from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from typing import TYPE_CHECKING, Any, Iterable, Optional, Union

from atoti_core import BitwiseOperatorsOnly, keyword_only_dataclass
from typeguard import check_argument_types, typechecked, typeguard_ignore

from ._java_api import JavaApi
from ._py4j_utils import as_java_object

if TYPE_CHECKING:
    from ._measures.boolean_measure import BooleanMeasure
    from ._measures.calculated_measure import CalculatedMeasure


@keyword_only_dataclass
@typeguard_ignore
# See https://github.com/python/mypy/issues/5374.
@dataclass(eq=False)  # type: ignore[misc]
class MeasureDescription(BitwiseOperatorsOnly):
    """The description of a :class:`~atoti.Measure` that has not been added to the cube yet."""

    def _distil(
        self, *, java_api: JavaApi, cube_name: str, measure_name: Optional[str] = None
    ) -> str:
        """Return the name of the measure, creating it in the cube if it does not exist yet."""
        if not hasattr(self, "_name"):
            self._name: str = (  # pylint: disable=attribute-defined-outside-init
                self._do_distil(
                    java_api=java_api, cube_name=cube_name, measure_name=measure_name
                )
            )
        elif measure_name is not None:
            # This measure has already been distilled, this is a copy.
            java_api.copy_measure(
                self._name,
                measure_name,
                cube_name=cube_name,
            )
        return self._name

    @abstractmethod
    def _do_distil(
        self, *, java_api: JavaApi, cube_name: str, measure_name: Optional[str] = None
    ) -> str:
        """Create the measure in the cube and return its name."""

    def __mul__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to self * other."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure_description(other)
        return CalculatedMeasure(Operator.mul([self, other_measure]))

    def __rmul__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to other * self."""
        other_measure = _convert_to_measure_description(other)
        return self.__mul__(other_measure)

    def __truediv__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to self / other."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure_description(other)
        return CalculatedMeasure(Operator.truediv([self, other_measure]))

    def __rtruediv__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to other / self."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other = _convert_to_measure_description(other)
        return CalculatedMeasure(Operator.truediv([other, self]))

    def __floordiv__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to self // other."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other = _convert_to_measure_description(other)
        return CalculatedMeasure(Operator.floordiv([self, other]))

    def __rfloordiv__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to other // self."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other = _convert_to_measure_description(other)
        return CalculatedMeasure(Operator.floordiv([other, self]))

    def __add__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to self + other."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure_description(other)
        return CalculatedMeasure(Operator.add([self, other_measure]))

    def __radd__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to other + self."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure_description(other)
        return CalculatedMeasure(Operator.add([other_measure, self]))

    def __sub__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to self - other."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure_description(other)
        return CalculatedMeasure(Operator.sub([self, other_measure]))

    def __rsub__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to other - self."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure_description(other)
        return CalculatedMeasure(Operator.sub([other_measure, self]))

    def __pow__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to self ** other."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure_description(other)
        return CalculatedMeasure(Operator("pow", [self, other_measure]))

    def __neg__(self) -> CalculatedMeasure:
        """Return a measure equal to -self."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        return CalculatedMeasure(Operator.neg(self))

    def __mod__(self, other: Any) -> CalculatedMeasure:
        """Return a measure equal to self % other."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        other_measure = _convert_to_measure_description(other)
        return CalculatedMeasure(Operator("mod", [self, other_measure]))

    ########################
    # Boolean calculations #
    ########################

    def _boolean_calculation(self, other: Any, operation: str) -> BooleanMeasure:
        from ._measures.boolean_measure import BooleanMeasure

        other_measure = _convert_to_measure_description(other)
        return BooleanMeasure(operation, (self, other_measure))

    def __lt__(self, other: Any) -> BooleanMeasure:
        """Lower than operator."""
        return self._boolean_calculation(other, "lt")

    def __le__(self, other: Any) -> BooleanMeasure:
        """Lower or equal operator."""
        return self._boolean_calculation(other, "le")

    def __gt__(self, other: Any) -> BooleanMeasure:
        """Greater than operator."""
        return self._boolean_calculation(other, "gt")

    def __ge__(self, other: Any) -> BooleanMeasure:
        """Greater or equal operator."""
        return self._boolean_calculation(other, "ge")

    def __eq__(  # type: ignore[override]
        self,
        other: Any,
    ) -> BooleanMeasure:
        """Equals operator."""
        from ._measures.boolean_measure import BooleanMeasure

        if other is None:
            return BooleanMeasure("isNull", (self,))
        return self._boolean_calculation(other, "eq")

    def __ne__(  # type: ignore[override]
        self,
        other: Any,
    ) -> BooleanMeasure:
        """Not equals operator."""
        from ._measures.boolean_measure import BooleanMeasure

        if other is None:
            return BooleanMeasure("notNull", (self,))
        return self._boolean_calculation(other, "ne")

    ####################
    # Array operations #
    ####################

    @typechecked
    def __getitem__(self, key: Union[slice, int, MeasureLike]) -> MeasureDescription:
        """Return a measure equal to the element or slice of this array measure at the passed index(es)."""
        from ._measures.calculated_measure import CalculatedMeasure, Operator

        # Return a sub-vector if the key is a slice.
        # Because MeasureLike is unbound, pyright throws an error here
        if isinstance(key, slice):
            if key.step:
                raise ValueError("step cannot be used to slice an array measure.")
            start = key.start if key.start is not None else float("nan")
            stop = key.stop if key.stop is not None else float("nan")
            return CalculatedMeasure(
                Operator(
                    "vector_sub",
                    [
                        self,
                        _convert_to_measure_description(start),
                        _convert_to_measure_description(stop),
                    ],
                )
            )

        # Return a single element.
        if isinstance(key, (int, MeasureDescription, MeasureConvertible)):
            return CalculatedMeasure(
                Operator("vector_element", [self, _convert_to_measure_description(key)])
            )

        # Crappy input
        raise TypeError("The index must be a slice, a measure or an integer")

    @property
    def _bool_alternative_message(self) -> Optional[str]:  # pylint: disable=no-self-use
        return "For conditions on measure values use `where` or `filter` method."

    # This is needed otherwise errors like "TypeError: unhashable type: 'BooleanMeasure'" are thrown.
    # This is a "eq=False" dataclass so hash method is generated "according to how eq" is set but
    # the desired behavior is to use BitwiseOperatorsOnly.__hash__().
    def __hash__(self) -> int:  # pylint: disable=useless-super-delegation, no-self-use
        return super().__hash__()


class MeasureConvertible(BitwiseOperatorsOnly):
    """Instances of this class can be converted to measures."""

    @property
    @abstractmethod
    def _measure_description(self) -> MeasureDescription:
        ...


LiteralMeasureValue = Union[
    date, datetime, int, float, str, Iterable[int], Iterable[float]
]
MeasureLike = Union[LiteralMeasureValue, MeasureDescription, MeasureConvertible]


@keyword_only_dataclass
@dataclass(eq=False)
class _LiteralMeasure(MeasureDescription):
    """A measure equal to a literal value."""

    _value: LiteralMeasureValue

    def _do_distil(
        self, *, java_api: JavaApi, cube_name: str, measure_name: Optional[str] = None
    ) -> str:
        val = as_java_object(self._value, gateway=java_api.gateway)
        distilled_name = java_api.create_measure(
            cube_name, measure_name, "LITERAL", val
        )
        return distilled_name


def _convert_to_measure_description(arg: MeasureLike) -> MeasureDescription:
    check_argument_types()

    if isinstance(arg, MeasureDescription):
        return arg
    if isinstance(arg, MeasureConvertible):
        return arg._measure_description
    return _LiteralMeasure(_value=arg)
