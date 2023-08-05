# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'AppServiceCertificateArgs',
]

@pulumi.input_type
class AppServiceCertificateArgs:
    def __init__(__self__, *,
                 key_vault_id: Optional[pulumi.Input[str]] = None,
                 key_vault_secret_name: Optional[pulumi.Input[str]] = None):
        """
        Key Vault container for a certificate that is purchased through Azure.
        :param pulumi.Input[str] key_vault_id: Key Vault resource Id.
        :param pulumi.Input[str] key_vault_secret_name: Key Vault secret name.
        """
        if key_vault_id is not None:
            pulumi.set(__self__, "key_vault_id", key_vault_id)
        if key_vault_secret_name is not None:
            pulumi.set(__self__, "key_vault_secret_name", key_vault_secret_name)

    @property
    @pulumi.getter(name="keyVaultId")
    def key_vault_id(self) -> Optional[pulumi.Input[str]]:
        """
        Key Vault resource Id.
        """
        return pulumi.get(self, "key_vault_id")

    @key_vault_id.setter
    def key_vault_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_id", value)

    @property
    @pulumi.getter(name="keyVaultSecretName")
    def key_vault_secret_name(self) -> Optional[pulumi.Input[str]]:
        """
        Key Vault secret name.
        """
        return pulumi.get(self, "key_vault_secret_name")

    @key_vault_secret_name.setter
    def key_vault_secret_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_secret_name", value)


