# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._inputs import *

__all__ = [
    'GetFactoryGitHubAccessTokenResult',
    'AwaitableGetFactoryGitHubAccessTokenResult',
    'get_factory_git_hub_access_token',
    'get_factory_git_hub_access_token_output',
]

@pulumi.output_type
class GetFactoryGitHubAccessTokenResult:
    """
    Get GitHub access token response definition.
    """
    def __init__(__self__, git_hub_access_token=None):
        if git_hub_access_token and not isinstance(git_hub_access_token, str):
            raise TypeError("Expected argument 'git_hub_access_token' to be a str")
        pulumi.set(__self__, "git_hub_access_token", git_hub_access_token)

    @property
    @pulumi.getter(name="gitHubAccessToken")
    def git_hub_access_token(self) -> Optional[str]:
        """
        GitHub access token.
        """
        return pulumi.get(self, "git_hub_access_token")


class AwaitableGetFactoryGitHubAccessTokenResult(GetFactoryGitHubAccessTokenResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFactoryGitHubAccessTokenResult(
            git_hub_access_token=self.git_hub_access_token)


def get_factory_git_hub_access_token(factory_name: Optional[str] = None,
                                     git_hub_access_code: Optional[str] = None,
                                     git_hub_access_token_base_url: Optional[str] = None,
                                     git_hub_client_id: Optional[str] = None,
                                     git_hub_client_secret: Optional[pulumi.InputType['GitHubClientSecret']] = None,
                                     resource_group_name: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFactoryGitHubAccessTokenResult:
    """
    Get GitHub access token response definition.
    API Version: 2018-06-01.


    :param str factory_name: The factory name.
    :param str git_hub_access_code: GitHub access code.
    :param str git_hub_access_token_base_url: GitHub access token base URL.
    :param str git_hub_client_id: GitHub application client ID.
    :param pulumi.InputType['GitHubClientSecret'] git_hub_client_secret: GitHub bring your own app client secret information.
    :param str resource_group_name: The resource group name.
    """
    __args__ = dict()
    __args__['factoryName'] = factory_name
    __args__['gitHubAccessCode'] = git_hub_access_code
    __args__['gitHubAccessTokenBaseUrl'] = git_hub_access_token_base_url
    __args__['gitHubClientId'] = git_hub_client_id
    __args__['gitHubClientSecret'] = git_hub_client_secret
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:datafactory:getFactoryGitHubAccessToken', __args__, opts=opts, typ=GetFactoryGitHubAccessTokenResult).value

    return AwaitableGetFactoryGitHubAccessTokenResult(
        git_hub_access_token=__ret__.git_hub_access_token)


@_utilities.lift_output_func(get_factory_git_hub_access_token)
def get_factory_git_hub_access_token_output(factory_name: Optional[pulumi.Input[str]] = None,
                                            git_hub_access_code: Optional[pulumi.Input[str]] = None,
                                            git_hub_access_token_base_url: Optional[pulumi.Input[str]] = None,
                                            git_hub_client_id: Optional[pulumi.Input[Optional[str]]] = None,
                                            git_hub_client_secret: Optional[pulumi.Input[Optional[pulumi.InputType['GitHubClientSecret']]]] = None,
                                            resource_group_name: Optional[pulumi.Input[str]] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFactoryGitHubAccessTokenResult]:
    """
    Get GitHub access token response definition.
    API Version: 2018-06-01.


    :param str factory_name: The factory name.
    :param str git_hub_access_code: GitHub access code.
    :param str git_hub_access_token_base_url: GitHub access token base URL.
    :param str git_hub_client_id: GitHub application client ID.
    :param pulumi.InputType['GitHubClientSecret'] git_hub_client_secret: GitHub bring your own app client secret information.
    :param str resource_group_name: The resource group name.
    """
    ...
