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
    'CmkKekIdentityArgs',
    'CmkKeyVaultPropertiesArgs',
    'IdentityDataArgs',
    'SkuArgs',
    'VaultPropertiesEncryptionArgs',
    'VaultPropertiesArgs',
]

@pulumi.input_type
class CmkKekIdentityArgs:
    def __init__(__self__, *,
                 use_system_assigned_identity: Optional[pulumi.Input[bool]] = None,
                 user_assigned_identity: Optional[pulumi.Input[str]] = None):
        """
        The details of the identity used for CMK
        :param pulumi.Input[bool] use_system_assigned_identity: Indicate that system assigned identity should be used. Mutually exclusive with 'userAssignedIdentity' field
        :param pulumi.Input[str] user_assigned_identity: The user assigned identity to be used to grant permissions in case the type of identity used is UserAssigned
        """
        if use_system_assigned_identity is not None:
            pulumi.set(__self__, "use_system_assigned_identity", use_system_assigned_identity)
        if user_assigned_identity is not None:
            pulumi.set(__self__, "user_assigned_identity", user_assigned_identity)

    @property
    @pulumi.getter(name="useSystemAssignedIdentity")
    def use_system_assigned_identity(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicate that system assigned identity should be used. Mutually exclusive with 'userAssignedIdentity' field
        """
        return pulumi.get(self, "use_system_assigned_identity")

    @use_system_assigned_identity.setter
    def use_system_assigned_identity(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "use_system_assigned_identity", value)

    @property
    @pulumi.getter(name="userAssignedIdentity")
    def user_assigned_identity(self) -> Optional[pulumi.Input[str]]:
        """
        The user assigned identity to be used to grant permissions in case the type of identity used is UserAssigned
        """
        return pulumi.get(self, "user_assigned_identity")

    @user_assigned_identity.setter
    def user_assigned_identity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_assigned_identity", value)


@pulumi.input_type
class CmkKeyVaultPropertiesArgs:
    def __init__(__self__, *,
                 key_uri: Optional[pulumi.Input[str]] = None):
        """
        The properties of the Key Vault which hosts CMK
        :param pulumi.Input[str] key_uri: The key uri of the Customer Managed Key
        """
        if key_uri is not None:
            pulumi.set(__self__, "key_uri", key_uri)

    @property
    @pulumi.getter(name="keyUri")
    def key_uri(self) -> Optional[pulumi.Input[str]]:
        """
        The key uri of the Customer Managed Key
        """
        return pulumi.get(self, "key_uri")

    @key_uri.setter
    def key_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_uri", value)


@pulumi.input_type
class IdentityDataArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[Union[str, 'ResourceIdentityType']],
                 user_assigned_identities: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        Identity for the resource.
        :param pulumi.Input[Union[str, 'ResourceIdentityType']] type: The type of managed identity used. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user-assigned identities. The type 'None' will remove any identities.
        :param pulumi.Input[Mapping[str, Any]] user_assigned_identities: The list of user-assigned identities associated with the resource. The user-assigned identity dictionary keys will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[Union[str, 'ResourceIdentityType']]:
        """
        The type of managed identity used. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user-assigned identities. The type 'None' will remove any identities.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[Union[str, 'ResourceIdentityType']]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        The list of user-assigned identities associated with the resource. The user-assigned identity dictionary keys will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        return pulumi.get(self, "user_assigned_identities")

    @user_assigned_identities.setter
    def user_assigned_identities(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "user_assigned_identities", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[Union[str, 'SkuName']],
                 capacity: Optional[pulumi.Input[str]] = None,
                 family: Optional[pulumi.Input[str]] = None,
                 size: Optional[pulumi.Input[str]] = None,
                 tier: Optional[pulumi.Input[str]] = None):
        """
        Identifies the unique system identifier for each Azure resource.
        :param pulumi.Input[Union[str, 'SkuName']] name: The Sku name.
        :param pulumi.Input[str] capacity: The sku capacity
        :param pulumi.Input[str] family: The sku family
        :param pulumi.Input[str] size: The sku size
        :param pulumi.Input[str] tier: The Sku tier.
        """
        pulumi.set(__self__, "name", name)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if family is not None:
            pulumi.set(__self__, "family", family)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[Union[str, 'SkuName']]:
        """
        The Sku name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[Union[str, 'SkuName']]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[str]]:
        """
        The sku capacity
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "capacity", value)

    @property
    @pulumi.getter
    def family(self) -> Optional[pulumi.Input[str]]:
        """
        The sku family
        """
        return pulumi.get(self, "family")

    @family.setter
    def family(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "family", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[str]]:
        """
        The sku size
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input[str]]:
        """
        The Sku tier.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tier", value)


@pulumi.input_type
class VaultPropertiesEncryptionArgs:
    def __init__(__self__, *,
                 infrastructure_encryption: Optional[pulumi.Input[Union[str, 'InfrastructureEncryptionState']]] = None,
                 kek_identity: Optional[pulumi.Input['CmkKekIdentityArgs']] = None,
                 key_vault_properties: Optional[pulumi.Input['CmkKeyVaultPropertiesArgs']] = None):
        """
        Customer Managed Key details of the resource.
        :param pulumi.Input[Union[str, 'InfrastructureEncryptionState']] infrastructure_encryption: Enabling/Disabling the Double Encryption state
        :param pulumi.Input['CmkKekIdentityArgs'] kek_identity: The details of the identity used for CMK
        :param pulumi.Input['CmkKeyVaultPropertiesArgs'] key_vault_properties: The properties of the Key Vault which hosts CMK
        """
        if infrastructure_encryption is not None:
            pulumi.set(__self__, "infrastructure_encryption", infrastructure_encryption)
        if kek_identity is not None:
            pulumi.set(__self__, "kek_identity", kek_identity)
        if key_vault_properties is not None:
            pulumi.set(__self__, "key_vault_properties", key_vault_properties)

    @property
    @pulumi.getter(name="infrastructureEncryption")
    def infrastructure_encryption(self) -> Optional[pulumi.Input[Union[str, 'InfrastructureEncryptionState']]]:
        """
        Enabling/Disabling the Double Encryption state
        """
        return pulumi.get(self, "infrastructure_encryption")

    @infrastructure_encryption.setter
    def infrastructure_encryption(self, value: Optional[pulumi.Input[Union[str, 'InfrastructureEncryptionState']]]):
        pulumi.set(self, "infrastructure_encryption", value)

    @property
    @pulumi.getter(name="kekIdentity")
    def kek_identity(self) -> Optional[pulumi.Input['CmkKekIdentityArgs']]:
        """
        The details of the identity used for CMK
        """
        return pulumi.get(self, "kek_identity")

    @kek_identity.setter
    def kek_identity(self, value: Optional[pulumi.Input['CmkKekIdentityArgs']]):
        pulumi.set(self, "kek_identity", value)

    @property
    @pulumi.getter(name="keyVaultProperties")
    def key_vault_properties(self) -> Optional[pulumi.Input['CmkKeyVaultPropertiesArgs']]:
        """
        The properties of the Key Vault which hosts CMK
        """
        return pulumi.get(self, "key_vault_properties")

    @key_vault_properties.setter
    def key_vault_properties(self, value: Optional[pulumi.Input['CmkKeyVaultPropertiesArgs']]):
        pulumi.set(self, "key_vault_properties", value)


@pulumi.input_type
class VaultPropertiesArgs:
    def __init__(__self__, *,
                 encryption: Optional[pulumi.Input['VaultPropertiesEncryptionArgs']] = None):
        """
        Properties of the vault.
        :param pulumi.Input['VaultPropertiesEncryptionArgs'] encryption: Customer Managed Key details of the resource.
        """
        if encryption is not None:
            pulumi.set(__self__, "encryption", encryption)

    @property
    @pulumi.getter
    def encryption(self) -> Optional[pulumi.Input['VaultPropertiesEncryptionArgs']]:
        """
        Customer Managed Key details of the resource.
        """
        return pulumi.get(self, "encryption")

    @encryption.setter
    def encryption(self, value: Optional[pulumi.Input['VaultPropertiesEncryptionArgs']]):
        pulumi.set(self, "encryption", value)


