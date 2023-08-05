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
    'GetRemoteRenderingAccountResult',
    'AwaitableGetRemoteRenderingAccountResult',
    'get_remote_rendering_account',
    'get_remote_rendering_account_output',
]

warnings.warn("""Version 2020-04-06-preview will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetRemoteRenderingAccountResult:
    """
    RemoteRenderingAccount Response.
    """
    def __init__(__self__, account_domain=None, account_id=None, id=None, identity=None, kind=None, location=None, name=None, plan=None, sku=None, storage_account_name=None, system_data=None, tags=None, type=None):
        if account_domain and not isinstance(account_domain, str):
            raise TypeError("Expected argument 'account_domain' to be a str")
        pulumi.set(__self__, "account_domain", account_domain)
        if account_id and not isinstance(account_id, str):
            raise TypeError("Expected argument 'account_id' to be a str")
        pulumi.set(__self__, "account_id", account_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if kind and not isinstance(kind, dict):
            raise TypeError("Expected argument 'kind' to be a dict")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if plan and not isinstance(plan, dict):
            raise TypeError("Expected argument 'plan' to be a dict")
        pulumi.set(__self__, "plan", plan)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if storage_account_name and not isinstance(storage_account_name, str):
            raise TypeError("Expected argument 'storage_account_name' to be a str")
        pulumi.set(__self__, "storage_account_name", storage_account_name)
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
    @pulumi.getter(name="accountDomain")
    def account_domain(self) -> str:
        """
        Correspond domain name of certain Spatial Anchors Account
        """
        return pulumi.get(self, "account_domain")

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> str:
        """
        unique id of certain account.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.IdentityResponse']:
        """
        The identity associated with this account
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def kind(self) -> Optional['outputs.SkuResponse']:
        """
        The kind of account, if supported
        """
        return pulumi.get(self, "kind")

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
    @pulumi.getter
    def plan(self) -> Optional['outputs.IdentityResponse']:
        """
        The plan associated with this account
        """
        return pulumi.get(self, "plan")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.SkuResponse']:
        """
        The sku associated with this account
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="storageAccountName")
    def storage_account_name(self) -> Optional[str]:
        """
        The name of the storage account associated with this accountId
        """
        return pulumi.get(self, "storage_account_name")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        System metadata for this account
        """
        return pulumi.get(self, "system_data")

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
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetRemoteRenderingAccountResult(GetRemoteRenderingAccountResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRemoteRenderingAccountResult(
            account_domain=self.account_domain,
            account_id=self.account_id,
            id=self.id,
            identity=self.identity,
            kind=self.kind,
            location=self.location,
            name=self.name,
            plan=self.plan,
            sku=self.sku,
            storage_account_name=self.storage_account_name,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_remote_rendering_account(account_name: Optional[str] = None,
                                 resource_group_name: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRemoteRenderingAccountResult:
    """
    RemoteRenderingAccount Response.


    :param str account_name: Name of an Mixed Reality Account.
    :param str resource_group_name: Name of an Azure resource group.
    """
    pulumi.log.warn("""get_remote_rendering_account is deprecated: Version 2020-04-06-preview will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:mixedreality/v20200406preview:getRemoteRenderingAccount', __args__, opts=opts, typ=GetRemoteRenderingAccountResult).value

    return AwaitableGetRemoteRenderingAccountResult(
        account_domain=__ret__.account_domain,
        account_id=__ret__.account_id,
        id=__ret__.id,
        identity=__ret__.identity,
        kind=__ret__.kind,
        location=__ret__.location,
        name=__ret__.name,
        plan=__ret__.plan,
        sku=__ret__.sku,
        storage_account_name=__ret__.storage_account_name,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_remote_rendering_account)
def get_remote_rendering_account_output(account_name: Optional[pulumi.Input[str]] = None,
                                        resource_group_name: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRemoteRenderingAccountResult]:
    """
    RemoteRenderingAccount Response.


    :param str account_name: Name of an Mixed Reality Account.
    :param str resource_group_name: Name of an Azure resource group.
    """
    pulumi.log.warn("""get_remote_rendering_account is deprecated: Version 2020-04-06-preview will be removed in v2 of the provider.""")
    ...
