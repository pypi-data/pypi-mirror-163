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
    'GetConnectorResult',
    'AwaitableGetConnectorResult',
    'get_connector',
    'get_connector_output',
]

@pulumi.output_type
class GetConnectorResult:
    """
    The Connector model definition
    """
    def __init__(__self__, collection=None, created_on=None, credentials_key=None, display_name=None, id=None, kind=None, location=None, modified_on=None, name=None, provider_account_id=None, report_id=None, status=None, tags=None, type=None):
        if collection and not isinstance(collection, dict):
            raise TypeError("Expected argument 'collection' to be a dict")
        pulumi.set(__self__, "collection", collection)
        if created_on and not isinstance(created_on, str):
            raise TypeError("Expected argument 'created_on' to be a str")
        pulumi.set(__self__, "created_on", created_on)
        if credentials_key and not isinstance(credentials_key, str):
            raise TypeError("Expected argument 'credentials_key' to be a str")
        pulumi.set(__self__, "credentials_key", credentials_key)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if modified_on and not isinstance(modified_on, str):
            raise TypeError("Expected argument 'modified_on' to be a str")
        pulumi.set(__self__, "modified_on", modified_on)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provider_account_id and not isinstance(provider_account_id, str):
            raise TypeError("Expected argument 'provider_account_id' to be a str")
        pulumi.set(__self__, "provider_account_id", provider_account_id)
        if report_id and not isinstance(report_id, str):
            raise TypeError("Expected argument 'report_id' to be a str")
        pulumi.set(__self__, "report_id", report_id)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def collection(self) -> 'outputs.ConnectorCollectionInfoResponse':
        """
        Collection information
        """
        return pulumi.get(self, "collection")

    @property
    @pulumi.getter(name="createdOn")
    def created_on(self) -> str:
        """
        Connector definition creation datetime
        """
        return pulumi.get(self, "created_on")

    @property
    @pulumi.getter(name="credentialsKey")
    def credentials_key(self) -> Optional[str]:
        """
        Credentials authentication key (eg AWS ARN)
        """
        return pulumi.get(self, "credentials_key")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        Connector DisplayName (defaults to Name)
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Connector id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Connector kind (eg aws)
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Connector location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="modifiedOn")
    def modified_on(self) -> str:
        """
        Connector last modified datetime
        """
        return pulumi.get(self, "modified_on")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Connector name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="providerAccountId")
    def provider_account_id(self) -> str:
        """
        Connector providerAccountId (determined from credentials)
        """
        return pulumi.get(self, "provider_account_id")

    @property
    @pulumi.getter(name="reportId")
    def report_id(self) -> Optional[str]:
        """
        Identifying source report. (For AWS this is a CUR report name, defined with Daily and with Resources)
        """
        return pulumi.get(self, "report_id")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Connector status
        """
        return pulumi.get(self, "status")

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
        Connector type
        """
        return pulumi.get(self, "type")


class AwaitableGetConnectorResult(GetConnectorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConnectorResult(
            collection=self.collection,
            created_on=self.created_on,
            credentials_key=self.credentials_key,
            display_name=self.display_name,
            id=self.id,
            kind=self.kind,
            location=self.location,
            modified_on=self.modified_on,
            name=self.name,
            provider_account_id=self.provider_account_id,
            report_id=self.report_id,
            status=self.status,
            tags=self.tags,
            type=self.type)


def get_connector(connector_name: Optional[str] = None,
                  resource_group_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConnectorResult:
    """
    The Connector model definition


    :param str connector_name: Connector Name.
    :param str resource_group_name: Azure Resource Group Name.
    """
    __args__ = dict()
    __args__['connectorName'] = connector_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:costmanagement/v20180801preview:getConnector', __args__, opts=opts, typ=GetConnectorResult).value

    return AwaitableGetConnectorResult(
        collection=__ret__.collection,
        created_on=__ret__.created_on,
        credentials_key=__ret__.credentials_key,
        display_name=__ret__.display_name,
        id=__ret__.id,
        kind=__ret__.kind,
        location=__ret__.location,
        modified_on=__ret__.modified_on,
        name=__ret__.name,
        provider_account_id=__ret__.provider_account_id,
        report_id=__ret__.report_id,
        status=__ret__.status,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_connector)
def get_connector_output(connector_name: Optional[pulumi.Input[str]] = None,
                         resource_group_name: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetConnectorResult]:
    """
    The Connector model definition


    :param str connector_name: Connector Name.
    :param str resource_group_name: Azure Resource Group Name.
    """
    ...
