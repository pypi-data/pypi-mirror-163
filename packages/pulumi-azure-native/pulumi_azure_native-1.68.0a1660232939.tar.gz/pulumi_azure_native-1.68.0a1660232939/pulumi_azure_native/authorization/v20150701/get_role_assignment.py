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
    'GetRoleAssignmentResult',
    'AwaitableGetRoleAssignmentResult',
    'get_role_assignment',
    'get_role_assignment_output',
]

warnings.warn("""Version 2015-07-01 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetRoleAssignmentResult:
    """
    Role Assignments
    """
    def __init__(__self__, id=None, name=None, properties=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The role assignment ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The role assignment name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.RoleAssignmentPropertiesWithScopeResponse':
        """
        Role assignment properties.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The role assignment type.
        """
        return pulumi.get(self, "type")


class AwaitableGetRoleAssignmentResult(GetRoleAssignmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRoleAssignmentResult(
            id=self.id,
            name=self.name,
            properties=self.properties,
            type=self.type)


def get_role_assignment(role_assignment_name: Optional[str] = None,
                        scope: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRoleAssignmentResult:
    """
    Role Assignments


    :param str role_assignment_name: The name of the role assignment to get.
    :param str scope: The scope of the role assignment.
    """
    pulumi.log.warn("""get_role_assignment is deprecated: Version 2015-07-01 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['roleAssignmentName'] = role_assignment_name
    __args__['scope'] = scope
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:authorization/v20150701:getRoleAssignment', __args__, opts=opts, typ=GetRoleAssignmentResult).value

    return AwaitableGetRoleAssignmentResult(
        id=__ret__.id,
        name=__ret__.name,
        properties=__ret__.properties,
        type=__ret__.type)


@_utilities.lift_output_func(get_role_assignment)
def get_role_assignment_output(role_assignment_name: Optional[pulumi.Input[str]] = None,
                               scope: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRoleAssignmentResult]:
    """
    Role Assignments


    :param str role_assignment_name: The name of the role assignment to get.
    :param str scope: The scope of the role assignment.
    """
    pulumi.log.warn("""get_role_assignment is deprecated: Version 2015-07-01 will be removed in v2 of the provider.""")
    ...
