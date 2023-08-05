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
    'GetWordpressInstanceResult',
    'AwaitableGetWordpressInstanceResult',
    'get_wordpress_instance',
    'get_wordpress_instance_output',
]

@pulumi.output_type
class GetWordpressInstanceResult:
    """
    WordPress instance resource
    """
    def __init__(__self__, database_name=None, database_user=None, id=None, name=None, provisioning_state=None, site_url=None, system_data=None, type=None, version=None):
        if database_name and not isinstance(database_name, str):
            raise TypeError("Expected argument 'database_name' to be a str")
        pulumi.set(__self__, "database_name", database_name)
        if database_user and not isinstance(database_user, str):
            raise TypeError("Expected argument 'database_user' to be a str")
        pulumi.set(__self__, "database_user", database_user)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if site_url and not isinstance(site_url, str):
            raise TypeError("Expected argument 'site_url' to be a str")
        pulumi.set(__self__, "site_url", site_url)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> Optional[str]:
        """
        Database name used by the application
        """
        return pulumi.get(self, "database_name")

    @property
    @pulumi.getter(name="databaseUser")
    def database_user(self) -> Optional[str]:
        """
        User name used by the application to connect to database
        """
        return pulumi.get(self, "database_user")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        WordPress instance provisioning state
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="siteUrl")
    def site_url(self) -> str:
        """
        Site Url to access the WordPress application
        """
        return pulumi.get(self, "site_url")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        Application version
        """
        return pulumi.get(self, "version")


class AwaitableGetWordpressInstanceResult(GetWordpressInstanceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWordpressInstanceResult(
            database_name=self.database_name,
            database_user=self.database_user,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            site_url=self.site_url,
            system_data=self.system_data,
            type=self.type,
            version=self.version)


def get_wordpress_instance(php_workload_name: Optional[str] = None,
                           resource_group_name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWordpressInstanceResult:
    """
    WordPress instance resource
    API Version: 2021-12-01-preview.


    :param str php_workload_name: Php workload name
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['phpWorkloadName'] = php_workload_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:workloads:getWordpressInstance', __args__, opts=opts, typ=GetWordpressInstanceResult).value

    return AwaitableGetWordpressInstanceResult(
        database_name=__ret__.database_name,
        database_user=__ret__.database_user,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        site_url=__ret__.site_url,
        system_data=__ret__.system_data,
        type=__ret__.type,
        version=__ret__.version)


@_utilities.lift_output_func(get_wordpress_instance)
def get_wordpress_instance_output(php_workload_name: Optional[pulumi.Input[str]] = None,
                                  resource_group_name: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWordpressInstanceResult]:
    """
    WordPress instance resource
    API Version: 2021-12-01-preview.


    :param str php_workload_name: Php workload name
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
