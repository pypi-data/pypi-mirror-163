# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['VirtualHubIpConfigurationArgs', 'VirtualHubIpConfiguration']

@pulumi.input_type
class VirtualHubIpConfigurationArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 virtual_hub_name: pulumi.Input[str],
                 id: Optional[pulumi.Input[str]] = None,
                 ip_config_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_ip_address: Optional[pulumi.Input[str]] = None,
                 private_ip_allocation_method: Optional[pulumi.Input[Union[str, 'IPAllocationMethod']]] = None,
                 public_ip_address: Optional[pulumi.Input['PublicIPAddressArgs']] = None,
                 subnet: Optional[pulumi.Input['SubnetArgs']] = None):
        """
        The set of arguments for constructing a VirtualHubIpConfiguration resource.
        :param pulumi.Input[str] resource_group_name: The resource group name of the VirtualHub.
        :param pulumi.Input[str] virtual_hub_name: The name of the VirtualHub.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] ip_config_name: The name of the ipconfig.
        :param pulumi.Input[str] name: Name of the Ip Configuration.
        :param pulumi.Input[str] private_ip_address: The private IP address of the IP configuration.
        :param pulumi.Input[Union[str, 'IPAllocationMethod']] private_ip_allocation_method: The private IP address allocation method.
        :param pulumi.Input['PublicIPAddressArgs'] public_ip_address: The reference to the public IP resource.
        :param pulumi.Input['SubnetArgs'] subnet: The reference to the subnet resource.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "virtual_hub_name", virtual_hub_name)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if ip_config_name is not None:
            pulumi.set(__self__, "ip_config_name", ip_config_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)
        if private_ip_allocation_method is not None:
            pulumi.set(__self__, "private_ip_allocation_method", private_ip_allocation_method)
        if public_ip_address is not None:
            pulumi.set(__self__, "public_ip_address", public_ip_address)
        if subnet is not None:
            pulumi.set(__self__, "subnet", subnet)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name of the VirtualHub.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="virtualHubName")
    def virtual_hub_name(self) -> pulumi.Input[str]:
        """
        The name of the VirtualHub.
        """
        return pulumi.get(self, "virtual_hub_name")

    @virtual_hub_name.setter
    def virtual_hub_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_hub_name", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter(name="ipConfigName")
    def ip_config_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the ipconfig.
        """
        return pulumi.get(self, "ip_config_name")

    @ip_config_name.setter
    def ip_config_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_config_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Ip Configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="privateIPAddress")
    def private_ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        The private IP address of the IP configuration.
        """
        return pulumi.get(self, "private_ip_address")

    @private_ip_address.setter
    def private_ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_ip_address", value)

    @property
    @pulumi.getter(name="privateIPAllocationMethod")
    def private_ip_allocation_method(self) -> Optional[pulumi.Input[Union[str, 'IPAllocationMethod']]]:
        """
        The private IP address allocation method.
        """
        return pulumi.get(self, "private_ip_allocation_method")

    @private_ip_allocation_method.setter
    def private_ip_allocation_method(self, value: Optional[pulumi.Input[Union[str, 'IPAllocationMethod']]]):
        pulumi.set(self, "private_ip_allocation_method", value)

    @property
    @pulumi.getter(name="publicIPAddress")
    def public_ip_address(self) -> Optional[pulumi.Input['PublicIPAddressArgs']]:
        """
        The reference to the public IP resource.
        """
        return pulumi.get(self, "public_ip_address")

    @public_ip_address.setter
    def public_ip_address(self, value: Optional[pulumi.Input['PublicIPAddressArgs']]):
        pulumi.set(self, "public_ip_address", value)

    @property
    @pulumi.getter
    def subnet(self) -> Optional[pulumi.Input['SubnetArgs']]:
        """
        The reference to the subnet resource.
        """
        return pulumi.get(self, "subnet")

    @subnet.setter
    def subnet(self, value: Optional[pulumi.Input['SubnetArgs']]):
        pulumi.set(self, "subnet", value)


class VirtualHubIpConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_config_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_ip_address: Optional[pulumi.Input[str]] = None,
                 private_ip_allocation_method: Optional[pulumi.Input[Union[str, 'IPAllocationMethod']]] = None,
                 public_ip_address: Optional[pulumi.Input[pulumi.InputType['PublicIPAddressArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 subnet: Optional[pulumi.Input[pulumi.InputType['SubnetArgs']]] = None,
                 virtual_hub_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        IpConfigurations.
        API Version: 2020-11-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] ip_config_name: The name of the ipconfig.
        :param pulumi.Input[str] name: Name of the Ip Configuration.
        :param pulumi.Input[str] private_ip_address: The private IP address of the IP configuration.
        :param pulumi.Input[Union[str, 'IPAllocationMethod']] private_ip_allocation_method: The private IP address allocation method.
        :param pulumi.Input[pulumi.InputType['PublicIPAddressArgs']] public_ip_address: The reference to the public IP resource.
        :param pulumi.Input[str] resource_group_name: The resource group name of the VirtualHub.
        :param pulumi.Input[pulumi.InputType['SubnetArgs']] subnet: The reference to the subnet resource.
        :param pulumi.Input[str] virtual_hub_name: The name of the VirtualHub.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VirtualHubIpConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        IpConfigurations.
        API Version: 2020-11-01.

        :param str resource_name: The name of the resource.
        :param VirtualHubIpConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VirtualHubIpConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_config_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_ip_address: Optional[pulumi.Input[str]] = None,
                 private_ip_allocation_method: Optional[pulumi.Input[Union[str, 'IPAllocationMethod']]] = None,
                 public_ip_address: Optional[pulumi.Input[pulumi.InputType['PublicIPAddressArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 subnet: Optional[pulumi.Input[pulumi.InputType['SubnetArgs']]] = None,
                 virtual_hub_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = VirtualHubIpConfigurationArgs.__new__(VirtualHubIpConfigurationArgs)

            __props__.__dict__["id"] = id
            __props__.__dict__["ip_config_name"] = ip_config_name
            __props__.__dict__["name"] = name
            __props__.__dict__["private_ip_address"] = private_ip_address
            __props__.__dict__["private_ip_allocation_method"] = private_ip_allocation_method
            __props__.__dict__["public_ip_address"] = public_ip_address
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["subnet"] = subnet
            if virtual_hub_name is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_hub_name'")
            __props__.__dict__["virtual_hub_name"] = virtual_hub_name
            __props__.__dict__["etag"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network/v20200501:VirtualHubIpConfiguration"), pulumi.Alias(type_="azure-native:network/v20200601:VirtualHubIpConfiguration"), pulumi.Alias(type_="azure-native:network/v20200701:VirtualHubIpConfiguration"), pulumi.Alias(type_="azure-native:network/v20200801:VirtualHubIpConfiguration"), pulumi.Alias(type_="azure-native:network/v20201101:VirtualHubIpConfiguration"), pulumi.Alias(type_="azure-native:network/v20210201:VirtualHubIpConfiguration"), pulumi.Alias(type_="azure-native:network/v20210301:VirtualHubIpConfiguration"), pulumi.Alias(type_="azure-native:network/v20210501:VirtualHubIpConfiguration"), pulumi.Alias(type_="azure-native:network/v20210801:VirtualHubIpConfiguration"), pulumi.Alias(type_="azure-native:network/v20220101:VirtualHubIpConfiguration")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VirtualHubIpConfiguration, __self__).__init__(
            'azure-native:network:VirtualHubIpConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VirtualHubIpConfiguration':
        """
        Get an existing VirtualHubIpConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = VirtualHubIpConfigurationArgs.__new__(VirtualHubIpConfigurationArgs)

        __props__.__dict__["etag"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["private_ip_address"] = None
        __props__.__dict__["private_ip_allocation_method"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["public_ip_address"] = None
        __props__.__dict__["subnet"] = None
        __props__.__dict__["type"] = None
        return VirtualHubIpConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        Name of the Ip Configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateIPAddress")
    def private_ip_address(self) -> pulumi.Output[Optional[str]]:
        """
        The private IP address of the IP configuration.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="privateIPAllocationMethod")
    def private_ip_allocation_method(self) -> pulumi.Output[Optional[str]]:
        """
        The private IP address allocation method.
        """
        return pulumi.get(self, "private_ip_allocation_method")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the IP configuration resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicIPAddress")
    def public_ip_address(self) -> pulumi.Output[Optional['outputs.PublicIPAddressResponse']]:
        """
        The reference to the public IP resource.
        """
        return pulumi.get(self, "public_ip_address")

    @property
    @pulumi.getter
    def subnet(self) -> pulumi.Output[Optional['outputs.SubnetResponse']]:
        """
        The reference to the subnet resource.
        """
        return pulumi.get(self, "subnet")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Ipconfiguration type.
        """
        return pulumi.get(self, "type")

