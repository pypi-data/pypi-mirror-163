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
    'ListNetworkManagerEffectiveConnectivityConfigurationsResult',
    'AwaitableListNetworkManagerEffectiveConnectivityConfigurationsResult',
    'list_network_manager_effective_connectivity_configurations',
    'list_network_manager_effective_connectivity_configurations_output',
]

@pulumi.output_type
class ListNetworkManagerEffectiveConnectivityConfigurationsResult:
    """
    Result of the request to list networkManagerEffectiveConnectivityConfiguration. It contains a list of groups and a skiptoken to get the next set of results.
    """
    def __init__(__self__, skip_token=None, value=None):
        if skip_token and not isinstance(skip_token, str):
            raise TypeError("Expected argument 'skip_token' to be a str")
        pulumi.set(__self__, "skip_token", skip_token)
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="skipToken")
    def skip_token(self) -> Optional[str]:
        """
        When present, the value can be passed to a subsequent query call (together with the same query and scopes used in the current request) to retrieve the next page of data.
        """
        return pulumi.get(self, "skip_token")

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence['outputs.EffectiveConnectivityConfigurationResponse']]:
        """
        Gets a page of NetworkManagerEffectiveConnectivityConfiguration
        """
        return pulumi.get(self, "value")


class AwaitableListNetworkManagerEffectiveConnectivityConfigurationsResult(ListNetworkManagerEffectiveConnectivityConfigurationsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListNetworkManagerEffectiveConnectivityConfigurationsResult(
            skip_token=self.skip_token,
            value=self.value)


def list_network_manager_effective_connectivity_configurations(resource_group_name: Optional[str] = None,
                                                               skip_token: Optional[str] = None,
                                                               virtual_network_name: Optional[str] = None,
                                                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListNetworkManagerEffectiveConnectivityConfigurationsResult:
    """
    Result of the request to list networkManagerEffectiveConnectivityConfiguration. It contains a list of groups and a skiptoken to get the next set of results.


    :param str resource_group_name: The name of the resource group.
    :param str skip_token: When present, the value can be passed to a subsequent query call (together with the same query and scopes used in the current request) to retrieve the next page of data.
    :param str virtual_network_name: The name of the virtual network.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['skipToken'] = skip_token
    __args__['virtualNetworkName'] = virtual_network_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20220201preview:listNetworkManagerEffectiveConnectivityConfigurations', __args__, opts=opts, typ=ListNetworkManagerEffectiveConnectivityConfigurationsResult).value

    return AwaitableListNetworkManagerEffectiveConnectivityConfigurationsResult(
        skip_token=__ret__.skip_token,
        value=__ret__.value)


@_utilities.lift_output_func(list_network_manager_effective_connectivity_configurations)
def list_network_manager_effective_connectivity_configurations_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                                                      skip_token: Optional[pulumi.Input[Optional[str]]] = None,
                                                                      virtual_network_name: Optional[pulumi.Input[str]] = None,
                                                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListNetworkManagerEffectiveConnectivityConfigurationsResult]:
    """
    Result of the request to list networkManagerEffectiveConnectivityConfiguration. It contains a list of groups and a skiptoken to get the next set of results.


    :param str resource_group_name: The name of the resource group.
    :param str skip_token: When present, the value can be passed to a subsequent query call (together with the same query and scopes used in the current request) to retrieve the next page of data.
    :param str virtual_network_name: The name of the virtual network.
    """
    ...
