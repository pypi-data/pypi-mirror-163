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
    'GetGlobalUserOperationBatchStatusResult',
    'AwaitableGetGlobalUserOperationBatchStatusResult',
    'get_global_user_operation_batch_status',
    'get_global_user_operation_batch_status_output',
]

@pulumi.output_type
class GetGlobalUserOperationBatchStatusResult:
    """
    Status Details of the long running operation for an environment
    """
    def __init__(__self__, items=None):
        if items and not isinstance(items, list):
            raise TypeError("Expected argument 'items' to be a list")
        pulumi.set(__self__, "items", items)

    @property
    @pulumi.getter
    def items(self) -> Sequence['outputs.OperationBatchStatusResponseItemResponse']:
        """
        Gets a collection of items that contain the operation url and status.
        """
        return pulumi.get(self, "items")


class AwaitableGetGlobalUserOperationBatchStatusResult(GetGlobalUserOperationBatchStatusResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGlobalUserOperationBatchStatusResult(
            items=self.items)


def get_global_user_operation_batch_status(urls: Optional[Sequence[str]] = None,
                                           user_name: Optional[str] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGlobalUserOperationBatchStatusResult:
    """
    Status Details of the long running operation for an environment
    API Version: 2018-10-15.


    :param Sequence[str] urls: The operation url of long running operation
    :param str user_name: The name of the user.
    """
    __args__ = dict()
    __args__['urls'] = urls
    __args__['userName'] = user_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:labservices:getGlobalUserOperationBatchStatus', __args__, opts=opts, typ=GetGlobalUserOperationBatchStatusResult).value

    return AwaitableGetGlobalUserOperationBatchStatusResult(
        items=__ret__.items)


@_utilities.lift_output_func(get_global_user_operation_batch_status)
def get_global_user_operation_batch_status_output(urls: Optional[pulumi.Input[Sequence[str]]] = None,
                                                  user_name: Optional[pulumi.Input[str]] = None,
                                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGlobalUserOperationBatchStatusResult]:
    """
    Status Details of the long running operation for an environment
    API Version: 2018-10-15.


    :param Sequence[str] urls: The operation url of long running operation
    :param str user_name: The name of the user.
    """
    ...
