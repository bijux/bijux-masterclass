from __future__ import annotations

from dataclasses import asdict, dataclass
import inspect

from .protocol import inspect_descriptor_protocol


@dataclass(frozen=True, slots=True)
class MethodBinding:
    """Identity evidence for one function-to-bound-method transition."""

    public_name: str
    static_type: str
    descriptor_kind: str
    class_access_type: str
    instance_access_type: str
    class_access_is_function: bool
    bound_function_is_static_function: bool
    bound_self_is_instance: bool

    def manifest(self) -> dict[str, object]:
        return asdict(self)


def inspect_method_binding(
    owner: type[object],
    instance: object,
    name: str,
) -> MethodBinding:
    """Compare static, class, and instance access for one method name."""

    static_value = inspect.getattr_static(owner, name)
    class_value = getattr(owner, name)
    instance_value = getattr(instance, name)
    protocol = inspect_descriptor_protocol(static_value)
    return MethodBinding(
        public_name=name,
        static_type=type(static_value).__name__,
        descriptor_kind=protocol.kind,
        class_access_type=type(class_value).__name__,
        instance_access_type=type(instance_value).__name__,
        class_access_is_function=class_value is static_value,
        bound_function_is_static_function=(
            getattr(instance_value, "__func__", None) is static_value
        ),
        bound_self_is_instance=getattr(instance_value, "__self__", None) is instance,
    )


def method_binding_evidence() -> dict[str, object]:
    """Expose method binding and the shadowing allowed by non-data precedence."""

    class Delivery:
        def __init__(self, prefix: str) -> None:
            self.prefix = prefix

        def render(self, title: str) -> str:
            return f"{self.prefix}: {title}"

    delivery = Delivery("[incident]")
    binding = inspect_method_binding(Delivery, delivery, "render")
    rendered = delivery.render("CPU high")

    shadowed = Delivery("[shadowed]")
    vars(shadowed)["render"] = "instance replacement"
    return {
        "binding": binding.manifest(),
        "bound_call_result": rendered,
        "shadowed_instance_value": shadowed.render,
        "shadowing_is_possible": shadowed.render == "instance replacement",
    }
