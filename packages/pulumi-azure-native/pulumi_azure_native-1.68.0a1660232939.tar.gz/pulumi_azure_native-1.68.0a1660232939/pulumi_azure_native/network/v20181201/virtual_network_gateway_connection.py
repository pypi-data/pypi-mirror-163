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

__all__ = ['VirtualNetworkGatewayConnectionArgs', 'VirtualNetworkGatewayConnection']

@pulumi.input_type
class VirtualNetworkGatewayConnectionArgs:
    def __init__(__self__, *,
                 connection_type: pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionType']],
                 resource_group_name: pulumi.Input[str],
                 virtual_network_gateway1: pulumi.Input['VirtualNetworkGatewayArgs'],
                 authorization_key: Optional[pulumi.Input[str]] = None,
                 connection_protocol: Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionProtocol']]] = None,
                 enable_bgp: Optional[pulumi.Input[bool]] = None,
                 express_route_gateway_bypass: Optional[pulumi.Input[bool]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ipsec_policies: Optional[pulumi.Input[Sequence[pulumi.Input['IpsecPolicyArgs']]]] = None,
                 local_network_gateway2: Optional[pulumi.Input['LocalNetworkGatewayArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 peer: Optional[pulumi.Input['SubResourceArgs']] = None,
                 resource_guid: Optional[pulumi.Input[str]] = None,
                 routing_weight: Optional[pulumi.Input[int]] = None,
                 shared_key: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 use_policy_based_traffic_selectors: Optional[pulumi.Input[bool]] = None,
                 virtual_network_gateway2: Optional[pulumi.Input['VirtualNetworkGatewayArgs']] = None,
                 virtual_network_gateway_connection_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a VirtualNetworkGatewayConnection resource.
        :param pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionType']] connection_type: Gateway connection type. Possible values are: 'Ipsec','Vnet2Vnet','ExpressRoute', and 'VPNClient.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input['VirtualNetworkGatewayArgs'] virtual_network_gateway1: The reference to virtual network gateway resource.
        :param pulumi.Input[str] authorization_key: The authorizationKey.
        :param pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionProtocol']] connection_protocol: Connection protocol used for this connection
        :param pulumi.Input[bool] enable_bgp: EnableBgp flag
        :param pulumi.Input[bool] express_route_gateway_bypass: Bypass ExpressRoute Gateway for data forwarding
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input['IpsecPolicyArgs']]] ipsec_policies: The IPSec Policies to be considered by this connection.
        :param pulumi.Input['LocalNetworkGatewayArgs'] local_network_gateway2: The reference to local network gateway resource.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input['SubResourceArgs'] peer: The reference to peerings resource.
        :param pulumi.Input[str] resource_guid: The resource GUID property of the VirtualNetworkGatewayConnection resource.
        :param pulumi.Input[int] routing_weight: The routing weight.
        :param pulumi.Input[str] shared_key: The IPSec shared key.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[bool] use_policy_based_traffic_selectors: Enable policy-based traffic selectors.
        :param pulumi.Input['VirtualNetworkGatewayArgs'] virtual_network_gateway2: The reference to virtual network gateway resource.
        :param pulumi.Input[str] virtual_network_gateway_connection_name: The name of the virtual network gateway connection.
        """
        pulumi.set(__self__, "connection_type", connection_type)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "virtual_network_gateway1", virtual_network_gateway1)
        if authorization_key is not None:
            pulumi.set(__self__, "authorization_key", authorization_key)
        if connection_protocol is not None:
            pulumi.set(__self__, "connection_protocol", connection_protocol)
        if enable_bgp is not None:
            pulumi.set(__self__, "enable_bgp", enable_bgp)
        if express_route_gateway_bypass is not None:
            pulumi.set(__self__, "express_route_gateway_bypass", express_route_gateway_bypass)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if ipsec_policies is not None:
            pulumi.set(__self__, "ipsec_policies", ipsec_policies)
        if local_network_gateway2 is not None:
            pulumi.set(__self__, "local_network_gateway2", local_network_gateway2)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if peer is not None:
            pulumi.set(__self__, "peer", peer)
        if resource_guid is not None:
            pulumi.set(__self__, "resource_guid", resource_guid)
        if routing_weight is not None:
            pulumi.set(__self__, "routing_weight", routing_weight)
        if shared_key is not None:
            pulumi.set(__self__, "shared_key", shared_key)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if use_policy_based_traffic_selectors is not None:
            pulumi.set(__self__, "use_policy_based_traffic_selectors", use_policy_based_traffic_selectors)
        if virtual_network_gateway2 is not None:
            pulumi.set(__self__, "virtual_network_gateway2", virtual_network_gateway2)
        if virtual_network_gateway_connection_name is not None:
            pulumi.set(__self__, "virtual_network_gateway_connection_name", virtual_network_gateway_connection_name)

    @property
    @pulumi.getter(name="connectionType")
    def connection_type(self) -> pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionType']]:
        """
        Gateway connection type. Possible values are: 'Ipsec','Vnet2Vnet','ExpressRoute', and 'VPNClient.
        """
        return pulumi.get(self, "connection_type")

    @connection_type.setter
    def connection_type(self, value: pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionType']]):
        pulumi.set(self, "connection_type", value)

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
    @pulumi.getter(name="virtualNetworkGateway1")
    def virtual_network_gateway1(self) -> pulumi.Input['VirtualNetworkGatewayArgs']:
        """
        The reference to virtual network gateway resource.
        """
        return pulumi.get(self, "virtual_network_gateway1")

    @virtual_network_gateway1.setter
    def virtual_network_gateway1(self, value: pulumi.Input['VirtualNetworkGatewayArgs']):
        pulumi.set(self, "virtual_network_gateway1", value)

    @property
    @pulumi.getter(name="authorizationKey")
    def authorization_key(self) -> Optional[pulumi.Input[str]]:
        """
        The authorizationKey.
        """
        return pulumi.get(self, "authorization_key")

    @authorization_key.setter
    def authorization_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authorization_key", value)

    @property
    @pulumi.getter(name="connectionProtocol")
    def connection_protocol(self) -> Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionProtocol']]]:
        """
        Connection protocol used for this connection
        """
        return pulumi.get(self, "connection_protocol")

    @connection_protocol.setter
    def connection_protocol(self, value: Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionProtocol']]]):
        pulumi.set(self, "connection_protocol", value)

    @property
    @pulumi.getter(name="enableBgp")
    def enable_bgp(self) -> Optional[pulumi.Input[bool]]:
        """
        EnableBgp flag
        """
        return pulumi.get(self, "enable_bgp")

    @enable_bgp.setter
    def enable_bgp(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_bgp", value)

    @property
    @pulumi.getter(name="expressRouteGatewayBypass")
    def express_route_gateway_bypass(self) -> Optional[pulumi.Input[bool]]:
        """
        Bypass ExpressRoute Gateway for data forwarding
        """
        return pulumi.get(self, "express_route_gateway_bypass")

    @express_route_gateway_bypass.setter
    def express_route_gateway_bypass(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "express_route_gateway_bypass", value)

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
    @pulumi.getter(name="ipsecPolicies")
    def ipsec_policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IpsecPolicyArgs']]]]:
        """
        The IPSec Policies to be considered by this connection.
        """
        return pulumi.get(self, "ipsec_policies")

    @ipsec_policies.setter
    def ipsec_policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IpsecPolicyArgs']]]]):
        pulumi.set(self, "ipsec_policies", value)

    @property
    @pulumi.getter(name="localNetworkGateway2")
    def local_network_gateway2(self) -> Optional[pulumi.Input['LocalNetworkGatewayArgs']]:
        """
        The reference to local network gateway resource.
        """
        return pulumi.get(self, "local_network_gateway2")

    @local_network_gateway2.setter
    def local_network_gateway2(self, value: Optional[pulumi.Input['LocalNetworkGatewayArgs']]):
        pulumi.set(self, "local_network_gateway2", value)

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
    def peer(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        The reference to peerings resource.
        """
        return pulumi.get(self, "peer")

    @peer.setter
    def peer(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, "peer", value)

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> Optional[pulumi.Input[str]]:
        """
        The resource GUID property of the VirtualNetworkGatewayConnection resource.
        """
        return pulumi.get(self, "resource_guid")

    @resource_guid.setter
    def resource_guid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_guid", value)

    @property
    @pulumi.getter(name="routingWeight")
    def routing_weight(self) -> Optional[pulumi.Input[int]]:
        """
        The routing weight.
        """
        return pulumi.get(self, "routing_weight")

    @routing_weight.setter
    def routing_weight(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "routing_weight", value)

    @property
    @pulumi.getter(name="sharedKey")
    def shared_key(self) -> Optional[pulumi.Input[str]]:
        """
        The IPSec shared key.
        """
        return pulumi.get(self, "shared_key")

    @shared_key.setter
    def shared_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "shared_key", value)

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
    @pulumi.getter(name="usePolicyBasedTrafficSelectors")
    def use_policy_based_traffic_selectors(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable policy-based traffic selectors.
        """
        return pulumi.get(self, "use_policy_based_traffic_selectors")

    @use_policy_based_traffic_selectors.setter
    def use_policy_based_traffic_selectors(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "use_policy_based_traffic_selectors", value)

    @property
    @pulumi.getter(name="virtualNetworkGateway2")
    def virtual_network_gateway2(self) -> Optional[pulumi.Input['VirtualNetworkGatewayArgs']]:
        """
        The reference to virtual network gateway resource.
        """
        return pulumi.get(self, "virtual_network_gateway2")

    @virtual_network_gateway2.setter
    def virtual_network_gateway2(self, value: Optional[pulumi.Input['VirtualNetworkGatewayArgs']]):
        pulumi.set(self, "virtual_network_gateway2", value)

    @property
    @pulumi.getter(name="virtualNetworkGatewayConnectionName")
    def virtual_network_gateway_connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the virtual network gateway connection.
        """
        return pulumi.get(self, "virtual_network_gateway_connection_name")

    @virtual_network_gateway_connection_name.setter
    def virtual_network_gateway_connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_network_gateway_connection_name", value)


class VirtualNetworkGatewayConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorization_key: Optional[pulumi.Input[str]] = None,
                 connection_protocol: Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionProtocol']]] = None,
                 connection_type: Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionType']]] = None,
                 enable_bgp: Optional[pulumi.Input[bool]] = None,
                 express_route_gateway_bypass: Optional[pulumi.Input[bool]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ipsec_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpsecPolicyArgs']]]]] = None,
                 local_network_gateway2: Optional[pulumi.Input[pulumi.InputType['LocalNetworkGatewayArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 peer: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_guid: Optional[pulumi.Input[str]] = None,
                 routing_weight: Optional[pulumi.Input[int]] = None,
                 shared_key: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 use_policy_based_traffic_selectors: Optional[pulumi.Input[bool]] = None,
                 virtual_network_gateway1: Optional[pulumi.Input[pulumi.InputType['VirtualNetworkGatewayArgs']]] = None,
                 virtual_network_gateway2: Optional[pulumi.Input[pulumi.InputType['VirtualNetworkGatewayArgs']]] = None,
                 virtual_network_gateway_connection_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A common class for general resource information

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authorization_key: The authorizationKey.
        :param pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionProtocol']] connection_protocol: Connection protocol used for this connection
        :param pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionType']] connection_type: Gateway connection type. Possible values are: 'Ipsec','Vnet2Vnet','ExpressRoute', and 'VPNClient.
        :param pulumi.Input[bool] enable_bgp: EnableBgp flag
        :param pulumi.Input[bool] express_route_gateway_bypass: Bypass ExpressRoute Gateway for data forwarding
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpsecPolicyArgs']]]] ipsec_policies: The IPSec Policies to be considered by this connection.
        :param pulumi.Input[pulumi.InputType['LocalNetworkGatewayArgs']] local_network_gateway2: The reference to local network gateway resource.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] peer: The reference to peerings resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] resource_guid: The resource GUID property of the VirtualNetworkGatewayConnection resource.
        :param pulumi.Input[int] routing_weight: The routing weight.
        :param pulumi.Input[str] shared_key: The IPSec shared key.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[bool] use_policy_based_traffic_selectors: Enable policy-based traffic selectors.
        :param pulumi.Input[pulumi.InputType['VirtualNetworkGatewayArgs']] virtual_network_gateway1: The reference to virtual network gateway resource.
        :param pulumi.Input[pulumi.InputType['VirtualNetworkGatewayArgs']] virtual_network_gateway2: The reference to virtual network gateway resource.
        :param pulumi.Input[str] virtual_network_gateway_connection_name: The name of the virtual network gateway connection.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VirtualNetworkGatewayConnectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A common class for general resource information

        :param str resource_name: The name of the resource.
        :param VirtualNetworkGatewayConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VirtualNetworkGatewayConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorization_key: Optional[pulumi.Input[str]] = None,
                 connection_protocol: Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionProtocol']]] = None,
                 connection_type: Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionType']]] = None,
                 enable_bgp: Optional[pulumi.Input[bool]] = None,
                 express_route_gateway_bypass: Optional[pulumi.Input[bool]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ipsec_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpsecPolicyArgs']]]]] = None,
                 local_network_gateway2: Optional[pulumi.Input[pulumi.InputType['LocalNetworkGatewayArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 peer: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_guid: Optional[pulumi.Input[str]] = None,
                 routing_weight: Optional[pulumi.Input[int]] = None,
                 shared_key: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 use_policy_based_traffic_selectors: Optional[pulumi.Input[bool]] = None,
                 virtual_network_gateway1: Optional[pulumi.Input[pulumi.InputType['VirtualNetworkGatewayArgs']]] = None,
                 virtual_network_gateway2: Optional[pulumi.Input[pulumi.InputType['VirtualNetworkGatewayArgs']]] = None,
                 virtual_network_gateway_connection_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = VirtualNetworkGatewayConnectionArgs.__new__(VirtualNetworkGatewayConnectionArgs)

            __props__.__dict__["authorization_key"] = authorization_key
            __props__.__dict__["connection_protocol"] = connection_protocol
            if connection_type is None and not opts.urn:
                raise TypeError("Missing required property 'connection_type'")
            __props__.__dict__["connection_type"] = connection_type
            __props__.__dict__["enable_bgp"] = enable_bgp
            __props__.__dict__["express_route_gateway_bypass"] = express_route_gateway_bypass
            __props__.__dict__["id"] = id
            __props__.__dict__["ipsec_policies"] = ipsec_policies
            __props__.__dict__["local_network_gateway2"] = local_network_gateway2
            __props__.__dict__["location"] = location
            __props__.__dict__["peer"] = peer
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_guid"] = resource_guid
            __props__.__dict__["routing_weight"] = routing_weight
            __props__.__dict__["shared_key"] = shared_key
            __props__.__dict__["tags"] = tags
            __props__.__dict__["use_policy_based_traffic_selectors"] = use_policy_based_traffic_selectors
            if virtual_network_gateway1 is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_network_gateway1'")
            __props__.__dict__["virtual_network_gateway1"] = virtual_network_gateway1
            __props__.__dict__["virtual_network_gateway2"] = virtual_network_gateway2
            __props__.__dict__["virtual_network_gateway_connection_name"] = virtual_network_gateway_connection_name
            __props__.__dict__["connection_status"] = None
            __props__.__dict__["egress_bytes_transferred"] = None
            __props__.__dict__["etag"] = None
            __props__.__dict__["ingress_bytes_transferred"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["tunnel_connection_status"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20150615:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20160330:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20160601:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20160901:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20161201:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20170301:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20170601:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20170801:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20170901:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20171001:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20171101:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20180101:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20180201:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20180401:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20180601:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20180701:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20180801:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20181001:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20181101:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20190201:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20190401:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20190601:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20190701:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20190801:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20190901:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20191101:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20191201:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20200301:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20200401:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20200501:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20200601:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20200701:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20200801:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20201101:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20210201:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20210301:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20210501:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20210801:VirtualNetworkGatewayConnection"), pulumi.Alias(type_="azure-native:network/v20220101:VirtualNetworkGatewayConnection")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VirtualNetworkGatewayConnection, __self__).__init__(
            'azure-native:network/v20181201:VirtualNetworkGatewayConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VirtualNetworkGatewayConnection':
        """
        Get an existing VirtualNetworkGatewayConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = VirtualNetworkGatewayConnectionArgs.__new__(VirtualNetworkGatewayConnectionArgs)

        __props__.__dict__["authorization_key"] = None
        __props__.__dict__["connection_protocol"] = None
        __props__.__dict__["connection_status"] = None
        __props__.__dict__["connection_type"] = None
        __props__.__dict__["egress_bytes_transferred"] = None
        __props__.__dict__["enable_bgp"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["express_route_gateway_bypass"] = None
        __props__.__dict__["ingress_bytes_transferred"] = None
        __props__.__dict__["ipsec_policies"] = None
        __props__.__dict__["local_network_gateway2"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["peer"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["resource_guid"] = None
        __props__.__dict__["routing_weight"] = None
        __props__.__dict__["shared_key"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["tunnel_connection_status"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["use_policy_based_traffic_selectors"] = None
        __props__.__dict__["virtual_network_gateway1"] = None
        __props__.__dict__["virtual_network_gateway2"] = None
        return VirtualNetworkGatewayConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="authorizationKey")
    def authorization_key(self) -> pulumi.Output[Optional[str]]:
        """
        The authorizationKey.
        """
        return pulumi.get(self, "authorization_key")

    @property
    @pulumi.getter(name="connectionProtocol")
    def connection_protocol(self) -> pulumi.Output[Optional[str]]:
        """
        Connection protocol used for this connection
        """
        return pulumi.get(self, "connection_protocol")

    @property
    @pulumi.getter(name="connectionStatus")
    def connection_status(self) -> pulumi.Output[str]:
        """
        Virtual network Gateway connection status. Possible values are 'Unknown', 'Connecting', 'Connected' and 'NotConnected'.
        """
        return pulumi.get(self, "connection_status")

    @property
    @pulumi.getter(name="connectionType")
    def connection_type(self) -> pulumi.Output[str]:
        """
        Gateway connection type. Possible values are: 'Ipsec','Vnet2Vnet','ExpressRoute', and 'VPNClient.
        """
        return pulumi.get(self, "connection_type")

    @property
    @pulumi.getter(name="egressBytesTransferred")
    def egress_bytes_transferred(self) -> pulumi.Output[float]:
        """
        The egress bytes transferred in this connection.
        """
        return pulumi.get(self, "egress_bytes_transferred")

    @property
    @pulumi.getter(name="enableBgp")
    def enable_bgp(self) -> pulumi.Output[Optional[bool]]:
        """
        EnableBgp flag
        """
        return pulumi.get(self, "enable_bgp")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Gets a unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="expressRouteGatewayBypass")
    def express_route_gateway_bypass(self) -> pulumi.Output[Optional[bool]]:
        """
        Bypass ExpressRoute Gateway for data forwarding
        """
        return pulumi.get(self, "express_route_gateway_bypass")

    @property
    @pulumi.getter(name="ingressBytesTransferred")
    def ingress_bytes_transferred(self) -> pulumi.Output[float]:
        """
        The ingress bytes transferred in this connection.
        """
        return pulumi.get(self, "ingress_bytes_transferred")

    @property
    @pulumi.getter(name="ipsecPolicies")
    def ipsec_policies(self) -> pulumi.Output[Optional[Sequence['outputs.IpsecPolicyResponse']]]:
        """
        The IPSec Policies to be considered by this connection.
        """
        return pulumi.get(self, "ipsec_policies")

    @property
    @pulumi.getter(name="localNetworkGateway2")
    def local_network_gateway2(self) -> pulumi.Output[Optional['outputs.LocalNetworkGatewayResponse']]:
        """
        The reference to local network gateway resource.
        """
        return pulumi.get(self, "local_network_gateway2")

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
    @pulumi.getter
    def peer(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        The reference to peerings resource.
        """
        return pulumi.get(self, "peer")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the VirtualNetworkGatewayConnection resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> pulumi.Output[Optional[str]]:
        """
        The resource GUID property of the VirtualNetworkGatewayConnection resource.
        """
        return pulumi.get(self, "resource_guid")

    @property
    @pulumi.getter(name="routingWeight")
    def routing_weight(self) -> pulumi.Output[Optional[int]]:
        """
        The routing weight.
        """
        return pulumi.get(self, "routing_weight")

    @property
    @pulumi.getter(name="sharedKey")
    def shared_key(self) -> pulumi.Output[Optional[str]]:
        """
        The IPSec shared key.
        """
        return pulumi.get(self, "shared_key")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tunnelConnectionStatus")
    def tunnel_connection_status(self) -> pulumi.Output[Sequence['outputs.TunnelConnectionHealthResponse']]:
        """
        Collection of all tunnels' connection health status.
        """
        return pulumi.get(self, "tunnel_connection_status")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="usePolicyBasedTrafficSelectors")
    def use_policy_based_traffic_selectors(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable policy-based traffic selectors.
        """
        return pulumi.get(self, "use_policy_based_traffic_selectors")

    @property
    @pulumi.getter(name="virtualNetworkGateway1")
    def virtual_network_gateway1(self) -> pulumi.Output['outputs.VirtualNetworkGatewayResponse']:
        """
        The reference to virtual network gateway resource.
        """
        return pulumi.get(self, "virtual_network_gateway1")

    @property
    @pulumi.getter(name="virtualNetworkGateway2")
    def virtual_network_gateway2(self) -> pulumi.Output[Optional['outputs.VirtualNetworkGatewayResponse']]:
        """
        The reference to virtual network gateway resource.
        """
        return pulumi.get(self, "virtual_network_gateway2")

