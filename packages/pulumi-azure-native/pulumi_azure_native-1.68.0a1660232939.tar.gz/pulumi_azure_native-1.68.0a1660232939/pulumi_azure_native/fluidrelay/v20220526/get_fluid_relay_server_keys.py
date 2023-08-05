# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetFluidRelayServerKeysResult',
    'AwaitableGetFluidRelayServerKeysResult',
    'get_fluid_relay_server_keys',
    'get_fluid_relay_server_keys_output',
]

@pulumi.output_type
class GetFluidRelayServerKeysResult:
    """
    The set of available keys for this server.
    """
    def __init__(__self__, key1=None, key2=None):
        if key1 and not isinstance(key1, str):
            raise TypeError("Expected argument 'key1' to be a str")
        pulumi.set(__self__, "key1", key1)
        if key2 and not isinstance(key2, str):
            raise TypeError("Expected argument 'key2' to be a str")
        pulumi.set(__self__, "key2", key2)

    @property
    @pulumi.getter
    def key1(self) -> str:
        """
        The primary key for this server
        """
        return pulumi.get(self, "key1")

    @property
    @pulumi.getter
    def key2(self) -> str:
        """
        The secondary key for this server
        """
        return pulumi.get(self, "key2")


class AwaitableGetFluidRelayServerKeysResult(GetFluidRelayServerKeysResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFluidRelayServerKeysResult(
            key1=self.key1,
            key2=self.key2)


def get_fluid_relay_server_keys(fluid_relay_server_name: Optional[str] = None,
                                resource_group: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFluidRelayServerKeysResult:
    """
    The set of available keys for this server.


    :param str fluid_relay_server_name: The Fluid Relay server resource name.
    :param str resource_group: The resource group containing the resource.
    """
    __args__ = dict()
    __args__['fluidRelayServerName'] = fluid_relay_server_name
    __args__['resourceGroup'] = resource_group
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:fluidrelay/v20220526:getFluidRelayServerKeys', __args__, opts=opts, typ=GetFluidRelayServerKeysResult).value

    return AwaitableGetFluidRelayServerKeysResult(
        key1=__ret__.key1,
        key2=__ret__.key2)


@_utilities.lift_output_func(get_fluid_relay_server_keys)
def get_fluid_relay_server_keys_output(fluid_relay_server_name: Optional[pulumi.Input[str]] = None,
                                       resource_group: Optional[pulumi.Input[str]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFluidRelayServerKeysResult]:
    """
    The set of available keys for this server.


    :param str fluid_relay_server_name: The Fluid Relay server resource name.
    :param str resource_group: The resource group containing the resource.
    """
    ...
