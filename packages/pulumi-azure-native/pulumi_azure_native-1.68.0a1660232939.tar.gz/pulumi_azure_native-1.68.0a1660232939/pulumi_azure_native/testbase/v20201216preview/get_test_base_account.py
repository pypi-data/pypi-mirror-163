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
    'GetTestBaseAccountResult',
    'AwaitableGetTestBaseAccountResult',
    'get_test_base_account',
    'get_test_base_account_output',
]

warnings.warn("""Version 2020-12-16-preview will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetTestBaseAccountResult:
    """
    The Test Base Account resource.
    """
    def __init__(__self__, access_level=None, etag=None, id=None, location=None, name=None, provisioning_state=None, sku=None, system_data=None, tags=None, type=None):
        if access_level and not isinstance(access_level, str):
            raise TypeError("Expected argument 'access_level' to be a str")
        pulumi.set(__self__, "access_level", access_level)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
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
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="accessLevel")
    def access_level(self) -> str:
        """
        The access level of the Test Base Account.
        """
        return pulumi.get(self, "access_level")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        Resource Etag.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
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
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.TestBaseAccountSKUResponse':
        """
        The SKU of the Test Base Account.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata relating to this resource
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetTestBaseAccountResult(GetTestBaseAccountResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTestBaseAccountResult(
            access_level=self.access_level,
            etag=self.etag,
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            sku=self.sku,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_test_base_account(resource_group_name: Optional[str] = None,
                          test_base_account_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTestBaseAccountResult:
    """
    The Test Base Account resource.


    :param str resource_group_name: The name of the resource group that contains the resource.
    :param str test_base_account_name: The resource name of the Test Base Account.
    """
    pulumi.log.warn("""get_test_base_account is deprecated: Version 2020-12-16-preview will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['testBaseAccountName'] = test_base_account_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:testbase/v20201216preview:getTestBaseAccount', __args__, opts=opts, typ=GetTestBaseAccountResult).value

    return AwaitableGetTestBaseAccountResult(
        access_level=__ret__.access_level,
        etag=__ret__.etag,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        sku=__ret__.sku,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_test_base_account)
def get_test_base_account_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                 test_base_account_name: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTestBaseAccountResult]:
    """
    The Test Base Account resource.


    :param str resource_group_name: The name of the resource group that contains the resource.
    :param str test_base_account_name: The resource name of the Test Base Account.
    """
    pulumi.log.warn("""get_test_base_account is deprecated: Version 2020-12-16-preview will be removed in v2 of the provider.""")
    ...
