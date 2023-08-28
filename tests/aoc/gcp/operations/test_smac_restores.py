"""Tests validating AoC on GCP restores."""
import pytest

from lib.aoc.gcp.operations.restore import *
from tests.aoc.conftest import AocDefaultOptions


@pytest.fixture
def aoc_gcp_restore(
    ansible_module: pytest.fixture, aoc_default_options: AocDefaultOptions
) -> AocGcpRestore:
    """Fixture returning aoc gcp restore operations."""
    command_generator_vars: AocGcpRestoreAvailableVars = AocGcpRestoreDataVars(
        todo="todo"
    )

    if aoc_default_options["stack_version"] == "2.3":
        command_generator_vars = Aoc23GcpRestoreDataVars(todo="todo")

    return AocGcpRestore(
        aoc_version=aoc_default_options["stack_version"],
        aoc_ops_image=aoc_default_options["ops_container_image"],
        aoc_ops_image_tag=aoc_default_options["ops_container_image_tag"],
        aoc_image_registry_username=aoc_default_options[
            "ops_container_image_registry_username"
        ],
        aoc_image_registry_password=aoc_default_options[
            "ops_container_image_registry_password"
        ],
        ansible_module=ansible_module,
        command_generator_vars=command_generator_vars,
    )


class TestAoCGcpRestore:
    @pytest.mark.gcp
    @pytest.mark.aoc_gcp_restore
    @pytest.mark.operations
    def test_restore(self, aoc_gcp_restore: AocGcpRestore) -> None:
        assert aoc_gcp_restore.run()
