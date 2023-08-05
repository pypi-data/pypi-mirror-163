# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetSiteRelayServiceConnectionResult',
    'AwaitableGetSiteRelayServiceConnectionResult',
    'get_site_relay_service_connection',
    'get_site_relay_service_connection_output',
]

warnings.warn("""Version 2015-08-01 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetSiteRelayServiceConnectionResult:
    """
    Class that represents a BizTalk Hybrid Connection
    """
    def __init__(__self__, biztalk_uri=None, entity_connection_string=None, entity_name=None, hostname=None, id=None, kind=None, location=None, name=None, port=None, resource_connection_string=None, resource_type=None, tags=None, type=None):
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
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
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
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
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
    def id(self) -> Optional[str]:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Resource Name
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
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetSiteRelayServiceConnectionResult(GetSiteRelayServiceConnectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSiteRelayServiceConnectionResult(
            biztalk_uri=self.biztalk_uri,
            entity_connection_string=self.entity_connection_string,
            entity_name=self.entity_name,
            hostname=self.hostname,
            id=self.id,
            kind=self.kind,
            location=self.location,
            name=self.name,
            port=self.port,
            resource_connection_string=self.resource_connection_string,
            resource_type=self.resource_type,
            tags=self.tags,
            type=self.type)


def get_site_relay_service_connection(entity_name: Optional[str] = None,
                                      name: Optional[str] = None,
                                      resource_group_name: Optional[str] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSiteRelayServiceConnectionResult:
    """
    Class that represents a BizTalk Hybrid Connection


    :param str entity_name: The name by which the Hybrid Connection is identified
    :param str name: The name of the web app
    :param str resource_group_name: The resource group name
    """
    pulumi.log.warn("""get_site_relay_service_connection is deprecated: Version 2015-08-01 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['entityName'] = entity_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20150801:getSiteRelayServiceConnection', __args__, opts=opts, typ=GetSiteRelayServiceConnectionResult).value

    return AwaitableGetSiteRelayServiceConnectionResult(
        biztalk_uri=__ret__.biztalk_uri,
        entity_connection_string=__ret__.entity_connection_string,
        entity_name=__ret__.entity_name,
        hostname=__ret__.hostname,
        id=__ret__.id,
        kind=__ret__.kind,
        location=__ret__.location,
        name=__ret__.name,
        port=__ret__.port,
        resource_connection_string=__ret__.resource_connection_string,
        resource_type=__ret__.resource_type,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_site_relay_service_connection)
def get_site_relay_service_connection_output(entity_name: Optional[pulumi.Input[str]] = None,
                                             name: Optional[pulumi.Input[str]] = None,
                                             resource_group_name: Optional[pulumi.Input[str]] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSiteRelayServiceConnectionResult]:
    """
    Class that represents a BizTalk Hybrid Connection


    :param str entity_name: The name by which the Hybrid Connection is identified
    :param str name: The name of the web app
    :param str resource_group_name: The resource group name
    """
    pulumi.log.warn("""get_site_relay_service_connection is deprecated: Version 2015-08-01 will be removed in v2 of the provider.""")
    ...
