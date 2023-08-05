# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetWebAppRelayServiceConnectionSlotResult',
    'AwaitableGetWebAppRelayServiceConnectionSlotResult',
    'get_web_app_relay_service_connection_slot',
    'get_web_app_relay_service_connection_slot_output',
]

@pulumi.output_type
class GetWebAppRelayServiceConnectionSlotResult:
    """
    Hybrid Connection for an App Service app.
    """
    def __init__(__self__, biztalk_uri=None, entity_connection_string=None, entity_name=None, hostname=None, id=None, kind=None, name=None, port=None, resource_connection_string=None, resource_type=None, type=None):
        if biztalk_uri and not isinstance(biztalk_uri, str):
            raise TypeError("Expected argument 'biztalk_uri' to be a str")
        pulumi.set(__self__, "biztalk_uri", biztalk_uri)
        if entity_connection_string and not isinstance(entity_connection_string, str):
            raise TypeError("Expected argument 'entity_connection_string' to be a str")
        pulumi.set(__self__, "entity_connection_string", entity_connection_string)
        if entity_name and not isinstance(entity_name, str):
            raise TypeError("Expected argument 'entity_name' to be a str")
        pulumi.set(__self__, "entity_name", entity_name)
        if hostname and not isinstance(hostname, str):
            raise TypeError("Expected argument 'hostname' to be a str")
        pulumi.set(__self__, "hostname", hostname)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if port and not isinstance(port, int):
            raise TypeError("Expected argument 'port' to be a int")
        pulumi.set(__self__, "port", port)
        if resource_connection_string and not isinstance(resource_connection_string, str):
            raise TypeError("Expected argument 'resource_connection_string' to be a str")
        pulumi.set(__self__, "resource_connection_string", resource_connection_string)
        if resource_type and not isinstance(resource_type, str):
            raise TypeError("Expected argument 'resource_type' to be a str")
        pulumi.set(__self__, "resource_type", resource_type)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="biztalkUri")
    def biztalk_uri(self) -> Optional[str]:
        return pulumi.get(self, "biztalk_uri")

    @property
    @pulumi.getter(name="entityConnectionString")
    def entity_connection_string(self) -> Optional[str]:
        return pulumi.get(self, "entity_connection_string")

    @property
    @pulumi.getter(name="entityName")
    def entity_name(self) -> Optional[str]:
        return pulumi.get(self, "entity_name")

    @property
    @pulumi.getter
    def hostname(self) -> Optional[str]:
        return pulumi.get(self, "hostname")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="resourceConnectionString")
    def resource_connection_string(self) -> Optional[str]:
        return pulumi.get(self, "resource_connection_string")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[str]:
        return pulumi.get(self, "resource_type")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetWebAppRelayServiceConnectionSlotResult(GetWebAppRelayServiceConnectionSlotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWebAppRelayServiceConnectionSlotResult(
            biztalk_uri=self.biztalk_uri,
            entity_connection_string=self.entity_connection_string,
            entity_name=self.entity_name,
            hostname=self.hostname,
            id=self.id,
            kind=self.kind,
            name=self.name,
            port=self.port,
            resource_connection_string=self.resource_connection_string,
            resource_type=self.resource_type,
            type=self.type)


def get_web_app_relay_service_connection_slot(entity_name: Optional[str] = None,
                                              name: Optional[str] = None,
                                              resource_group_name: Optional[str] = None,
                                              slot: Optional[str] = None,
                                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWebAppRelayServiceConnectionSlotResult:
    """
    Hybrid Connection for an App Service app.
    API Version: 2020-12-01.


    :param str entity_name: Name of the hybrid connection.
    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. If a slot is not specified, the API will get a hybrid connection for the production slot.
    """
    __args__ = dict()
    __args__['entityName'] = entity_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['slot'] = slot
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:web:getWebAppRelayServiceConnectionSlot', __args__, opts=opts, typ=GetWebAppRelayServiceConnectionSlotResult).value

    return AwaitableGetWebAppRelayServiceConnectionSlotResult(
        biztalk_uri=__ret__.biztalk_uri,
        entity_connection_string=__ret__.entity_connection_string,
        entity_name=__ret__.entity_name,
        hostname=__ret__.hostname,
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        port=__ret__.port,
        resource_connection_string=__ret__.resource_connection_string,
        resource_type=__ret__.resource_type,
        type=__ret__.type)


@_utilities.lift_output_func(get_web_app_relay_service_connection_slot)
def get_web_app_relay_service_connection_slot_output(entity_name: Optional[pulumi.Input[str]] = None,
                                                     name: Optional[pulumi.Input[str]] = None,
                                                     resource_group_name: Optional[pulumi.Input[str]] = None,
                                                     slot: Optional[pulumi.Input[str]] = None,
                                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWebAppRelayServiceConnectionSlotResult]:
    """
    Hybrid Connection for an App Service app.
    API Version: 2020-12-01.


    :param str entity_name: Name of the hybrid connection.
    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. If a slot is not specified, the API will get a hybrid connection for the production slot.
    """
    ...
