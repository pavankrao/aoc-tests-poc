"""AoC on GCP backup module.

This module performs the standard operations for backing up an
AoC deployment on GCP cloud.
"""
import typing
from typing import Dict
from typing import TypedDict

from pytest_ansible.host_manager import BaseHostManager

from lib.aoc.ops_container import OpsContainer

__all__ = [
    "AocGcpBackup",
    "AocGcpBackupDataVars",
    "AocGcpBackupDataExtraVars",
    "AocGcpBackupStackResult",
]


class AocGcpBackupDataExtraVars(TypedDict, total=False):
    """AoC default backup operations playbook data extra vars."""

    gcp_compute_region: str
    gcp_compute_zone: str
    gcp_storage_bucket: str
    gcp_backup_prefix: str


class AocGcpBackupDataVars(TypedDict, total=False):
    """AoC default backup operations playbook data vars."""

    cloud_credentials_path: str
    deployment_name: str
    extra_vars: AocGcpBackupDataExtraVars


class AocGcpBackupStackResult(TypedDict):
    """Aoc Gcp stack backup results."""

    playbook_output: str
    playbook_result: bool
    backup_object_name: str


class AocGcpBackup(OpsContainer):
    """AocGcpBackup class.

    This class handles all operations to perform an aoc on gcp stack backup.
    Perform the following to initiate a backup:
        1. Instantiate the class constructing an object
            > aoc_gcp_backup = AocGcpBackup(...)
        2. Call the `setup` method to perform pre backup operations
            > aoc_gcp_backup.setup()
        3. Call the `backup_stack` method to perform backup
            > aoc_gcp_backup.backup_stack()
    """

    def __init__(
        self,
        aoc_version: str,
        aoc_ops_image: str,
        aoc_ops_image_tag: str,
        aoc_image_registry_username: str,
        aoc_image_registry_password: str,
        ansible_module: BaseHostManager,
        command_generator_vars: AocGcpBackupDataVars,
    ) -> None:
        """Constructor.

        :param aoc_version: the aoc version deployed
        :param aoc_ops_image: the aoc operations container image
        :param aoc_ops_image_tag: the aoc operations container image tag
        :param aoc_image_registry_username: the username to authenticate with
            the image registry holding aoc operations image
        :param aoc_image_registry_password: the password to authenticate with
            the image registry holding aoc operations image
        :param ansible_module: the pytest ansible module fixture
        :param command_generator_vars: the data to provide to aoc operations command generator playbooks
        """
        super().__init__(
            "gcp",
            aoc_version,
            aoc_ops_image,
            aoc_ops_image_tag,
            aoc_image_registry_username,
            aoc_image_registry_password,
            ansible_module,
        )

        self.ansible_module: BaseHostManager = ansible_module

        self.command_generator_vars: AocGcpBackupDataVars = command_generator_vars

    def command_generator_setup(self) -> None:
        """Performs any setup required to run command generator playbooks."""
        self.command_args: List[str] = [
            f'gcp_foundation_stack_name={self.command_generator_vars["deployment_name"]}',
            f'gcp_region={self.command_generator_vars["extra_vars"]["gcp_compute_region"]}',
            f'gcp_zone={self.command_generator_vars["extra_vars"]["gcp_compute_zone"]}',
            f'gcp_storage_bucket={self.command_generator_vars["extra_vars"]["gcp_storage_bucket"]}',
        ]
        cloud_credentials_path: str

        if self.aoc_version != "2.3":
            self.env_vars = {
                "DEPLOYMENT_NAME": f'{self.command_generator_vars["deployment_name"]}',
                "GENERATE_INVENTORY": "true",
            }
            self.command_args.extend(
                [
                    f'gcp_backup_prefix={self.command_generator_vars["extra_vars"]["gcp_backup_prefix"]}',
                ]
            )

        self.command = "redhat.ansible_on_clouds.gcp_backup_deployment"
        self.env_vars.update({
            "ANSIBLE_CONFIG": "../gcp-ansible.cfg",
            "PLATFORM": f"{self.cloud.upper()}",
        })
        self.volume_mounts = [
            f'{self.command_generator_vars["cloud_credentials_path"]}:/home/runner/.gcp/credentials:ro',
        ]

    def create_storage_bucket(self) -> bool:
        """Create gcp storage bucket to store backup files."""
        # TODO: Implement gcp_storage_bucket module to create bucket
        pass

    def delete_storage_bucket(self) -> bool:
        """Delete gcp storage bucket holding backup files."""
        # TODO: Implement gcp_storage_bucket module to delete bucket
        pass

    def get_storage_backup_object(self) -> str:
        """Gets the stack backup object stored in the gcp bucket."""
        # TODO: Implement gcp_storage_bucket module to fetch backup objects
        pass
