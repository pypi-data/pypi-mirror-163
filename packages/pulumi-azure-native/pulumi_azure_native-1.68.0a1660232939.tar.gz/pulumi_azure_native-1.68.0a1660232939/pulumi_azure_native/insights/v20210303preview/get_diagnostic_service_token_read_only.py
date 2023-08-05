# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetDiagnosticServiceTokenReadOnlyResult',
    'AwaitableGetDiagnosticServiceTokenReadOnlyResult',
    'get_diagnostic_service_token_read_only',
    'get_diagnostic_service_token_read_only_output',
]

@pulumi.output_type
class GetDiagnosticServiceTokenReadOnlyResult:
    """
    The response to a diagnostic services token query.
    """
    def __init__(__self__, token=None):
        if token and not isinstance(token, str):
            raise TypeError("Expected argument 'token' to be a str")
        pulumi.set(__self__, "token", token)

    @property
    @pulumi.getter
    def token(self) -> Optional[str]:
        """
        JWT token for accessing application insights diagnostic service data.
        """
        return pulumi.get(self, "token")


class AwaitableGetDiagnosticServiceTokenReadOnlyResult(GetDiagnosticServiceTokenReadOnlyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDiagnosticServiceTokenReadOnlyResult(
            token=self.token)


def get_diagnostic_service_token_read_only(resource_uri: Optional[str] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDiagnosticServiceTokenReadOnlyResult:
    """
    The response to a diagnostic services token query.


    :param str resource_uri: The identifier of the resource.
    """
    __args__ = dict()
    __args__['resourceUri'] = resource_uri
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:insights/v20210303preview:getDiagnosticServiceTokenReadOnly', __args__, opts=opts, typ=GetDiagnosticServiceTokenReadOnlyResult).value

    return AwaitableGetDiagnosticServiceTokenReadOnlyResult(
        token=__ret__.token)


@_utilities.lift_output_func(get_diagnostic_service_token_read_only)
def get_diagnostic_service_token_read_only_output(resource_uri: Optional[pulumi.Input[str]] = None,
                                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDiagnosticServiceTokenReadOnlyResult]:
    """
    The response to a diagnostic services token query.


    :param str resource_uri: The identifier of the resource.
    """
    ...
