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
    'GetEntityQueryResult',
    'AwaitableGetEntityQueryResult',
    'get_entity_query',
    'get_entity_query_output',
]

warnings.warn("""Please use one of the variants: ActivityCustomEntityQuery.""", DeprecationWarning)

@pulumi.output_type
class GetEntityQueryResult:
    """
    Specific entity query.
    """
    def __init__(__self__, etag=None, id=None, kind=None, name=None, system_data=None, type=None):
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        the entity query kind
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetEntityQueryResult(GetEntityQueryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEntityQueryResult(
            etag=self.etag,
            id=self.id,
            kind=self.kind,
            name=self.name,
            system_data=self.system_data,
            type=self.type)


def get_entity_query(entity_query_id: Optional[str] = None,
                     resource_group_name: Optional[str] = None,
                     workspace_name: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEntityQueryResult:
    """
    Specific entity query.


    :param str entity_query_id: entity query ID
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    pulumi.log.warn("""get_entity_query is deprecated: Please use one of the variants: ActivityCustomEntityQuery.""")
    __args__ = dict()
    __args__['entityQueryId'] = entity_query_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:securityinsights/v20220601preview:getEntityQuery', __args__, opts=opts, typ=GetEntityQueryResult).value

    return AwaitableGetEntityQueryResult(
        etag=__ret__.etag,
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_entity_query)
def get_entity_query_output(entity_query_id: Optional[pulumi.Input[str]] = None,
                            resource_group_name: Optional[pulumi.Input[str]] = None,
                            workspace_name: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEntityQueryResult]:
    """
    Specific entity query.


    :param str entity_query_id: entity query ID
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    pulumi.log.warn("""get_entity_query is deprecated: Please use one of the variants: ActivityCustomEntityQuery.""")
    ...
