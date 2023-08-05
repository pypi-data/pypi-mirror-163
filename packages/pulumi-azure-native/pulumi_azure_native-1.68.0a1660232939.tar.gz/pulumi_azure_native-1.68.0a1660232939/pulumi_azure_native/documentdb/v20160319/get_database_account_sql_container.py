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
    'GetDatabaseAccountSqlContainerResult',
    'AwaitableGetDatabaseAccountSqlContainerResult',
    'get_database_account_sql_container',
    'get_database_account_sql_container_output',
]

warnings.warn("""Version 2016-03-19 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetDatabaseAccountSqlContainerResult:
    """
    An Azure Cosmos DB container.
    """
    def __init__(__self__, conflict_resolution_policy=None, default_ttl=None, etag=None, id=None, indexing_policy=None, location=None, name=None, partition_key=None, rid=None, tags=None, ts=None, type=None, unique_key_policy=None):
        if conflict_resolution_policy and not isinstance(conflict_resolution_policy, dict):
            raise TypeError("Expected argument 'conflict_resolution_policy' to be a dict")
        pulumi.set(__self__, "conflict_resolution_policy", conflict_resolution_policy)
        if default_ttl and not isinstance(default_ttl, int):
            raise TypeError("Expected argument 'default_ttl' to be a int")
        pulumi.set(__self__, "default_ttl", default_ttl)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if indexing_policy and not isinstance(indexing_policy, dict):
            raise TypeError("Expected argument 'indexing_policy' to be a dict")
        pulumi.set(__self__, "indexing_policy", indexing_policy)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if partition_key and not isinstance(partition_key, dict):
            raise TypeError("Expected argument 'partition_key' to be a dict")
        pulumi.set(__self__, "partition_key", partition_key)
        if rid and not isinstance(rid, str):
            raise TypeError("Expected argument 'rid' to be a str")
        pulumi.set(__self__, "rid", rid)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if ts and not isinstance(ts, dict):
            raise TypeError("Expected argument 'ts' to be a dict")
        pulumi.set(__self__, "ts", ts)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if unique_key_policy and not isinstance(unique_key_policy, dict):
            raise TypeError("Expected argument 'unique_key_policy' to be a dict")
        pulumi.set(__self__, "unique_key_policy", unique_key_policy)

    @property
    @pulumi.getter(name="conflictResolutionPolicy")
    def conflict_resolution_policy(self) -> Optional['outputs.ConflictResolutionPolicyResponse']:
        """
        The conflict resolution policy for the container.
        """
        return pulumi.get(self, "conflict_resolution_policy")

    @property
    @pulumi.getter(name="defaultTtl")
    def default_ttl(self) -> Optional[int]:
        """
        Default time to live
        """
        return pulumi.get(self, "default_ttl")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        A system generated property representing the resource etag required for optimistic concurrency control.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The unique resource identifier of the database account.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="indexingPolicy")
    def indexing_policy(self) -> Optional['outputs.IndexingPolicyResponse']:
        """
        The configuration of the indexing policy. By default, the indexing is automatic for all document paths within the container
        """
        return pulumi.get(self, "indexing_policy")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The location of the resource group to which the resource belongs.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the database account.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="partitionKey")
    def partition_key(self) -> Optional['outputs.ContainerPartitionKeyResponse']:
        """
        The configuration of the partition key to be used for partitioning data into multiple partitions
        """
        return pulumi.get(self, "partition_key")

    @property
    @pulumi.getter
    def rid(self) -> Optional[str]:
        """
        A system generated property. A unique identifier.
        """
        return pulumi.get(self, "rid")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def ts(self) -> Optional[Any]:
        """
        A system generated property that denotes the last updated timestamp of the resource.
        """
        return pulumi.get(self, "ts")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of Azure resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="uniqueKeyPolicy")
    def unique_key_policy(self) -> Optional['outputs.UniqueKeyPolicyResponse']:
        """
        The unique key policy configuration for specifying uniqueness constraints on documents in the collection in the Azure Cosmos DB service.
        """
        return pulumi.get(self, "unique_key_policy")


class AwaitableGetDatabaseAccountSqlContainerResult(GetDatabaseAccountSqlContainerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDatabaseAccountSqlContainerResult(
            conflict_resolution_policy=self.conflict_resolution_policy,
            default_ttl=self.default_ttl,
            etag=self.etag,
            id=self.id,
            indexing_policy=self.indexing_policy,
            location=self.location,
            name=self.name,
            partition_key=self.partition_key,
            rid=self.rid,
            tags=self.tags,
            ts=self.ts,
            type=self.type,
            unique_key_policy=self.unique_key_policy)


def get_database_account_sql_container(account_name: Optional[str] = None,
                                       container_name: Optional[str] = None,
                                       database_name: Optional[str] = None,
                                       resource_group_name: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDatabaseAccountSqlContainerResult:
    """
    An Azure Cosmos DB container.


    :param str account_name: Cosmos DB database account name.
    :param str container_name: Cosmos DB container name.
    :param str database_name: Cosmos DB database name.
    :param str resource_group_name: Name of an Azure resource group.
    """
    pulumi.log.warn("""get_database_account_sql_container is deprecated: Version 2016-03-19 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['containerName'] = container_name
    __args__['databaseName'] = database_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:documentdb/v20160319:getDatabaseAccountSqlContainer', __args__, opts=opts, typ=GetDatabaseAccountSqlContainerResult).value

    return AwaitableGetDatabaseAccountSqlContainerResult(
        conflict_resolution_policy=__ret__.conflict_resolution_policy,
        default_ttl=__ret__.default_ttl,
        etag=__ret__.etag,
        id=__ret__.id,
        indexing_policy=__ret__.indexing_policy,
        location=__ret__.location,
        name=__ret__.name,
        partition_key=__ret__.partition_key,
        rid=__ret__.rid,
        tags=__ret__.tags,
        ts=__ret__.ts,
        type=__ret__.type,
        unique_key_policy=__ret__.unique_key_policy)


@_utilities.lift_output_func(get_database_account_sql_container)
def get_database_account_sql_container_output(account_name: Optional[pulumi.Input[str]] = None,
                                              container_name: Optional[pulumi.Input[str]] = None,
                                              database_name: Optional[pulumi.Input[str]] = None,
                                              resource_group_name: Optional[pulumi.Input[str]] = None,
                                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDatabaseAccountSqlContainerResult]:
    """
    An Azure Cosmos DB container.


    :param str account_name: Cosmos DB database account name.
    :param str container_name: Cosmos DB container name.
    :param str database_name: Cosmos DB database name.
    :param str resource_group_name: Name of an Azure resource group.
    """
    pulumi.log.warn("""get_database_account_sql_container is deprecated: Version 2016-03-19 will be removed in v2 of the provider.""")
    ...
