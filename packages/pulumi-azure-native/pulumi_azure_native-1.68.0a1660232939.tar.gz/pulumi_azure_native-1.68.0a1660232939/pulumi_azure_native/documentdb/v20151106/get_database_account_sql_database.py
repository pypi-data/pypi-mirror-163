# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetDatabaseAccountSqlDatabaseResult',
    'AwaitableGetDatabaseAccountSqlDatabaseResult',
    'get_database_account_sql_database',
    'get_database_account_sql_database_output',
]

warnings.warn("""Version 2015-11-06 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetDatabaseAccountSqlDatabaseResult:
    """
    An Azure Cosmos DB SQL database.
    """
    def __init__(__self__, colls=None, etag=None, id=None, location=None, name=None, rid=None, tags=None, ts=None, type=None, users=None):
        if colls and not isinstance(colls, str):
            raise TypeError("Expected argument 'colls' to be a str")
        pulumi.set(__self__, "colls", colls)
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
        if users and not isinstance(users, str):
            raise TypeError("Expected argument 'users' to be a str")
        pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter
    def colls(self) -> Optional[str]:
        """
        A system generated property that specified the addressable path of the collections resource.
        """
        return pulumi.get(self, "colls")

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
    @pulumi.getter
    def users(self) -> Optional[str]:
        """
        A system generated property that specifies the addressable path of the users resource.
        """
        return pulumi.get(self, "users")


class AwaitableGetDatabaseAccountSqlDatabaseResult(GetDatabaseAccountSqlDatabaseResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDatabaseAccountSqlDatabaseResult(
            colls=self.colls,
            etag=self.etag,
            id=self.id,
            location=self.location,
            name=self.name,
            rid=self.rid,
            tags=self.tags,
            ts=self.ts,
            type=self.type,
            users=self.users)


def get_database_account_sql_database(account_name: Optional[str] = None,
                                      database_name: Optional[str] = None,
                                      resource_group_name: Optional[str] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDatabaseAccountSqlDatabaseResult:
    """
    An Azure Cosmos DB SQL database.


    :param str account_name: Cosmos DB database account name.
    :param str database_name: Cosmos DB database name.
    :param str resource_group_name: Name of an Azure resource group.
    """
    pulumi.log.warn("""get_database_account_sql_database is deprecated: Version 2015-11-06 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['databaseName'] = database_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:documentdb/v20151106:getDatabaseAccountSqlDatabase', __args__, opts=opts, typ=GetDatabaseAccountSqlDatabaseResult).value

    return AwaitableGetDatabaseAccountSqlDatabaseResult(
        colls=__ret__.colls,
        etag=__ret__.etag,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        rid=__ret__.rid,
        tags=__ret__.tags,
        ts=__ret__.ts,
        type=__ret__.type,
        users=__ret__.users)


@_utilities.lift_output_func(get_database_account_sql_database)
def get_database_account_sql_database_output(account_name: Optional[pulumi.Input[str]] = None,
                                             database_name: Optional[pulumi.Input[str]] = None,
                                             resource_group_name: Optional[pulumi.Input[str]] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDatabaseAccountSqlDatabaseResult]:
    """
    An Azure Cosmos DB SQL database.


    :param str account_name: Cosmos DB database account name.
    :param str database_name: Cosmos DB database name.
    :param str resource_group_name: Name of an Azure resource group.
    """
    pulumi.log.warn("""get_database_account_sql_database is deprecated: Version 2015-11-06 will be removed in v2 of the provider.""")
    ...
