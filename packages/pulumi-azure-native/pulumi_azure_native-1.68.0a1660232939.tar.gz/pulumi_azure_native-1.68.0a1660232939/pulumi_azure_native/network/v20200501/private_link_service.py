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

__all__ = ['PrivateLinkServiceArgs', 'PrivateLinkService']

@pulumi.input_type
class PrivateLinkServiceArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 auto_approval: Optional[pulumi.Input['PrivateLinkServicePropertiesAutoApprovalArgs']] = None,
                 enable_proxy_protocol: Optional[pulumi.Input[bool]] = None,
                 fqdns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['PrivateLinkServiceIpConfigurationArgs']]]] = None,
                 load_balancer_frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['FrontendIPConfigurationArgs']]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 visibility: Optional[pulumi.Input['PrivateLinkServicePropertiesVisibilityArgs']] = None):
        """
        The set of arguments for constructing a PrivateLinkService resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input['PrivateLinkServicePropertiesAutoApprovalArgs'] auto_approval: The auto-approval list of the private link service.
        :param pulumi.Input[bool] enable_proxy_protocol: Whether the private link service is enabled for proxy protocol or not.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] fqdns: The list of Fqdn.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input['PrivateLinkServiceIpConfigurationArgs']]] ip_configurations: An array of private link service IP configurations.
        :param pulumi.Input[Sequence[pulumi.Input['FrontendIPConfigurationArgs']]] load_balancer_frontend_ip_configurations: An array of references to the load balancer IP configurations.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] service_name: The name of the private link service.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input['PrivateLinkServicePropertiesVisibilityArgs'] visibility: The visibility list of the private link service.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if auto_approval is not None:
            pulumi.set(__self__, "auto_approval", auto_approval)
        if enable_proxy_protocol is not None:
            pulumi.set(__self__, "enable_proxy_protocol", enable_proxy_protocol)
        if fqdns is not None:
            pulumi.set(__self__, "fqdns", fqdns)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if ip_configurations is not None:
            pulumi.set(__self__, "ip_configurations", ip_configurations)
        if load_balancer_frontend_ip_configurations is not None:
            pulumi.set(__self__, "load_balancer_frontend_ip_configurations", load_balancer_frontend_ip_configurations)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if service_name is not None:
            pulumi.set(__self__, "service_name", service_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if visibility is not None:
            pulumi.set(__self__, "visibility", visibility)

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
    @pulumi.getter(name="autoApproval")
    def auto_approval(self) -> Optional[pulumi.Input['PrivateLinkServicePropertiesAutoApprovalArgs']]:
        """
        The auto-approval list of the private link service.
        """
        return pulumi.get(self, "auto_approval")

    @auto_approval.setter
    def auto_approval(self, value: Optional[pulumi.Input['PrivateLinkServicePropertiesAutoApprovalArgs']]):
        pulumi.set(self, "auto_approval", value)

    @property
    @pulumi.getter(name="enableProxyProtocol")
    def enable_proxy_protocol(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the private link service is enabled for proxy protocol or not.
        """
        return pulumi.get(self, "enable_proxy_protocol")

    @enable_proxy_protocol.setter
    def enable_proxy_protocol(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_proxy_protocol", value)

    @property
    @pulumi.getter
    def fqdns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of Fqdn.
        """
        return pulumi.get(self, "fqdns")

    @fqdns.setter
    def fqdns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "fqdns", value)

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
    @pulumi.getter(name="ipConfigurations")
    def ip_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PrivateLinkServiceIpConfigurationArgs']]]]:
        """
        An array of private link service IP configurations.
        """
        return pulumi.get(self, "ip_configurations")

    @ip_configurations.setter
    def ip_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PrivateLinkServiceIpConfigurationArgs']]]]):
        pulumi.set(self, "ip_configurations", value)

    @property
    @pulumi.getter(name="loadBalancerFrontendIpConfigurations")
    def load_balancer_frontend_ip_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FrontendIPConfigurationArgs']]]]:
        """
        An array of references to the load balancer IP configurations.
        """
        return pulumi.get(self, "load_balancer_frontend_ip_configurations")

    @load_balancer_frontend_ip_configurations.setter
    def load_balancer_frontend_ip_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FrontendIPConfigurationArgs']]]]):
        pulumi.set(self, "load_balancer_frontend_ip_configurations", value)

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
    @pulumi.getter(name="serviceName")
    def service_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the private link service.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_name", value)

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
    def visibility(self) -> Optional[pulumi.Input['PrivateLinkServicePropertiesVisibilityArgs']]:
        """
        The visibility list of the private link service.
        """
        return pulumi.get(self, "visibility")

    @visibility.setter
    def visibility(self, value: Optional[pulumi.Input['PrivateLinkServicePropertiesVisibilityArgs']]):
        pulumi.set(self, "visibility", value)


class PrivateLinkService(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_approval: Optional[pulumi.Input[pulumi.InputType['PrivateLinkServicePropertiesAutoApprovalArgs']]] = None,
                 enable_proxy_protocol: Optional[pulumi.Input[bool]] = None,
                 fqdns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PrivateLinkServiceIpConfigurationArgs']]]]] = None,
                 load_balancer_frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FrontendIPConfigurationArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 visibility: Optional[pulumi.Input[pulumi.InputType['PrivateLinkServicePropertiesVisibilityArgs']]] = None,
                 __props__=None):
        """
        Private link service resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['PrivateLinkServicePropertiesAutoApprovalArgs']] auto_approval: The auto-approval list of the private link service.
        :param pulumi.Input[bool] enable_proxy_protocol: Whether the private link service is enabled for proxy protocol or not.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] fqdns: The list of Fqdn.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PrivateLinkServiceIpConfigurationArgs']]]] ip_configurations: An array of private link service IP configurations.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FrontendIPConfigurationArgs']]]] load_balancer_frontend_ip_configurations: An array of references to the load balancer IP configurations.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the private link service.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[pulumi.InputType['PrivateLinkServicePropertiesVisibilityArgs']] visibility: The visibility list of the private link service.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PrivateLinkServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Private link service resource.

        :param str resource_name: The name of the resource.
        :param PrivateLinkServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PrivateLinkServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_approval: Optional[pulumi.Input[pulumi.InputType['PrivateLinkServicePropertiesAutoApprovalArgs']]] = None,
                 enable_proxy_protocol: Optional[pulumi.Input[bool]] = None,
                 fqdns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PrivateLinkServiceIpConfigurationArgs']]]]] = None,
                 load_balancer_frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FrontendIPConfigurationArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 visibility: Optional[pulumi.Input[pulumi.InputType['PrivateLinkServicePropertiesVisibilityArgs']]] = None,
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
            __props__ = PrivateLinkServiceArgs.__new__(PrivateLinkServiceArgs)

            __props__.__dict__["auto_approval"] = auto_approval
            __props__.__dict__["enable_proxy_protocol"] = enable_proxy_protocol
            __props__.__dict__["fqdns"] = fqdns
            __props__.__dict__["id"] = id
            __props__.__dict__["ip_configurations"] = ip_configurations
            __props__.__dict__["load_balancer_frontend_ip_configurations"] = load_balancer_frontend_ip_configurations
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["service_name"] = service_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["visibility"] = visibility
            __props__.__dict__["alias"] = None
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["network_interfaces"] = None
            __props__.__dict__["private_endpoint_connections"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20190401:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20190601:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20190701:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20190801:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20190901:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20191101:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20191201:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20200301:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20200401:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20200601:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20200701:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20200801:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20201101:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20210201:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20210301:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20210501:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20210801:PrivateLinkService"), pulumi.Alias(type_="azure-native:network/v20220101:PrivateLinkService")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(PrivateLinkService, __self__).__init__(
            'azure-native:network/v20200501:PrivateLinkService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PrivateLinkService':
        """
        Get an existing PrivateLinkService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PrivateLinkServiceArgs.__new__(PrivateLinkServiceArgs)

        __props__.__dict__["alias"] = None
        __props__.__dict__["auto_approval"] = None
        __props__.__dict__["enable_proxy_protocol"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["fqdns"] = None
        __props__.__dict__["ip_configurations"] = None
        __props__.__dict__["load_balancer_frontend_ip_configurations"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["network_interfaces"] = None
        __props__.__dict__["private_endpoint_connections"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["visibility"] = None
        return PrivateLinkService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def alias(self) -> pulumi.Output[str]:
        """
        The alias of the private link service.
        """
        return pulumi.get(self, "alias")

    @property
    @pulumi.getter(name="autoApproval")
    def auto_approval(self) -> pulumi.Output[Optional['outputs.PrivateLinkServicePropertiesResponseAutoApproval']]:
        """
        The auto-approval list of the private link service.
        """
        return pulumi.get(self, "auto_approval")

    @property
    @pulumi.getter(name="enableProxyProtocol")
    def enable_proxy_protocol(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether the private link service is enabled for proxy protocol or not.
        """
        return pulumi.get(self, "enable_proxy_protocol")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def fqdns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The list of Fqdn.
        """
        return pulumi.get(self, "fqdns")

    @property
    @pulumi.getter(name="ipConfigurations")
    def ip_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.PrivateLinkServiceIpConfigurationResponse']]]:
        """
        An array of private link service IP configurations.
        """
        return pulumi.get(self, "ip_configurations")

    @property
    @pulumi.getter(name="loadBalancerFrontendIpConfigurations")
    def load_balancer_frontend_ip_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.FrontendIPConfigurationResponse']]]:
        """
        An array of references to the load balancer IP configurations.
        """
        return pulumi.get(self, "load_balancer_frontend_ip_configurations")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> pulumi.Output[Sequence['outputs.NetworkInterfaceResponse']]:
        """
        An array of references to the network interfaces created for this private link service.
        """
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> pulumi.Output[Sequence['outputs.PrivateEndpointConnectionResponse']]:
        """
        An array of list about connections to the private endpoint.
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the private link service resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def visibility(self) -> pulumi.Output[Optional['outputs.PrivateLinkServicePropertiesResponseVisibility']]:
        """
        The visibility list of the private link service.
        """
        return pulumi.get(self, "visibility")

