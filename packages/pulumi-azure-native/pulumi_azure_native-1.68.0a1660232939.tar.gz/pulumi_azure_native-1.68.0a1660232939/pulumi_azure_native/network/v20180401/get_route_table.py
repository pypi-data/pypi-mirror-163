# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetRouteTableResult',
    'AwaitableGetRouteTableResult',
    'get_route_table',
    'get_route_table_output',
]

warnings.warn("""Version 2018-04-01 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetRouteTableResult:
    """
    Route table resource.
    """
    def __init__(__self__, disable_bgp_route_propagation=None, etag=None, id=None, location=None, name=None, provisioning_state=None, routes=None, subnets=None, tags=None, type=None):
        if disable_bgp_route_propagation and not isinstance(disable_bgp_route_propagation, bool):
            raise TypeError("Expected argument 'disable_bgp_route_propagation' to be a bool")
        pulumi.set(__self__, "disable_bgp_route_propagation", disable_bgp_route_propagation)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if routes and not isinstance(routes, list):
            raise TypeError("Expected argument 'routes' to be a list")
        pulumi.set(__self__, "routes", routes)
        if subnets and not isinstance(subnets, list):
            raise TypeError("Expected argument 'subnets' to be a list")
        pulumi.set(__self__, "subnets", subnets)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="disableBgpRoutePropagation")
    def disable_bgp_route_propagation(self) -> Optional[bool]:
        """
        Gets or sets whether to disable the routes learned by BGP on that route table. True means disable.
        """
        return pulumi.get(self, "disable_bgp_route_propagation")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Gets a unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        The provisioning state of the resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def routes(self) -> Optional[Sequence['outputs.RouteResponse']]:
        """
        Collection of routes contained within a route table.
        """
        return pulumi.get(self, "routes")

    @property
    @pulumi.getter
    def subnets(self) -> Sequence['outputs.SubnetResponse']:
        """
        A collection of references to subnets.
        """
        return pulumi.get(self, "subnets")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetRouteTableResult(GetRouteTableResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRouteTableResult(
            disable_bgp_route_propagation=self.disable_bgp_route_propagation,
            etag=self.etag,
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            routes=self.routes,
            subnets=self.subnets,
            tags=self.tags,
            type=self.type)


def get_route_table(expand: Optional[str] = None,
                    resource_group_name: Optional[str] = None,
                    route_table_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRouteTableResult:
    """
    Route table resource.


    :param str expand: Expands referenced resources.
    :param str resource_group_name: The name of the resource group.
    :param str route_table_name: The name of the route table.
    """
    pulumi.log.warn("""get_route_table is deprecated: Version 2018-04-01 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['expand'] = expand
    __args__['resourceGroupName'] = resource_group_name
    __args__['routeTableName'] = route_table_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20180401:getRouteTable', __args__, opts=opts, typ=GetRouteTableResult).value

    return AwaitableGetRouteTableResult(
        disable_bgp_route_propagation=__ret__.disable_bgp_route_propagation,
        etag=__ret__.etag,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        routes=__ret__.routes,
        subnets=__ret__.subnets,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_route_table)
def get_route_table_output(expand: Optional[pulumi.Input[Optional[str]]] = None,
                           resource_group_name: Optional[pulumi.Input[str]] = None,
                           route_table_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRouteTableResult]:
    """
    Route table resource.


    :param str expand: Expands referenced resources.
    :param str resource_group_name: The name of the resource group.
    :param str route_table_name: The name of the route table.
    """
    pulumi.log.warn("""get_route_table is deprecated: Version 2018-04-01 will be removed in v2 of the provider.""")
    ...
