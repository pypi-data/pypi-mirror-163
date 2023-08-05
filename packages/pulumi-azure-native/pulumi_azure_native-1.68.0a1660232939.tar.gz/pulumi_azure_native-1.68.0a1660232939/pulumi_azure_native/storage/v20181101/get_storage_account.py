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
    'GetStorageAccountResult',
    'AwaitableGetStorageAccountResult',
    'get_storage_account',
    'get_storage_account_output',
]

warnings.warn("""Version 2018-11-01 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetStorageAccountResult:
    """
    The storage account.
    """
    def __init__(__self__, access_tier=None, creation_time=None, custom_domain=None, enable_azure_files_aad_integration=None, enable_https_traffic_only=None, encryption=None, failover_in_progress=None, geo_replication_stats=None, id=None, identity=None, is_hns_enabled=None, kind=None, last_geo_failover_time=None, location=None, name=None, network_rule_set=None, primary_endpoints=None, primary_location=None, provisioning_state=None, secondary_endpoints=None, secondary_location=None, sku=None, status_of_primary=None, status_of_secondary=None, tags=None, type=None):
        if access_tier and not isinstance(access_tier, str):
            raise TypeError("Expected argument 'access_tier' to be a str")
        pulumi.set(__self__, "access_tier", access_tier)
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if custom_domain and not isinstance(custom_domain, dict):
            raise TypeError("Expected argument 'custom_domain' to be a dict")
        pulumi.set(__self__, "custom_domain", custom_domain)
        if enable_azure_files_aad_integration and not isinstance(enable_azure_files_aad_integration, bool):
            raise TypeError("Expected argument 'enable_azure_files_aad_integration' to be a bool")
        pulumi.set(__self__, "enable_azure_files_aad_integration", enable_azure_files_aad_integration)
        if enable_https_traffic_only and not isinstance(enable_https_traffic_only, bool):
            raise TypeError("Expected argument 'enable_https_traffic_only' to be a bool")
        pulumi.set(__self__, "enable_https_traffic_only", enable_https_traffic_only)
        if encryption and not isinstance(encryption, dict):
            raise TypeError("Expected argument 'encryption' to be a dict")
        pulumi.set(__self__, "encryption", encryption)
        if failover_in_progress and not isinstance(failover_in_progress, bool):
            raise TypeError("Expected argument 'failover_in_progress' to be a bool")
        pulumi.set(__self__, "failover_in_progress", failover_in_progress)
        if geo_replication_stats and not isinstance(geo_replication_stats, dict):
            raise TypeError("Expected argument 'geo_replication_stats' to be a dict")
        pulumi.set(__self__, "geo_replication_stats", geo_replication_stats)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if is_hns_enabled and not isinstance(is_hns_enabled, bool):
            raise TypeError("Expected argument 'is_hns_enabled' to be a bool")
        pulumi.set(__self__, "is_hns_enabled", is_hns_enabled)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if last_geo_failover_time and not isinstance(last_geo_failover_time, str):
            raise TypeError("Expected argument 'last_geo_failover_time' to be a str")
        pulumi.set(__self__, "last_geo_failover_time", last_geo_failover_time)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_rule_set and not isinstance(network_rule_set, dict):
            raise TypeError("Expected argument 'network_rule_set' to be a dict")
        pulumi.set(__self__, "network_rule_set", network_rule_set)
        if primary_endpoints and not isinstance(primary_endpoints, dict):
            raise TypeError("Expected argument 'primary_endpoints' to be a dict")
        pulumi.set(__self__, "primary_endpoints", primary_endpoints)
        if primary_location and not isinstance(primary_location, str):
            raise TypeError("Expected argument 'primary_location' to be a str")
        pulumi.set(__self__, "primary_location", primary_location)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if secondary_endpoints and not isinstance(secondary_endpoints, dict):
            raise TypeError("Expected argument 'secondary_endpoints' to be a dict")
        pulumi.set(__self__, "secondary_endpoints", secondary_endpoints)
        if secondary_location and not isinstance(secondary_location, str):
            raise TypeError("Expected argument 'secondary_location' to be a str")
        pulumi.set(__self__, "secondary_location", secondary_location)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if status_of_primary and not isinstance(status_of_primary, str):
            raise TypeError("Expected argument 'status_of_primary' to be a str")
        pulumi.set(__self__, "status_of_primary", status_of_primary)
        if status_of_secondary and not isinstance(status_of_secondary, str):
            raise TypeError("Expected argument 'status_of_secondary' to be a str")
        pulumi.set(__self__, "status_of_secondary", status_of_secondary)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="accessTier")
    def access_tier(self) -> str:
        """
        Required for storage accounts where kind = BlobStorage. The access tier used for billing.
        """
        return pulumi.get(self, "access_tier")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> str:
        """
        Gets the creation date and time of the storage account in UTC.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="customDomain")
    def custom_domain(self) -> 'outputs.CustomDomainResponse':
        """
        Gets the custom domain the user assigned to this storage account.
        """
        return pulumi.get(self, "custom_domain")

    @property
    @pulumi.getter(name="enableAzureFilesAadIntegration")
    def enable_azure_files_aad_integration(self) -> Optional[bool]:
        """
        Enables Azure Files AAD Integration for SMB if sets to true.
        """
        return pulumi.get(self, "enable_azure_files_aad_integration")

    @property
    @pulumi.getter(name="enableHttpsTrafficOnly")
    def enable_https_traffic_only(self) -> Optional[bool]:
        """
        Allows https traffic only to storage service if sets to true.
        """
        return pulumi.get(self, "enable_https_traffic_only")

    @property
    @pulumi.getter
    def encryption(self) -> 'outputs.EncryptionResponse':
        """
        Gets the encryption settings on the account. If unspecified, the account is unencrypted.
        """
        return pulumi.get(self, "encryption")

    @property
    @pulumi.getter(name="failoverInProgress")
    def failover_in_progress(self) -> bool:
        """
        If the failover is in progress, the value will be true, otherwise, it will be null.
        """
        return pulumi.get(self, "failover_in_progress")

    @property
    @pulumi.getter(name="geoReplicationStats")
    def geo_replication_stats(self) -> 'outputs.GeoReplicationStatsResponse':
        """
        Geo Replication Stats
        """
        return pulumi.get(self, "geo_replication_stats")

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
        The identity of the resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="isHnsEnabled")
    def is_hns_enabled(self) -> Optional[bool]:
        """
        Account HierarchicalNamespace enabled if sets to true.
        """
        return pulumi.get(self, "is_hns_enabled")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Gets the Kind.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastGeoFailoverTime")
    def last_geo_failover_time(self) -> str:
        """
        Gets the timestamp of the most recent instance of a failover to the secondary location. Only the most recent timestamp is retained. This element is not returned if there has never been a failover instance. Only available if the accountType is Standard_GRS or Standard_RAGRS.
        """
        return pulumi.get(self, "last_geo_failover_time")

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
    @pulumi.getter(name="networkRuleSet")
    def network_rule_set(self) -> 'outputs.NetworkRuleSetResponse':
        """
        Network rule set
        """
        return pulumi.get(self, "network_rule_set")

    @property
    @pulumi.getter(name="primaryEndpoints")
    def primary_endpoints(self) -> 'outputs.EndpointsResponse':
        """
        Gets the URLs that are used to perform a retrieval of a public blob, queue, or table object. Note that Standard_ZRS and Premium_LRS accounts only return the blob endpoint.
        """
        return pulumi.get(self, "primary_endpoints")

    @property
    @pulumi.getter(name="primaryLocation")
    def primary_location(self) -> str:
        """
        Gets the location of the primary data center for the storage account.
        """
        return pulumi.get(self, "primary_location")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Gets the status of the storage account at the time the operation was called.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="secondaryEndpoints")
    def secondary_endpoints(self) -> 'outputs.EndpointsResponse':
        """
        Gets the URLs that are used to perform a retrieval of a public blob, queue, or table object from the secondary location of the storage account. Only available if the SKU name is Standard_RAGRS.
        """
        return pulumi.get(self, "secondary_endpoints")

    @property
    @pulumi.getter(name="secondaryLocation")
    def secondary_location(self) -> str:
        """
        Gets the location of the geo-replicated secondary for the storage account. Only available if the accountType is Standard_GRS or Standard_RAGRS.
        """
        return pulumi.get(self, "secondary_location")

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.SkuResponse':
        """
        Gets the SKU.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="statusOfPrimary")
    def status_of_primary(self) -> str:
        """
        Gets the status indicating whether the primary location of the storage account is available or unavailable.
        """
        return pulumi.get(self, "status_of_primary")

    @property
    @pulumi.getter(name="statusOfSecondary")
    def status_of_secondary(self) -> str:
        """
        Gets the status indicating whether the secondary location of the storage account is available or unavailable. Only available if the SKU name is Standard_GRS or Standard_RAGRS.
        """
        return pulumi.get(self, "status_of_secondary")

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


class AwaitableGetStorageAccountResult(GetStorageAccountResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStorageAccountResult(
            access_tier=self.access_tier,
            creation_time=self.creation_time,
            custom_domain=self.custom_domain,
            enable_azure_files_aad_integration=self.enable_azure_files_aad_integration,
            enable_https_traffic_only=self.enable_https_traffic_only,
            encryption=self.encryption,
            failover_in_progress=self.failover_in_progress,
            geo_replication_stats=self.geo_replication_stats,
            id=self.id,
            identity=self.identity,
            is_hns_enabled=self.is_hns_enabled,
            kind=self.kind,
            last_geo_failover_time=self.last_geo_failover_time,
            location=self.location,
            name=self.name,
            network_rule_set=self.network_rule_set,
            primary_endpoints=self.primary_endpoints,
            primary_location=self.primary_location,
            provisioning_state=self.provisioning_state,
            secondary_endpoints=self.secondary_endpoints,
            secondary_location=self.secondary_location,
            sku=self.sku,
            status_of_primary=self.status_of_primary,
            status_of_secondary=self.status_of_secondary,
            tags=self.tags,
            type=self.type)


def get_storage_account(account_name: Optional[str] = None,
                        expand: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStorageAccountResult:
    """
    The storage account.


    :param str account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
    :param str expand: May be used to expand the properties within account's properties. By default, data is not included when fetching properties. Currently we only support geoReplicationStats.
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    pulumi.log.warn("""get_storage_account is deprecated: Version 2018-11-01 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['expand'] = expand
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:storage/v20181101:getStorageAccount', __args__, opts=opts, typ=GetStorageAccountResult).value

    return AwaitableGetStorageAccountResult(
        access_tier=__ret__.access_tier,
        creation_time=__ret__.creation_time,
        custom_domain=__ret__.custom_domain,
        enable_azure_files_aad_integration=__ret__.enable_azure_files_aad_integration,
        enable_https_traffic_only=__ret__.enable_https_traffic_only,
        encryption=__ret__.encryption,
        failover_in_progress=__ret__.failover_in_progress,
        geo_replication_stats=__ret__.geo_replication_stats,
        id=__ret__.id,
        identity=__ret__.identity,
        is_hns_enabled=__ret__.is_hns_enabled,
        kind=__ret__.kind,
        last_geo_failover_time=__ret__.last_geo_failover_time,
        location=__ret__.location,
        name=__ret__.name,
        network_rule_set=__ret__.network_rule_set,
        primary_endpoints=__ret__.primary_endpoints,
        primary_location=__ret__.primary_location,
        provisioning_state=__ret__.provisioning_state,
        secondary_endpoints=__ret__.secondary_endpoints,
        secondary_location=__ret__.secondary_location,
        sku=__ret__.sku,
        status_of_primary=__ret__.status_of_primary,
        status_of_secondary=__ret__.status_of_secondary,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_storage_account)
def get_storage_account_output(account_name: Optional[pulumi.Input[str]] = None,
                               expand: Optional[pulumi.Input[Optional[str]]] = None,
                               resource_group_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetStorageAccountResult]:
    """
    The storage account.


    :param str account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
    :param str expand: May be used to expand the properties within account's properties. By default, data is not included when fetching properties. Currently we only support geoReplicationStats.
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    pulumi.log.warn("""get_storage_account is deprecated: Version 2018-11-01 will be removed in v2 of the provider.""")
    ...
