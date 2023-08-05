# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetSqlResourceSqlRoleDefinitionResult',
    'AwaitableGetSqlResourceSqlRoleDefinitionResult',
    'get_sql_resource_sql_role_definition',
    'get_sql_resource_sql_role_definition_output',
]

@pulumi.output_type
class GetSqlResourceSqlRoleDefinitionResult:
    """
    An Azure Cosmos DB SQL Role Definition.
    """
    def __init__(__self__, assignable_scopes=None, id=None, name=None, permissions=None, role_name=None, type=None):
        if assignable_scopes and not isinstance(assignable_scopes, list):
            raise TypeError("Expected argument 'assignable_scopes' to be a list")
        pulumi.set(__self__, "assignable_scopes", assignable_scopes)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if permissions and not isinstance(permissions, list):
            raise TypeError("Expected argument 'permissions' to be a list")
        pulumi.set(__self__, "permissions", permissions)
        if role_name and not isinstance(role_name, str):
            raise TypeError("Expected argument 'role_name' to be a str")
        pulumi.set(__self__, "role_name", role_name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="assignableScopes")
    def assignable_scopes(self) -> Optional[Sequence[str]]:
        """
        A set of fully qualified Scopes at or below which Role Assignments may be created using this Role Definition. This will allow application of this Role Definition on the entire database account or any underlying Database / Collection. Must have at least one element. Scopes higher than Database account are not enforceable as assignable Scopes. Note that resources referenced in assignable Scopes need not exist.
        """
        return pulumi.get(self, "assignable_scopes")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The unique resource identifier of the database account.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the database account.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def permissions(self) -> Optional[Sequence['outputs.PermissionResponse']]:
        """
        The set of operations allowed through this Role Definition.
        """
        return pulumi.get(self, "permissions")

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> Optional[str]:
        """
        A user-friendly name for the Role Definition. Must be unique for the database account.
        """
        return pulumi.get(self, "role_name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of Azure resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetSqlResourceSqlRoleDefinitionResult(GetSqlResourceSqlRoleDefinitionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSqlResourceSqlRoleDefinitionResult(
            assignable_scopes=self.assignable_scopes,
            id=self.id,
            name=self.name,
            permissions=self.permissions,
            role_name=self.role_name,
            type=self.type)


def get_sql_resource_sql_role_definition(account_name: Optional[str] = None,
                                         resource_group_name: Optional[str] = None,
                                         role_definition_id: Optional[str] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSqlResourceSqlRoleDefinitionResult:
    """
    An Azure Cosmos DB SQL Role Definition.
    API Version: 2021-03-01-preview.


    :param str account_name: Cosmos DB database account name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str role_definition_id: The GUID for the Role Definition.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['roleDefinitionId'] = role_definition_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:documentdb:getSqlResourceSqlRoleDefinition', __args__, opts=opts, typ=GetSqlResourceSqlRoleDefinitionResult).value

    return AwaitableGetSqlResourceSqlRoleDefinitionResult(
        assignable_scopes=__ret__.assignable_scopes,
        id=__ret__.id,
        name=__ret__.name,
        permissions=__ret__.permissions,
        role_name=__ret__.role_name,
        type=__ret__.type)


@_utilities.lift_output_func(get_sql_resource_sql_role_definition)
def get_sql_resource_sql_role_definition_output(account_name: Optional[pulumi.Input[str]] = None,
                                                resource_group_name: Optional[pulumi.Input[str]] = None,
                                                role_definition_id: Optional[pulumi.Input[str]] = None,
                                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSqlResourceSqlRoleDefinitionResult]:
    """
    An Azure Cosmos DB SQL Role Definition.
    API Version: 2021-03-01-preview.


    :param str account_name: Cosmos DB database account name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str role_definition_id: The GUID for the Role Definition.
    """
    ...
