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
    'GetApplicationResult',
    'AwaitableGetApplicationResult',
    'get_application',
    'get_application_output',
]

warnings.warn("""Version 2018-07-01-preview will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetApplicationResult:
    """
    This type describes an application resource.
    """
    def __init__(__self__, debug_params=None, description=None, diagnostics=None, health_state=None, id=None, location=None, name=None, provisioning_state=None, service_names=None, services=None, status=None, status_details=None, tags=None, type=None, unhealthy_evaluation=None):
        if debug_params and not isinstance(debug_params, str):
            raise TypeError("Expected argument 'debug_params' to be a str")
        pulumi.set(__self__, "debug_params", debug_params)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if diagnostics and not isinstance(diagnostics, dict):
            raise TypeError("Expected argument 'diagnostics' to be a dict")
        pulumi.set(__self__, "diagnostics", diagnostics)
        if health_state and not isinstance(health_state, str):
            raise TypeError("Expected argument 'health_state' to be a str")
        pulumi.set(__self__, "health_state", health_state)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if service_names and not isinstance(service_names, list):
            raise TypeError("Expected argument 'service_names' to be a list")
        pulumi.set(__self__, "service_names", service_names)
        if services and not isinstance(services, list):
            raise TypeError("Expected argument 'services' to be a list")
        pulumi.set(__self__, "services", services)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if status_details and not isinstance(status_details, str):
            raise TypeError("Expected argument 'status_details' to be a str")
        pulumi.set(__self__, "status_details", status_details)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if unhealthy_evaluation and not isinstance(unhealthy_evaluation, str):
            raise TypeError("Expected argument 'unhealthy_evaluation' to be a str")
        pulumi.set(__self__, "unhealthy_evaluation", unhealthy_evaluation)

    @property
    @pulumi.getter(name="debugParams")
    def debug_params(self) -> Optional[str]:
        """
        Internal use.
        """
        return pulumi.get(self, "debug_params")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        User readable description of the application.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def diagnostics(self) -> Optional['outputs.DiagnosticsDescriptionResponse']:
        """
        Describes the diagnostics definition and usage for an application resource.
        """
        return pulumi.get(self, "diagnostics")

    @property
    @pulumi.getter(name="healthState")
    def health_state(self) -> str:
        """
        Describes the health state of an application resource.
        """
        return pulumi.get(self, "health_state")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified identifier for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        State of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="serviceNames")
    def service_names(self) -> Sequence[str]:
        """
        Names of the services in the application.
        """
        return pulumi.get(self, "service_names")

    @property
    @pulumi.getter
    def services(self) -> Optional[Sequence['outputs.ServiceResourceDescriptionResponse']]:
        """
        describes the services in the application.
        """
        return pulumi.get(self, "services")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the application resource.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="statusDetails")
    def status_details(self) -> str:
        """
        Gives additional information about the current status of the application deployment.
        """
        return pulumi.get(self, "status_details")

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
        The type of the resource. Ex- Microsoft.Compute/virtualMachines or Microsoft.Storage/storageAccounts.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="unhealthyEvaluation")
    def unhealthy_evaluation(self) -> str:
        """
        When the application's health state is not 'Ok', this additional details from service fabric Health Manager for the user to know why the application is marked unhealthy.
        """
        return pulumi.get(self, "unhealthy_evaluation")


class AwaitableGetApplicationResult(GetApplicationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplicationResult(
            debug_params=self.debug_params,
            description=self.description,
            diagnostics=self.diagnostics,
            health_state=self.health_state,
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            service_names=self.service_names,
            services=self.services,
            status=self.status,
            status_details=self.status_details,
            tags=self.tags,
            type=self.type,
            unhealthy_evaluation=self.unhealthy_evaluation)


def get_application(application_name: Optional[str] = None,
                    resource_group_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApplicationResult:
    """
    This type describes an application resource.


    :param str application_name: The identity of the application.
    :param str resource_group_name: Azure resource group name
    """
    pulumi.log.warn("""get_application is deprecated: Version 2018-07-01-preview will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['applicationName'] = application_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:servicefabricmesh/v20180701preview:getApplication', __args__, opts=opts, typ=GetApplicationResult).value

    return AwaitableGetApplicationResult(
        debug_params=__ret__.debug_params,
        description=__ret__.description,
        diagnostics=__ret__.diagnostics,
        health_state=__ret__.health_state,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        service_names=__ret__.service_names,
        services=__ret__.services,
        status=__ret__.status,
        status_details=__ret__.status_details,
        tags=__ret__.tags,
        type=__ret__.type,
        unhealthy_evaluation=__ret__.unhealthy_evaluation)


@_utilities.lift_output_func(get_application)
def get_application_output(application_name: Optional[pulumi.Input[str]] = None,
                           resource_group_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetApplicationResult]:
    """
    This type describes an application resource.


    :param str application_name: The identity of the application.
    :param str resource_group_name: Azure resource group name
    """
    pulumi.log.warn("""get_application is deprecated: Version 2018-07-01-preview will be removed in v2 of the provider.""")
    ...
