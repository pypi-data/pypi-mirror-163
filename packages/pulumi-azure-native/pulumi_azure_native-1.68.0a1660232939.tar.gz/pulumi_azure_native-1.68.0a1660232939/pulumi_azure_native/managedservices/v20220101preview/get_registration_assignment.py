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
    'GetRegistrationAssignmentResult',
    'AwaitableGetRegistrationAssignmentResult',
    'get_registration_assignment',
    'get_registration_assignment_output',
]

@pulumi.output_type
class GetRegistrationAssignmentResult:
    """
    The registration assignment.
    """
    def __init__(__self__, id=None, name=None, properties=None, system_data=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The fully qualified path of the registration assignment.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the registration assignment.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.RegistrationAssignmentPropertiesResponse':
        """
        The properties of a registration assignment.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The metadata for the registration assignment resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the Azure resource (Microsoft.ManagedServices/registrationAssignments).
        """
        return pulumi.get(self, "type")


class AwaitableGetRegistrationAssignmentResult(GetRegistrationAssignmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRegistrationAssignmentResult(
            id=self.id,
            name=self.name,
            properties=self.properties,
            system_data=self.system_data,
            type=self.type)


def get_registration_assignment(expand_registration_definition: Optional[bool] = None,
                                registration_assignment_id: Optional[str] = None,
                                scope: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRegistrationAssignmentResult:
    """
    The registration assignment.


    :param bool expand_registration_definition: The flag indicating whether to return the registration definition details along with the registration assignment details.
    :param str registration_assignment_id: The GUID of the registration assignment.
    :param str scope: The scope of the resource.
    """
    __args__ = dict()
    __args__['expandRegistrationDefinition'] = expand_registration_definition
    __args__['registrationAssignmentId'] = registration_assignment_id
    __args__['scope'] = scope
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:managedservices/v20220101preview:getRegistrationAssignment', __args__, opts=opts, typ=GetRegistrationAssignmentResult).value

    return AwaitableGetRegistrationAssignmentResult(
        id=__ret__.id,
        name=__ret__.name,
        properties=__ret__.properties,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_registration_assignment)
def get_registration_assignment_output(expand_registration_definition: Optional[pulumi.Input[Optional[bool]]] = None,
                                       registration_assignment_id: Optional[pulumi.Input[str]] = None,
                                       scope: Optional[pulumi.Input[str]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRegistrationAssignmentResult]:
    """
    The registration assignment.


    :param bool expand_registration_definition: The flag indicating whether to return the registration definition details along with the registration assignment details.
    :param str registration_assignment_id: The GUID of the registration assignment.
    :param str scope: The scope of the resource.
    """
    ...
