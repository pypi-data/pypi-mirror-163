# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['StorageAccountManagementPoliciesArgs', 'StorageAccountManagementPolicies']

@pulumi.input_type
class StorageAccountManagementPoliciesArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 management_policy_name: Optional[pulumi.Input[str]] = None,
                 policy: Optional[Any] = None):
        """
        The set of arguments for constructing a StorageAccountManagementPolicies resource.
        :param pulumi.Input[str] account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input[str] management_policy_name: The name of the Storage Account Management Policy. It should always be 'default'
        :param Any policy: The Storage Account ManagementPolicies Rules, in JSON format. See more details in: https://docs.microsoft.com/en-us/azure/storage/common/storage-lifecycle-managment-concepts.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if management_policy_name is not None:
            pulumi.set(__self__, "management_policy_name", management_policy_name)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group within the user's subscription. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="managementPolicyName")
    def management_policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Storage Account Management Policy. It should always be 'default'
        """
        return pulumi.get(self, "management_policy_name")

    @management_policy_name.setter
    def management_policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "management_policy_name", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[Any]:
        """
        The Storage Account ManagementPolicies Rules, in JSON format. See more details in: https://docs.microsoft.com/en-us/azure/storage/common/storage-lifecycle-managment-concepts.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[Any]):
        pulumi.set(self, "policy", value)


warnings.warn("""Version 2018-03-01-preview will be removed in v2 of the provider.""", DeprecationWarning)


class StorageAccountManagementPolicies(pulumi.CustomResource):
    warnings.warn("""Version 2018-03-01-preview will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 management_policy_name: Optional[pulumi.Input[str]] = None,
                 policy: Optional[Any] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The Get Storage Account ManagementPolicies operation response.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
        :param pulumi.Input[str] management_policy_name: The name of the Storage Account Management Policy. It should always be 'default'
        :param Any policy: The Storage Account ManagementPolicies Rules, in JSON format. See more details in: https://docs.microsoft.com/en-us/azure/storage/common/storage-lifecycle-managment-concepts.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StorageAccountManagementPoliciesArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The Get Storage Account ManagementPolicies operation response.

        :param str resource_name: The name of the resource.
        :param StorageAccountManagementPoliciesArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StorageAccountManagementPoliciesArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 management_policy_name: Optional[pulumi.Input[str]] = None,
                 policy: Optional[Any] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""StorageAccountManagementPolicies is deprecated: Version 2018-03-01-preview will be removed in v2 of the provider.""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = StorageAccountManagementPoliciesArgs.__new__(StorageAccountManagementPoliciesArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["management_policy_name"] = management_policy_name
            __props__.__dict__["policy"] = policy
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["last_modified_time"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:storage:StorageAccountManagementPolicies"), pulumi.Alias(type_="azure-native:storage/v20181101:StorageAccountManagementPolicies"), pulumi.Alias(type_="azure-native:storage/v20190401:StorageAccountManagementPolicies"), pulumi.Alias(type_="azure-native:storage/v20190601:StorageAccountManagementPolicies"), pulumi.Alias(type_="azure-native:storage/v20200801preview:StorageAccountManagementPolicies"), pulumi.Alias(type_="azure-native:storage/v20210101:StorageAccountManagementPolicies"), pulumi.Alias(type_="azure-native:storage/v20210201:StorageAccountManagementPolicies"), pulumi.Alias(type_="azure-native:storage/v20210401:StorageAccountManagementPolicies"), pulumi.Alias(type_="azure-native:storage/v20210601:StorageAccountManagementPolicies"), pulumi.Alias(type_="azure-native:storage/v20210801:StorageAccountManagementPolicies"), pulumi.Alias(type_="azure-native:storage/v20210901:StorageAccountManagementPolicies")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StorageAccountManagementPolicies, __self__).__init__(
            'azure-native:storage/v20180301preview:StorageAccountManagementPolicies',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StorageAccountManagementPolicies':
        """
        Get an existing StorageAccountManagementPolicies resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = StorageAccountManagementPoliciesArgs.__new__(StorageAccountManagementPoliciesArgs)

        __props__.__dict__["last_modified_time"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["policy"] = None
        __props__.__dict__["type"] = None
        return StorageAccountManagementPolicies(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[str]:
        """
        Returns the date and time the ManagementPolicies was last modified.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[Optional[Any]]:
        """
        The Storage Account ManagementPolicies Rules, in JSON format. See more details in: https://docs.microsoft.com/en-us/azure/storage/common/storage-lifecycle-managment-concepts.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

