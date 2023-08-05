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
    'ListStreamingLocatorPathsResult',
    'AwaitableListStreamingLocatorPathsResult',
    'list_streaming_locator_paths',
    'list_streaming_locator_paths_output',
]

@pulumi.output_type
class ListStreamingLocatorPathsResult:
    """
    Class of response for listPaths action
    """
    def __init__(__self__, download_paths=None, streaming_paths=None):
        if download_paths and not isinstance(download_paths, list):
            raise TypeError("Expected argument 'download_paths' to be a list")
        pulumi.set(__self__, "download_paths", download_paths)
        if streaming_paths and not isinstance(streaming_paths, list):
            raise TypeError("Expected argument 'streaming_paths' to be a list")
        pulumi.set(__self__, "streaming_paths", streaming_paths)

    @property
    @pulumi.getter(name="downloadPaths")
    def download_paths(self) -> Optional[Sequence[str]]:
        """
        Download Paths supported by current Streaming Locator
        """
        return pulumi.get(self, "download_paths")

    @property
    @pulumi.getter(name="streamingPaths")
    def streaming_paths(self) -> Optional[Sequence['outputs.StreamingPathResponse']]:
        """
        Streaming Paths supported by current Streaming Locator
        """
        return pulumi.get(self, "streaming_paths")


class AwaitableListStreamingLocatorPathsResult(ListStreamingLocatorPathsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListStreamingLocatorPathsResult(
            download_paths=self.download_paths,
            streaming_paths=self.streaming_paths)


def list_streaming_locator_paths(account_name: Optional[str] = None,
                                 resource_group_name: Optional[str] = None,
                                 streaming_locator_name: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListStreamingLocatorPathsResult:
    """
    Class of response for listPaths action


    :param str account_name: The Media Services account name.
    :param str resource_group_name: The name of the resource group within the Azure subscription.
    :param str streaming_locator_name: The Streaming Locator name.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['streamingLocatorName'] = streaming_locator_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:media/v20211101:listStreamingLocatorPaths', __args__, opts=opts, typ=ListStreamingLocatorPathsResult).value

    return AwaitableListStreamingLocatorPathsResult(
        download_paths=__ret__.download_paths,
        streaming_paths=__ret__.streaming_paths)


@_utilities.lift_output_func(list_streaming_locator_paths)
def list_streaming_locator_paths_output(account_name: Optional[pulumi.Input[str]] = None,
                                        resource_group_name: Optional[pulumi.Input[str]] = None,
                                        streaming_locator_name: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListStreamingLocatorPathsResult]:
    """
    Class of response for listPaths action


    :param str account_name: The Media Services account name.
    :param str resource_group_name: The name of the resource group within the Azure subscription.
    :param str streaming_locator_name: The Streaming Locator name.
    """
    ...
