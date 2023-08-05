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
    'GetManagementGroupResult',
    'AwaitableGetManagementGroupResult',
    'get_management_group',
    'get_management_group_output',
]

warnings.warn("""Version 2018-03-01-preview will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetManagementGroupResult:
    """
    The management group details.
    """
    def __init__(__self__, children=None, details=None, display_name=None, id=None, name=None, roles=None, tenant_id=None, type=None):
        if children and not isinstance(children, list):
            raise TypeError("Expected argument 'children' to be a list")
        pulumi.set(__self__, "children", children)
        if details and not isinstance(details, dict):
            raise TypeError("Expected argument 'details' to be a dict")
        pulumi.set(__self__, "details", details)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if roles and not isinstance(roles, list):
            raise TypeError("Expected argument 'roles' to be a list")
        pulumi.set(__self__, "roles", roles)
        if tenant_id and not isinstance(tenant_id, str):
            raise TypeError("Expected argument 'tenant_id' to be a str")
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def children(self) -> Optional[Sequence['outputs.ManagementGroupChildInfoResponse']]:
        """
        The list of children.
        """
        return pulumi.get(self, "children")

    @property
    @pulumi.getter
    def details(self) -> Optional['outputs.ManagementGroupDetailsResponse']:
        """
        The details of a management group.
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The friendly name of the management group.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The fully qualified ID for the management group.  For example, /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the management group. For example, 00000000-0000-0000-0000-000000000000
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def roles(self) -> Optional[Sequence[str]]:
        """
        The role definitions associated with the management group.
        """
        return pulumi.get(self, "roles")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[str]:
        """
        The AAD Tenant ID associated with the management group. For example, 00000000-0000-0000-0000-000000000000
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.  For example, /providers/Microsoft.Management/managementGroups
        """
        return pulumi.get(self, "type")


class AwaitableGetManagementGroupResult(GetManagementGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagementGroupResult(
            children=self.children,
            details=self.details,
            display_name=self.display_name,
            id=self.id,
            name=self.name,
            roles=self.roles,
            tenant_id=self.tenant_id,
            type=self.type)


def get_management_group(expand: Optional[str] = None,
                         filter: Optional[str] = None,
                         group_id: Optional[str] = None,
                         recurse: Optional[bool] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetManagementGroupResult:
    """
    The management group details.


    :param str expand: The $expand=children query string parameter allows clients to request inclusion of children in the response payload.
    :param str filter: A filter which allows the exclusion of subscriptions from results (i.e. '$filter=children.childType ne Subscription')
    :param str group_id: Management Group ID.
    :param bool recurse: The $recurse=true query string parameter allows clients to request inclusion of entire hierarchy in the response payload. Note that  $expand=children must be passed up if $recurse is set to true.
    """
    pulumi.log.warn("""get_management_group is deprecated: Version 2018-03-01-preview will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['expand'] = expand
    __args__['filter'] = filter
    __args__['groupId'] = group_id
    __args__['recurse'] = recurse
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:management/v20180301preview:getManagementGroup', __args__, opts=opts, typ=GetManagementGroupResult).value

    return AwaitableGetManagementGroupResult(
        children=__ret__.children,
        details=__ret__.details,
        display_name=__ret__.display_name,
        id=__ret__.id,
        name=__ret__.name,
        roles=__ret__.roles,
        tenant_id=__ret__.tenant_id,
        type=__ret__.type)


@_utilities.lift_output_func(get_management_group)
def get_management_group_output(expand: Optional[pulumi.Input[Optional[str]]] = None,
                                filter: Optional[pulumi.Input[Optional[str]]] = None,
                                group_id: Optional[pulumi.Input[str]] = None,
                                recurse: Optional[pulumi.Input[Optional[bool]]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetManagementGroupResult]:
    """
    The management group details.


    :param str expand: The $expand=children query string parameter allows clients to request inclusion of children in the response payload.
    :param str filter: A filter which allows the exclusion of subscriptions from results (i.e. '$filter=children.childType ne Subscription')
    :param str group_id: Management Group ID.
    :param bool recurse: The $recurse=true query string parameter allows clients to request inclusion of entire hierarchy in the response payload. Note that  $expand=children must be passed up if $recurse is set to true.
    """
    pulumi.log.warn("""get_management_group is deprecated: Version 2018-03-01-preview will be removed in v2 of the provider.""")
    ...
