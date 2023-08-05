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
    'GetGuestConfigurationAssignmentResult',
    'AwaitableGetGuestConfigurationAssignmentResult',
    'get_guest_configuration_assignment',
    'get_guest_configuration_assignment_output',
]

@pulumi.output_type
class GetGuestConfigurationAssignmentResult:
    """
    Guest configuration assignment is an association between a machine and guest configuration.
    """
    def __init__(__self__, id=None, location=None, name=None, properties=None, system_data=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
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
        ARM resource id of the guest configuration assignment.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Region where the VM is located.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the guest configuration assignment.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.GuestConfigurationAssignmentPropertiesResponse':
        """
        Properties of the Guest configuration assignment.
        """
        return pulumi.get(self, "properties")

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
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetGuestConfigurationAssignmentResult(GetGuestConfigurationAssignmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGuestConfigurationAssignmentResult(
            id=self.id,
            location=self.location,
            name=self.name,
            properties=self.properties,
            system_data=self.system_data,
            type=self.type)


def get_guest_configuration_assignment(guest_configuration_assignment_name: Optional[str] = None,
                                       resource_group_name: Optional[str] = None,
                                       vm_name: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGuestConfigurationAssignmentResult:
    """
    Guest configuration assignment is an association between a machine and guest configuration.


    :param str guest_configuration_assignment_name: The guest configuration assignment name.
    :param str resource_group_name: The resource group name.
    :param str vm_name: The name of the virtual machine.
    """
    __args__ = dict()
    __args__['guestConfigurationAssignmentName'] = guest_configuration_assignment_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['vmName'] = vm_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:guestconfiguration/v20210125:getGuestConfigurationAssignment', __args__, opts=opts, typ=GetGuestConfigurationAssignmentResult).value

    return AwaitableGetGuestConfigurationAssignmentResult(
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        properties=__ret__.properties,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_guest_configuration_assignment)
def get_guest_configuration_assignment_output(guest_configuration_assignment_name: Optional[pulumi.Input[str]] = None,
                                              resource_group_name: Optional[pulumi.Input[str]] = None,
                                              vm_name: Optional[pulumi.Input[str]] = None,
                                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGuestConfigurationAssignmentResult]:
    """
    Guest configuration assignment is an association between a machine and guest configuration.


    :param str guest_configuration_assignment_name: The guest configuration assignment name.
    :param str resource_group_name: The resource group name.
    :param str vm_name: The name of the virtual machine.
    """
    ...
