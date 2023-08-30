"""Tests validating AoC on AWS backup/restore."""
import pytest

from lib.aoc.aws.operations.backup import AocAwsBackup
from lib.aoc.aws.operations.backup import AocAwsBackupDataExtraVars
from lib.aoc.aws.operations.backup import AocAwsBackupDataVars
from lib.aoc.aws.operations.restore import AocAwsRestore
from lib.aoc.aws.operations.restore import AocAwsRestoreDataExtraVars
from lib.aoc.aws.operations.restore import AocAwsRestoreDataVars
from tests.aoc.aws.conftest import AocAwsDefaultOptions
from tests.aoc.aws.operations.conftest import AocAwsBackupDefaultOptions
from tests.aoc.aws.operations.conftest import AocAwsRestoreDefaultOptions
from tests.aoc.conftest import AocDefaultOptions


@pytest.fixture
def aoc_aws_backup(
    ansible_module: pytest.fixture,
    aoc_default_options: AocDefaultOptions,
    aoc_aws_default_options: AocAwsDefaultOptions,
    aoc_aws_backup_default_options: AocAwsBackupDefaultOptions,
) -> AocAwsBackup:
    """Fixture returning aoc aws backup operations."""

    command_generator_vars: AocAwsBackupDataVars = AocAwsBackupDataVars(
        cloud_credentials_path=aoc_aws_default_options["credentials_path"],
        deployment_name=aoc_default_options["stack_deployment_name"],
        extra_vars=AocAwsBackupDataExtraVars(
            aws_backup_iam_role_arn=aoc_aws_backup_default_options[
                "backup_iam_role_arn"
            ],
            aws_backup_vault_name=aoc_aws_backup_default_options["backup_vault_name"],
            aws_region=aoc_aws_default_options["region"],
            aws_s3_bucket=aoc_aws_backup_default_options["backup_s3_bucket"],
            aws_ssm_bucket_name=aoc_aws_backup_default_options[
                "backup_ssm_bucket_name"
            ],
            backup_prefix=aoc_aws_backup_default_options["backup_prefix"],
        ),
    )

    return AocAwsBackup(
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


@pytest.fixture
def aoc_aws_restore(
    ansible_module: pytest.fixture,
    aoc_default_options: AocDefaultOptions,
    aoc_aws_default_options: AocAwsDefaultOptions,
    aoc_aws_restore_default_options: AocAwsRestoreDefaultOptions,
) -> AocAwsRestore:
    """Fixture returning aoc aws restore operations."""
    command_generator_vars: AocAwsRestoreDataVars = AocAwsRestoreDataVars(
        cloud_credentials_path=aoc_aws_default_options["credentials_path"],
        deployment_name=aoc_default_options["stack_deployment_name"],
        extra_vars=AocAwsRestoreDataExtraVars(
            aws_backup_name=aoc_aws_restore_default_options["backup_name"],
            aws_region=aoc_aws_default_options["region"],
            aws_s3_bucket=aoc_aws_restore_default_options["backup_s3_bucket"],
            aws_ssm_bucket_name=aoc_aws_restore_default_options[
                "backup_ssm_bucket_name"
            ],
        ),
    )

    return AocAwsRestore(
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


@pytest.mark.aws
@pytest.mark.operations
@pytest.mark.aoc_aws_backup_restore
class TestAoCAwsBackupRestore:
    @pytest.mark.aoc_aws_backup
    def test_backup(self, aoc_aws_backup: AocAwsBackup) -> None:
        assert aoc_aws_backup.validate()
        assert aoc_aws_backup.run()

    @pytest.mark.aoc_aws_restore
    def test_restore(self, aoc_aws_restore: AocAwsRestore) -> None:
        assert aoc_aws_restore.validate()
        assert aoc_aws_restore.run()
