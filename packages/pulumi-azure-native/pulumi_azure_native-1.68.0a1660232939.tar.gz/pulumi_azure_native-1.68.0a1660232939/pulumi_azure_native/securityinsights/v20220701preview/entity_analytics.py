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

__all__ = ['EntityAnalyticsArgs', 'EntityAnalytics']

@pulumi.input_type
class EntityAnalyticsArgs:
    def __init__(__self__, *,
                 kind: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 workspace_name: pulumi.Input[str],
                 entity_providers: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'EntityProviders']]]]] = None,
                 settings_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a EntityAnalytics resource.
        :param pulumi.Input[str] kind: The kind of the setting
               Expected value is 'EntityAnalytics'.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'EntityProviders']]]] entity_providers: The relevant entity providers that are synced
        :param pulumi.Input[str] settings_name: The setting name. Supports - Anomalies, EyesOn, EntityAnalytics, Ueba
        """
        pulumi.set(__self__, "kind", 'EntityAnalytics')
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "workspace_name", workspace_name)
        if entity_providers is not None:
            pulumi.set(__self__, "entity_providers", entity_providers)
        if settings_name is not None:
            pulumi.set(__self__, "settings_name", settings_name)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[str]:
        """
        The kind of the setting
        Expected value is 'EntityAnalytics'.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: pulumi.Input[str]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> pulumi.Input[str]:
        """
        The name of the workspace.
        """
        return pulumi.get(self, "workspace_name")

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_name", value)

    @property
    @pulumi.getter(name="entityProviders")
    def entity_providers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'EntityProviders']]]]]:
        """
        The relevant entity providers that are synced
        """
        return pulumi.get(self, "entity_providers")

    @entity_providers.setter
    def entity_providers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'EntityProviders']]]]]):
        pulumi.set(self, "entity_providers", value)

    @property
    @pulumi.getter(name="settingsName")
    def settings_name(self) -> Optional[pulumi.Input[str]]:
        """
        The setting name. Supports - Anomalies, EyesOn, EntityAnalytics, Ueba
        """
        return pulumi.get(self, "settings_name")

    @settings_name.setter
    def settings_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "settings_name", value)


class EntityAnalytics(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 entity_providers: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'EntityProviders']]]]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 settings_name: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Settings with single toggle.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'EntityProviders']]]] entity_providers: The relevant entity providers that are synced
        :param pulumi.Input[str] kind: The kind of the setting
               Expected value is 'EntityAnalytics'.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] settings_name: The setting name. Supports - Anomalies, EyesOn, EntityAnalytics, Ueba
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EntityAnalyticsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Settings with single toggle.

        :param str resource_name: The name of the resource.
        :param EntityAnalyticsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EntityAnalyticsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 entity_providers: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'EntityProviders']]]]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 settings_name: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EntityAnalyticsArgs.__new__(EntityAnalyticsArgs)

            __props__.__dict__["entity_providers"] = entity_providers
            if kind is None and not opts.urn:
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__["kind"] = 'EntityAnalytics'
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["settings_name"] = settings_name
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__["workspace_name"] = workspace_name
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:securityinsights:EntityAnalytics"), pulumi.Alias(type_="azure-native:securityinsights/v20190101preview:EntityAnalytics"), pulumi.Alias(type_="azure-native:securityinsights/v20210301preview:EntityAnalytics"), pulumi.Alias(type_="azure-native:securityinsights/v20210901preview:EntityAnalytics"), pulumi.Alias(type_="azure-native:securityinsights/v20211001preview:EntityAnalytics"), pulumi.Alias(type_="azure-native:securityinsights/v20220101preview:EntityAnalytics"), pulumi.Alias(type_="azure-native:securityinsights/v20220401preview:EntityAnalytics"), pulumi.Alias(type_="azure-native:securityinsights/v20220501preview:EntityAnalytics"), pulumi.Alias(type_="azure-native:securityinsights/v20220601preview:EntityAnalytics")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(EntityAnalytics, __self__).__init__(
            'azure-native:securityinsights/v20220701preview:EntityAnalytics',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'EntityAnalytics':
        """
        Get an existing EntityAnalytics resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = EntityAnalyticsArgs.__new__(EntityAnalyticsArgs)

        __props__.__dict__["entity_providers"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return EntityAnalytics(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="entityProviders")
    def entity_providers(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The relevant entity providers that are synced
        """
        return pulumi.get(self, "entity_providers")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        The kind of the setting
        Expected value is 'EntityAnalytics'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

