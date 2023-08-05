from functools import wraps
from typing import Callable, Dict, TypeVar

from servicefoundry.builder.builders import dockerfile, tfy_python_buildpack

BUILD_REGISTRY: Dict[str, Callable] = {
    "dockerfile": dockerfile.build,
    "tfy-python-buildpack": tfy_python_buildpack.build,
}

__all__ = ["get_builder"]


def get_builder(build_configuration_type: str) -> Callable:
    if build_configuration_type not in BUILD_REGISTRY:
        raise NotImplementedError(f"Builder for {build_configuration_type} not found")

    return BUILD_REGISTRY[build_configuration_type]
