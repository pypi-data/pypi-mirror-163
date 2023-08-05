# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['ProtectionPolicyArgs', 'ProtectionPolicy']

@pulumi.input_type
class ProtectionPolicyArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 vault_name: pulumi.Input[str],
                 e_tag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Union['AzureIaaSVMProtectionPolicyArgs', 'AzureSqlProtectionPolicyArgs', 'MabProtectionPolicyArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ProtectionPolicy resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group associated with the Recovery Services vault.
        :param pulumi.Input[str] vault_name: The name of the Recovery Services vault.
        :param pulumi.Input[str] e_tag: Optional ETag.
        :param pulumi.Input[str] id: Resource ID represents the complete path to the resource.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] name: Resource name associated with the resource.
        :param pulumi.Input[str] policy_name: The backup policy to be created.
        :param pulumi.Input[Union['AzureIaaSVMProtectionPolicyArgs', 'AzureSqlProtectionPolicyArgs', 'MabProtectionPolicyArgs']] properties: The base class for a backup policy. Workload-specific backup policies are derived from this class.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] type: Resource type represents the complete path of the form Namespace/ResourceType/ResourceType/...
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "vault_name", vault_name)
        if e_tag is not None:
            pulumi.set(__self__, "e_tag", e_tag)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if policy_name is not None:
            pulumi.set(__self__, "policy_name", policy_name)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group associated with the Recovery Services vault.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="vaultName")
    def vault_name(self) -> pulumi.Input[str]:
        """
        The name of the Recovery Services vault.
        """
        return pulumi.get(self, "vault_name")

    @vault_name.setter
    def vault_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "vault_name", value)

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> Optional[pulumi.Input[str]]:
        """
        Optional ETag.
        """
        return pulumi.get(self, "e_tag")

    @e_tag.setter
    def e_tag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "e_tag", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID represents the complete path to the resource.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Resource name associated with the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        The backup policy to be created.
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_name", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input[Union['AzureIaaSVMProtectionPolicyArgs', 'AzureSqlProtectionPolicyArgs', 'MabProtectionPolicyArgs']]]:
        """
        The base class for a backup policy. Workload-specific backup policies are derived from this class.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input[Union['AzureIaaSVMProtectionPolicyArgs', 'AzureSqlProtectionPolicyArgs', 'MabProtectionPolicyArgs']]]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Resource type represents the complete path of the form Namespace/ResourceType/ResourceType/...
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


warnings.warn("""Version 2016-06-01 will be removed in v2 of the provider.""", DeprecationWarning)


class ProtectionPolicy(pulumi.CustomResource):
    warnings.warn("""Version 2016-06-01 will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 e_tag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Union[pulumi.InputType['AzureIaaSVMProtectionPolicyArgs'], pulumi.InputType['AzureSqlProtectionPolicyArgs'], pulumi.InputType['MabProtectionPolicyArgs']]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 vault_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The base class for backup policy. Workload-specific backup policies are derived from this class.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] e_tag: Optional ETag.
        :param pulumi.Input[str] id: Resource ID represents the complete path to the resource.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] name: Resource name associated with the resource.
        :param pulumi.Input[str] policy_name: The backup policy to be created.
        :param pulumi.Input[Union[pulumi.InputType['AzureIaaSVMProtectionPolicyArgs'], pulumi.InputType['AzureSqlProtectionPolicyArgs'], pulumi.InputType['MabProtectionPolicyArgs']]] properties: The base class for a backup policy. Workload-specific backup policies are derived from this class.
        :param pulumi.Input[str] resource_group_name: The name of the resource group associated with the Recovery Services vault.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] type: Resource type represents the complete path of the form Namespace/ResourceType/ResourceType/...
        :param pulumi.Input[str] vault_name: The name of the Recovery Services vault.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ProtectionPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The base class for backup policy. Workload-specific backup policies are derived from this class.

        :param str resource_name: The name of the resource.
        :param ProtectionPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProtectionPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 e_tag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Union[pulumi.InputType['AzureIaaSVMProtectionPolicyArgs'], pulumi.InputType['AzureSqlProtectionPolicyArgs'], pulumi.InputType['MabProtectionPolicyArgs']]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 vault_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""ProtectionPolicy is deprecated: Version 2016-06-01 will be removed in v2 of the provider.""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProtectionPolicyArgs.__new__(ProtectionPolicyArgs)

            __props__.__dict__["e_tag"] = e_tag
            __props__.__dict__["id"] = id
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["policy_name"] = policy_name
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["type"] = type
            if vault_name is None and not opts.urn:
                raise TypeError("Missing required property 'vault_name'")
            __props__.__dict__["vault_name"] = vault_name
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:recoveryservices:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20201001:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20201201:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210101:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210201:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210201preview:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210210:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210301:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210401:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210601:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210701:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210801:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20211001:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20211201:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20220101:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20220201:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20220301:ProtectionPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20220601preview:ProtectionPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ProtectionPolicy, __self__).__init__(
            'azure-native:recoveryservices/v20160601:ProtectionPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ProtectionPolicy':
        """
        Get an existing ProtectionPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ProtectionPolicyArgs.__new__(ProtectionPolicyArgs)

        __props__.__dict__["e_tag"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return ProtectionPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> pulumi.Output[Optional[str]]:
        """
        Optional ETag.
        """
        return pulumi.get(self, "e_tag")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        Resource name associated with the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output[Any]:
        """
        The base class for a backup policy. Workload-specific backup policies are derived from this class.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[Optional[str]]:
        """
        Resource type represents the complete path of the form Namespace/ResourceType/ResourceType/...
        """
        return pulumi.get(self, "type")

