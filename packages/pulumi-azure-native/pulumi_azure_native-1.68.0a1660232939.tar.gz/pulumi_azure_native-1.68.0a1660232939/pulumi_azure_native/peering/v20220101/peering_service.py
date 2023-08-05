# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *

__all__ = ['PeeringServiceArgs', 'PeeringService']

@pulumi.input_type
class PeeringServiceArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 peering_service_location: Optional[pulumi.Input[str]] = None,
                 peering_service_name: Optional[pulumi.Input[str]] = None,
                 peering_service_provider: Optional[pulumi.Input[str]] = None,
                 provider_backup_peering_location: Optional[pulumi.Input[str]] = None,
                 provider_primary_peering_location: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input['PeeringServiceSkuArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a PeeringService resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] location: The location of the resource.
        :param pulumi.Input[str] peering_service_location: The location (state/province) of the customer.
        :param pulumi.Input[str] peering_service_name: The name of the peering service.
        :param pulumi.Input[str] peering_service_provider: The name of the service provider.
        :param pulumi.Input[str] provider_backup_peering_location: The backup peering (Microsoft/service provider) location to be used for customer traffic.
        :param pulumi.Input[str] provider_primary_peering_location: The primary peering (Microsoft/service provider) location to be used for customer traffic.
        :param pulumi.Input['PeeringServiceSkuArgs'] sku: The SKU that defines the type of the peering service.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if peering_service_location is not None:
            pulumi.set(__self__, "peering_service_location", peering_service_location)
        if peering_service_name is not None:
            pulumi.set(__self__, "peering_service_name", peering_service_name)
        if peering_service_provider is not None:
            pulumi.set(__self__, "peering_service_provider", peering_service_provider)
        if provider_backup_peering_location is not None:
            pulumi.set(__self__, "provider_backup_peering_location", provider_backup_peering_location)
        if provider_primary_peering_location is not None:
            pulumi.set(__self__, "provider_primary_peering_location", provider_primary_peering_location)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the resource.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="peeringServiceLocation")
    def peering_service_location(self) -> Optional[pulumi.Input[str]]:
        """
        The location (state/province) of the customer.
        """
        return pulumi.get(self, "peering_service_location")

    @peering_service_location.setter
    def peering_service_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "peering_service_location", value)

    @property
    @pulumi.getter(name="peeringServiceName")
    def peering_service_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the peering service.
        """
        return pulumi.get(self, "peering_service_name")

    @peering_service_name.setter
    def peering_service_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "peering_service_name", value)

    @property
    @pulumi.getter(name="peeringServiceProvider")
    def peering_service_provider(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the service provider.
        """
        return pulumi.get(self, "peering_service_provider")

    @peering_service_provider.setter
    def peering_service_provider(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "peering_service_provider", value)

    @property
    @pulumi.getter(name="providerBackupPeeringLocation")
    def provider_backup_peering_location(self) -> Optional[pulumi.Input[str]]:
        """
        The backup peering (Microsoft/service provider) location to be used for customer traffic.
        """
        return pulumi.get(self, "provider_backup_peering_location")

    @provider_backup_peering_location.setter
    def provider_backup_peering_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "provider_backup_peering_location", value)

    @property
    @pulumi.getter(name="providerPrimaryPeeringLocation")
    def provider_primary_peering_location(self) -> Optional[pulumi.Input[str]]:
        """
        The primary peering (Microsoft/service provider) location to be used for customer traffic.
        """
        return pulumi.get(self, "provider_primary_peering_location")

    @provider_primary_peering_location.setter
    def provider_primary_peering_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "provider_primary_peering_location", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['PeeringServiceSkuArgs']]:
        """
        The SKU that defines the type of the peering service.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['PeeringServiceSkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class PeeringService(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 peering_service_location: Optional[pulumi.Input[str]] = None,
                 peering_service_name: Optional[pulumi.Input[str]] = None,
                 peering_service_provider: Optional[pulumi.Input[str]] = None,
                 provider_backup_peering_location: Optional[pulumi.Input[str]] = None,
                 provider_primary_peering_location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['PeeringServiceSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Peering Service

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The location of the resource.
        :param pulumi.Input[str] peering_service_location: The location (state/province) of the customer.
        :param pulumi.Input[str] peering_service_name: The name of the peering service.
        :param pulumi.Input[str] peering_service_provider: The name of the service provider.
        :param pulumi.Input[str] provider_backup_peering_location: The backup peering (Microsoft/service provider) location to be used for customer traffic.
        :param pulumi.Input[str] provider_primary_peering_location: The primary peering (Microsoft/service provider) location to be used for customer traffic.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['PeeringServiceSkuArgs']] sku: The SKU that defines the type of the peering service.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PeeringServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Peering Service

        :param str resource_name: The name of the resource.
        :param PeeringServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PeeringServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 peering_service_location: Optional[pulumi.Input[str]] = None,
                 peering_service_name: Optional[pulumi.Input[str]] = None,
                 peering_service_provider: Optional[pulumi.Input[str]] = None,
                 provider_backup_peering_location: Optional[pulumi.Input[str]] = None,
                 provider_primary_peering_location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['PeeringServiceSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
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
            __props__ = PeeringServiceArgs.__new__(PeeringServiceArgs)

            __props__.__dict__["location"] = location
            __props__.__dict__["peering_service_location"] = peering_service_location
            __props__.__dict__["peering_service_name"] = peering_service_name
            __props__.__dict__["peering_service_provider"] = peering_service_provider
            __props__.__dict__["provider_backup_peering_location"] = provider_backup_peering_location
            __props__.__dict__["provider_primary_peering_location"] = provider_primary_peering_location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["log_analytics_workspace_properties"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:peering:PeeringService"), pulumi.Alias(type_="azure-native:peering/v20190801preview:PeeringService"), pulumi.Alias(type_="azure-native:peering/v20190901preview:PeeringService"), pulumi.Alias(type_="azure-native:peering/v20200101preview:PeeringService"), pulumi.Alias(type_="azure-native:peering/v20200401:PeeringService"), pulumi.Alias(type_="azure-native:peering/v20201001:PeeringService"), pulumi.Alias(type_="azure-native:peering/v20210101:PeeringService"), pulumi.Alias(type_="azure-native:peering/v20210601:PeeringService")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(PeeringService, __self__).__init__(
            'azure-native:peering/v20220101:PeeringService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PeeringService':
        """
        Get an existing PeeringService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PeeringServiceArgs.__new__(PeeringServiceArgs)

        __props__.__dict__["location"] = None
        __props__.__dict__["log_analytics_workspace_properties"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["peering_service_location"] = None
        __props__.__dict__["peering_service_provider"] = None
        __props__.__dict__["provider_backup_peering_location"] = None
        __props__.__dict__["provider_primary_peering_location"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return PeeringService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceProperties")
    def log_analytics_workspace_properties(self) -> pulumi.Output[Optional['outputs.LogAnalyticsWorkspacePropertiesResponse']]:
        """
        The Log Analytics Workspace Properties
        """
        return pulumi.get(self, "log_analytics_workspace_properties")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="peeringServiceLocation")
    def peering_service_location(self) -> pulumi.Output[Optional[str]]:
        """
        The location (state/province) of the customer.
        """
        return pulumi.get(self, "peering_service_location")

    @property
    @pulumi.getter(name="peeringServiceProvider")
    def peering_service_provider(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the service provider.
        """
        return pulumi.get(self, "peering_service_provider")

    @property
    @pulumi.getter(name="providerBackupPeeringLocation")
    def provider_backup_peering_location(self) -> pulumi.Output[Optional[str]]:
        """
        The backup peering (Microsoft/service provider) location to be used for customer traffic.
        """
        return pulumi.get(self, "provider_backup_peering_location")

    @property
    @pulumi.getter(name="providerPrimaryPeeringLocation")
    def provider_primary_peering_location(self) -> pulumi.Output[Optional[str]]:
        """
        The primary peering (Microsoft/service provider) location to be used for customer traffic.
        """
        return pulumi.get(self, "provider_primary_peering_location")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.PeeringServiceSkuResponse']]:
        """
        The SKU that defines the type of the peering service.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

