# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'ListWebAppFunctionSecretsResult',
    'AwaitableListWebAppFunctionSecretsResult',
    'list_web_app_function_secrets',
    'list_web_app_function_secrets_output',
]

@pulumi.output_type
class ListWebAppFunctionSecretsResult:
    """
    Function secrets.
    """
    def __init__(__self__, key=None, trigger_url=None):
        if key and not isinstance(key, str):
            raise TypeError("Expected argument 'key' to be a str")
        pulumi.set(__self__, "key", key)
        if trigger_url and not isinstance(trigger_url, str):
            raise TypeError("Expected argument 'trigger_url' to be a str")
        pulumi.set(__self__, "trigger_url", trigger_url)

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        Secret key.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter(name="triggerUrl")
    def trigger_url(self) -> Optional[str]:
        """
        Trigger URL.
        """
        return pulumi.get(self, "trigger_url")


class AwaitableListWebAppFunctionSecretsResult(ListWebAppFunctionSecretsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListWebAppFunctionSecretsResult(
            key=self.key,
            trigger_url=self.trigger_url)


def list_web_app_function_secrets(function_name: Optional[str] = None,
                                  name: Optional[str] = None,
                                  resource_group_name: Optional[str] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListWebAppFunctionSecretsResult:
    """
    Function secrets.


    :param str function_name: Function name.
    :param str name: Site name.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    __args__ = dict()
    __args__['functionName'] = function_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20201201:listWebAppFunctionSecrets', __args__, opts=opts, typ=ListWebAppFunctionSecretsResult).value

    return AwaitableListWebAppFunctionSecretsResult(
        key=__ret__.key,
        trigger_url=__ret__.trigger_url)


@_utilities.lift_output_func(list_web_app_function_secrets)
def list_web_app_function_secrets_output(function_name: Optional[pulumi.Input[str]] = None,
                                         name: Optional[pulumi.Input[str]] = None,
                                         resource_group_name: Optional[pulumi.Input[str]] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListWebAppFunctionSecretsResult]:
    """
    Function secrets.


    :param str function_name: Function name.
    :param str name: Site name.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    ...
