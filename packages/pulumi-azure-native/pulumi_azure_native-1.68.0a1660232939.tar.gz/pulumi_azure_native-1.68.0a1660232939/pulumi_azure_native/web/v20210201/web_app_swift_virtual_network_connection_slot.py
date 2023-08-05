# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['WebAppSwiftVirtualNetworkConnectionSlotArgs', 'WebAppSwiftVirtualNetworkConnectionSlot']

@pulumi.input_type
class WebAppSwiftVirtualNetworkConnectionSlotArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 slot: pulumi.Input[str],
                 kind: Optional[pulumi.Input[str]] = None,
                 subnet_resource_id: Optional[pulumi.Input[str]] = None,
                 swift_supported: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a WebAppSwiftVirtualNetworkConnectionSlot resource.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] slot: Name of the deployment slot. If a slot is not specified, the API will add or update connections for the production slot.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] subnet_resource_id: The Virtual Network subnet's resource ID. This is the subnet that this Web App will join. This subnet must have a delegation to Microsoft.Web/serverFarms defined first.
        :param pulumi.Input[bool] swift_supported: A flag that specifies if the scale unit this Web App is on supports Swift integration.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "slot", slot)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if subnet_resource_id is not None:
            pulumi.set(__self__, "subnet_resource_id", subnet_resource_id)
        if swift_supported is not None:
            pulumi.set(__self__, "swift_supported", swift_supported)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the app.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group to which the resource belongs.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def slot(self) -> pulumi.Input[str]:
        """
        Name of the deployment slot. If a slot is not specified, the API will add or update connections for the production slot.
        """
        return pulumi.get(self, "slot")

    @slot.setter
    def slot(self, value: pulumi.Input[str]):
        pulumi.set(self, "slot", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter(name="subnetResourceId")
    def subnet_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Virtual Network subnet's resource ID. This is the subnet that this Web App will join. This subnet must have a delegation to Microsoft.Web/serverFarms defined first.
        """
        return pulumi.get(self, "subnet_resource_id")

    @subnet_resource_id.setter
    def subnet_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_resource_id", value)

    @property
    @pulumi.getter(name="swiftSupported")
    def swift_supported(self) -> Optional[pulumi.Input[bool]]:
        """
        A flag that specifies if the scale unit this Web App is on supports Swift integration.
        """
        return pulumi.get(self, "swift_supported")

    @swift_supported.setter
    def swift_supported(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "swift_supported", value)


class WebAppSwiftVirtualNetworkConnectionSlot(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 slot: Optional[pulumi.Input[str]] = None,
                 subnet_resource_id: Optional[pulumi.Input[str]] = None,
                 swift_supported: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Swift Virtual Network Contract. This is used to enable the new Swift way of doing virtual network integration.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] slot: Name of the deployment slot. If a slot is not specified, the API will add or update connections for the production slot.
        :param pulumi.Input[str] subnet_resource_id: The Virtual Network subnet's resource ID. This is the subnet that this Web App will join. This subnet must have a delegation to Microsoft.Web/serverFarms defined first.
        :param pulumi.Input[bool] swift_supported: A flag that specifies if the scale unit this Web App is on supports Swift integration.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WebAppSwiftVirtualNetworkConnectionSlotArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Swift Virtual Network Contract. This is used to enable the new Swift way of doing virtual network integration.

        :param str resource_name: The name of the resource.
        :param WebAppSwiftVirtualNetworkConnectionSlotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WebAppSwiftVirtualNetworkConnectionSlotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 slot: Optional[pulumi.Input[str]] = None,
                 subnet_resource_id: Optional[pulumi.Input[str]] = None,
                 swift_supported: Optional[pulumi.Input[bool]] = None,
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
            __props__ = WebAppSwiftVirtualNetworkConnectionSlotArgs.__new__(WebAppSwiftVirtualNetworkConnectionSlotArgs)

            __props__.__dict__["kind"] = kind
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if slot is None and not opts.urn:
                raise TypeError("Missing required property 'slot'")
            __props__.__dict__["slot"] = slot
            __props__.__dict__["subnet_resource_id"] = subnet_resource_id
            __props__.__dict__["swift_supported"] = swift_supported
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:web:WebAppSwiftVirtualNetworkConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20180201:WebAppSwiftVirtualNetworkConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20181101:WebAppSwiftVirtualNetworkConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20190801:WebAppSwiftVirtualNetworkConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20200601:WebAppSwiftVirtualNetworkConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20200901:WebAppSwiftVirtualNetworkConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20201001:WebAppSwiftVirtualNetworkConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20210115:WebAppSwiftVirtualNetworkConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20210301:WebAppSwiftVirtualNetworkConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20220301:WebAppSwiftVirtualNetworkConnectionSlot")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppSwiftVirtualNetworkConnectionSlot, __self__).__init__(
            'azure-native:web/v20210201:WebAppSwiftVirtualNetworkConnectionSlot',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebAppSwiftVirtualNetworkConnectionSlot':
        """
        Get an existing WebAppSwiftVirtualNetworkConnectionSlot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = WebAppSwiftVirtualNetworkConnectionSlotArgs.__new__(WebAppSwiftVirtualNetworkConnectionSlotArgs)

        __props__.__dict__["kind"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["subnet_resource_id"] = None
        __props__.__dict__["swift_supported"] = None
        __props__.__dict__["type"] = None
        return WebAppSwiftVirtualNetworkConnectionSlot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="subnetResourceId")
    def subnet_resource_id(self) -> pulumi.Output[Optional[str]]:
        """
        The Virtual Network subnet's resource ID. This is the subnet that this Web App will join. This subnet must have a delegation to Microsoft.Web/serverFarms defined first.
        """
        return pulumi.get(self, "subnet_resource_id")

    @property
    @pulumi.getter(name="swiftSupported")
    def swift_supported(self) -> pulumi.Output[Optional[bool]]:
        """
        A flag that specifies if the scale unit this Web App is on supports Swift integration.
        """
        return pulumi.get(self, "swift_supported")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

