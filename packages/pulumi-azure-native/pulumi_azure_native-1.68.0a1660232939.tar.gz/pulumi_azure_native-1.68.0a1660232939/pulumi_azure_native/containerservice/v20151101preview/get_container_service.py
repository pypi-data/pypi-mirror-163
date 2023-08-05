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
    'GetContainerServiceResult',
    'AwaitableGetContainerServiceResult',
    'get_container_service',
    'get_container_service_output',
]

warnings.warn("""Version 2015-11-01-preview will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetContainerServiceResult:
    """
    Container service
    """
    def __init__(__self__, agent_pool_profiles=None, diagnostics_profile=None, id=None, linux_profile=None, location=None, master_profile=None, name=None, orchestrator_profile=None, provisioning_state=None, tags=None, type=None, windows_profile=None):
        if agent_pool_profiles and not isinstance(agent_pool_profiles, list):
            raise TypeError("Expected argument 'agent_pool_profiles' to be a list")
        pulumi.set(__self__, "agent_pool_profiles", agent_pool_profiles)
        if diagnostics_profile and not isinstance(diagnostics_profile, dict):
            raise TypeError("Expected argument 'diagnostics_profile' to be a dict")
        pulumi.set(__self__, "diagnostics_profile", diagnostics_profile)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if linux_profile and not isinstance(linux_profile, dict):
            raise TypeError("Expected argument 'linux_profile' to be a dict")
        pulumi.set(__self__, "linux_profile", linux_profile)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if master_profile and not isinstance(master_profile, dict):
            raise TypeError("Expected argument 'master_profile' to be a dict")
        pulumi.set(__self__, "master_profile", master_profile)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if orchestrator_profile and not isinstance(orchestrator_profile, dict):
            raise TypeError("Expected argument 'orchestrator_profile' to be a dict")
        pulumi.set(__self__, "orchestrator_profile", orchestrator_profile)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if windows_profile and not isinstance(windows_profile, dict):
            raise TypeError("Expected argument 'windows_profile' to be a dict")
        pulumi.set(__self__, "windows_profile", windows_profile)

    @property
    @pulumi.getter(name="agentPoolProfiles")
    def agent_pool_profiles(self) -> Sequence['outputs.ContainerServiceAgentPoolProfileResponse']:
        """
        Properties of agent pools
        """
        return pulumi.get(self, "agent_pool_profiles")

    @property
    @pulumi.getter(name="diagnosticsProfile")
    def diagnostics_profile(self) -> Optional['outputs.ContainerServiceDiagnosticsProfileResponse']:
        """
        Properties for Diagnostic Agent
        """
        return pulumi.get(self, "diagnostics_profile")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="linuxProfile")
    def linux_profile(self) -> 'outputs.ContainerServiceLinuxProfileResponse':
        """
        Properties for Linux VMs
        """
        return pulumi.get(self, "linux_profile")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="masterProfile")
    def master_profile(self) -> 'outputs.ContainerServiceMasterProfileResponse':
        """
        Properties of master agents
        """
        return pulumi.get(self, "master_profile")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orchestratorProfile")
    def orchestrator_profile(self) -> Optional['outputs.ContainerServiceOrchestratorProfileResponse']:
        """
        Properties of orchestrator
        """
        return pulumi.get(self, "orchestrator_profile")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Gets the provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="windowsProfile")
    def windows_profile(self) -> Optional['outputs.ContainerServiceWindowsProfileResponse']:
        """
        Properties of Windows VMs
        """
        return pulumi.get(self, "windows_profile")


class AwaitableGetContainerServiceResult(GetContainerServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetContainerServiceResult(
            agent_pool_profiles=self.agent_pool_profiles,
            diagnostics_profile=self.diagnostics_profile,
            id=self.id,
            linux_profile=self.linux_profile,
            location=self.location,
            master_profile=self.master_profile,
            name=self.name,
            orchestrator_profile=self.orchestrator_profile,
            provisioning_state=self.provisioning_state,
            tags=self.tags,
            type=self.type,
            windows_profile=self.windows_profile)


def get_container_service(container_service_name: Optional[str] = None,
                          resource_group_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetContainerServiceResult:
    """
    Container service


    :param str container_service_name: The name of the container service within the given subscription and resource group.
    :param str resource_group_name: The name of the resource group.
    """
    pulumi.log.warn("""get_container_service is deprecated: Version 2015-11-01-preview will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['containerServiceName'] = container_service_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:containerservice/v20151101preview:getContainerService', __args__, opts=opts, typ=GetContainerServiceResult).value

    return AwaitableGetContainerServiceResult(
        agent_pool_profiles=__ret__.agent_pool_profiles,
        diagnostics_profile=__ret__.diagnostics_profile,
        id=__ret__.id,
        linux_profile=__ret__.linux_profile,
        location=__ret__.location,
        master_profile=__ret__.master_profile,
        name=__ret__.name,
        orchestrator_profile=__ret__.orchestrator_profile,
        provisioning_state=__ret__.provisioning_state,
        tags=__ret__.tags,
        type=__ret__.type,
        windows_profile=__ret__.windows_profile)


@_utilities.lift_output_func(get_container_service)
def get_container_service_output(container_service_name: Optional[pulumi.Input[str]] = None,
                                 resource_group_name: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetContainerServiceResult]:
    """
    Container service


    :param str container_service_name: The name of the container service within the given subscription and resource group.
    :param str resource_group_name: The name of the resource group.
    """
    pulumi.log.warn("""get_container_service is deprecated: Version 2015-11-01-preview will be removed in v2 of the provider.""")
    ...
