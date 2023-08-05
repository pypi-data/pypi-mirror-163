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
    'GetComponentContainerResult',
    'AwaitableGetComponentContainerResult',
    'get_component_container',
    'get_component_container_output',
]

@pulumi.output_type
class GetComponentContainerResult:
    """
    Azure Resource Manager resource envelope.
    """
    def __init__(__self__, component_container_details=None, id=None, name=None, system_data=None, type=None):
        if component_container_details and not isinstance(component_container_details, dict):
            raise TypeError("Expected argument 'component_container_details' to be a dict")
        pulumi.set(__self__, "component_container_details", component_container_details)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
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
    @pulumi.getter(name="componentContainerDetails")
    def component_container_details(self) -> 'outputs.ComponentContainerResponse':
        """
        [Required] Additional attributes of the entity.
        """
        return pulumi.get(self, "component_container_details")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

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


class AwaitableGetComponentContainerResult(GetComponentContainerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetComponentContainerResult(
            component_container_details=self.component_container_details,
            id=self.id,
            name=self.name,
            system_data=self.system_data,
            type=self.type)


def get_component_container(name: Optional[str] = None,
                            resource_group_name: Optional[str] = None,
                            workspace_name: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetComponentContainerResult:
    """
    Azure Resource Manager resource envelope.
    API Version: 2022-02-01-preview.


    :param str name: Container name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: Name of Azure Machine Learning workspace.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:machinelearningservices:getComponentContainer', __args__, opts=opts, typ=GetComponentContainerResult).value

    return AwaitableGetComponentContainerResult(
        component_container_details=__ret__.component_container_details,
        id=__ret__.id,
        name=__ret__.name,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_component_container)
def get_component_container_output(name: Optional[pulumi.Input[str]] = None,
                                   resource_group_name: Optional[pulumi.Input[str]] = None,
                                   workspace_name: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetComponentContainerResult]:
    """
    Azure Resource Manager resource envelope.
    API Version: 2022-02-01-preview.


    :param str name: Container name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: Name of Azure Machine Learning workspace.
    """
    ...
