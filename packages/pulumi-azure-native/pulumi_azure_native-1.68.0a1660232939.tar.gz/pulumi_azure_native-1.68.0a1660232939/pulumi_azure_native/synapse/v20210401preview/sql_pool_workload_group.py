# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['SqlPoolWorkloadGroupArgs', 'SqlPoolWorkloadGroup']

@pulumi.input_type
class SqlPoolWorkloadGroupArgs:
    def __init__(__self__, *,
                 max_resource_percent: pulumi.Input[int],
                 min_resource_percent: pulumi.Input[int],
                 min_resource_percent_per_request: pulumi.Input[float],
                 resource_group_name: pulumi.Input[str],
                 sql_pool_name: pulumi.Input[str],
                 workspace_name: pulumi.Input[str],
                 importance: Optional[pulumi.Input[str]] = None,
                 max_resource_percent_per_request: Optional[pulumi.Input[float]] = None,
                 query_execution_timeout: Optional[pulumi.Input[int]] = None,
                 workload_group_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SqlPoolWorkloadGroup resource.
        :param pulumi.Input[int] max_resource_percent: The workload group cap percentage resource.
        :param pulumi.Input[int] min_resource_percent: The workload group minimum percentage resource.
        :param pulumi.Input[float] min_resource_percent_per_request: The workload group request minimum grant percentage.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] sql_pool_name: SQL pool name
        :param pulumi.Input[str] workspace_name: The name of the workspace
        :param pulumi.Input[str] importance: The workload group importance level.
        :param pulumi.Input[float] max_resource_percent_per_request: The workload group request maximum grant percentage.
        :param pulumi.Input[int] query_execution_timeout: The workload group query execution timeout.
        :param pulumi.Input[str] workload_group_name: The name of the workload group.
        """
        pulumi.set(__self__, "max_resource_percent", max_resource_percent)
        pulumi.set(__self__, "min_resource_percent", min_resource_percent)
        pulumi.set(__self__, "min_resource_percent_per_request", min_resource_percent_per_request)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "sql_pool_name", sql_pool_name)
        pulumi.set(__self__, "workspace_name", workspace_name)
        if importance is not None:
            pulumi.set(__self__, "importance", importance)
        if max_resource_percent_per_request is not None:
            pulumi.set(__self__, "max_resource_percent_per_request", max_resource_percent_per_request)
        if query_execution_timeout is not None:
            pulumi.set(__self__, "query_execution_timeout", query_execution_timeout)
        if workload_group_name is not None:
            pulumi.set(__self__, "workload_group_name", workload_group_name)

    @property
    @pulumi.getter(name="maxResourcePercent")
    def max_resource_percent(self) -> pulumi.Input[int]:
        """
        The workload group cap percentage resource.
        """
        return pulumi.get(self, "max_resource_percent")

    @max_resource_percent.setter
    def max_resource_percent(self, value: pulumi.Input[int]):
        pulumi.set(self, "max_resource_percent", value)

    @property
    @pulumi.getter(name="minResourcePercent")
    def min_resource_percent(self) -> pulumi.Input[int]:
        """
        The workload group minimum percentage resource.
        """
        return pulumi.get(self, "min_resource_percent")

    @min_resource_percent.setter
    def min_resource_percent(self, value: pulumi.Input[int]):
        pulumi.set(self, "min_resource_percent", value)

    @property
    @pulumi.getter(name="minResourcePercentPerRequest")
    def min_resource_percent_per_request(self) -> pulumi.Input[float]:
        """
        The workload group request minimum grant percentage.
        """
        return pulumi.get(self, "min_resource_percent_per_request")

    @min_resource_percent_per_request.setter
    def min_resource_percent_per_request(self, value: pulumi.Input[float]):
        pulumi.set(self, "min_resource_percent_per_request", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="sqlPoolName")
    def sql_pool_name(self) -> pulumi.Input[str]:
        """
        SQL pool name
        """
        return pulumi.get(self, "sql_pool_name")

    @sql_pool_name.setter
    def sql_pool_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "sql_pool_name", value)

    @property
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> pulumi.Input[str]:
        """
        The name of the workspace
        """
        return pulumi.get(self, "workspace_name")

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_name", value)

    @property
    @pulumi.getter
    def importance(self) -> Optional[pulumi.Input[str]]:
        """
        The workload group importance level.
        """
        return pulumi.get(self, "importance")

    @importance.setter
    def importance(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "importance", value)

    @property
    @pulumi.getter(name="maxResourcePercentPerRequest")
    def max_resource_percent_per_request(self) -> Optional[pulumi.Input[float]]:
        """
        The workload group request maximum grant percentage.
        """
        return pulumi.get(self, "max_resource_percent_per_request")

    @max_resource_percent_per_request.setter
    def max_resource_percent_per_request(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "max_resource_percent_per_request", value)

    @property
    @pulumi.getter(name="queryExecutionTimeout")
    def query_execution_timeout(self) -> Optional[pulumi.Input[int]]:
        """
        The workload group query execution timeout.
        """
        return pulumi.get(self, "query_execution_timeout")

    @query_execution_timeout.setter
    def query_execution_timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "query_execution_timeout", value)

    @property
    @pulumi.getter(name="workloadGroupName")
    def workload_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the workload group.
        """
        return pulumi.get(self, "workload_group_name")

    @workload_group_name.setter
    def workload_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workload_group_name", value)


class SqlPoolWorkloadGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 importance: Optional[pulumi.Input[str]] = None,
                 max_resource_percent: Optional[pulumi.Input[int]] = None,
                 max_resource_percent_per_request: Optional[pulumi.Input[float]] = None,
                 min_resource_percent: Optional[pulumi.Input[int]] = None,
                 min_resource_percent_per_request: Optional[pulumi.Input[float]] = None,
                 query_execution_timeout: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sql_pool_name: Optional[pulumi.Input[str]] = None,
                 workload_group_name: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Workload group operations for a sql pool

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] importance: The workload group importance level.
        :param pulumi.Input[int] max_resource_percent: The workload group cap percentage resource.
        :param pulumi.Input[float] max_resource_percent_per_request: The workload group request maximum grant percentage.
        :param pulumi.Input[int] min_resource_percent: The workload group minimum percentage resource.
        :param pulumi.Input[float] min_resource_percent_per_request: The workload group request minimum grant percentage.
        :param pulumi.Input[int] query_execution_timeout: The workload group query execution timeout.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] sql_pool_name: SQL pool name
        :param pulumi.Input[str] workload_group_name: The name of the workload group.
        :param pulumi.Input[str] workspace_name: The name of the workspace
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SqlPoolWorkloadGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Workload group operations for a sql pool

        :param str resource_name: The name of the resource.
        :param SqlPoolWorkloadGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SqlPoolWorkloadGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 importance: Optional[pulumi.Input[str]] = None,
                 max_resource_percent: Optional[pulumi.Input[int]] = None,
                 max_resource_percent_per_request: Optional[pulumi.Input[float]] = None,
                 min_resource_percent: Optional[pulumi.Input[int]] = None,
                 min_resource_percent_per_request: Optional[pulumi.Input[float]] = None,
                 query_execution_timeout: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sql_pool_name: Optional[pulumi.Input[str]] = None,
                 workload_group_name: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SqlPoolWorkloadGroupArgs.__new__(SqlPoolWorkloadGroupArgs)

            __props__.__dict__["importance"] = importance
            if max_resource_percent is None and not opts.urn:
                raise TypeError("Missing required property 'max_resource_percent'")
            __props__.__dict__["max_resource_percent"] = max_resource_percent
            __props__.__dict__["max_resource_percent_per_request"] = max_resource_percent_per_request
            if min_resource_percent is None and not opts.urn:
                raise TypeError("Missing required property 'min_resource_percent'")
            __props__.__dict__["min_resource_percent"] = min_resource_percent
            if min_resource_percent_per_request is None and not opts.urn:
                raise TypeError("Missing required property 'min_resource_percent_per_request'")
            __props__.__dict__["min_resource_percent_per_request"] = min_resource_percent_per_request
            __props__.__dict__["query_execution_timeout"] = query_execution_timeout
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if sql_pool_name is None and not opts.urn:
                raise TypeError("Missing required property 'sql_pool_name'")
            __props__.__dict__["sql_pool_name"] = sql_pool_name
            __props__.__dict__["workload_group_name"] = workload_group_name
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__["workspace_name"] = workspace_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:synapse:SqlPoolWorkloadGroup"), pulumi.Alias(type_="azure-native:synapse/v20190601preview:SqlPoolWorkloadGroup"), pulumi.Alias(type_="azure-native:synapse/v20201201:SqlPoolWorkloadGroup"), pulumi.Alias(type_="azure-native:synapse/v20210301:SqlPoolWorkloadGroup"), pulumi.Alias(type_="azure-native:synapse/v20210501:SqlPoolWorkloadGroup"), pulumi.Alias(type_="azure-native:synapse/v20210601:SqlPoolWorkloadGroup"), pulumi.Alias(type_="azure-native:synapse/v20210601preview:SqlPoolWorkloadGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SqlPoolWorkloadGroup, __self__).__init__(
            'azure-native:synapse/v20210401preview:SqlPoolWorkloadGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SqlPoolWorkloadGroup':
        """
        Get an existing SqlPoolWorkloadGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SqlPoolWorkloadGroupArgs.__new__(SqlPoolWorkloadGroupArgs)

        __props__.__dict__["importance"] = None
        __props__.__dict__["max_resource_percent"] = None
        __props__.__dict__["max_resource_percent_per_request"] = None
        __props__.__dict__["min_resource_percent"] = None
        __props__.__dict__["min_resource_percent_per_request"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["query_execution_timeout"] = None
        __props__.__dict__["type"] = None
        return SqlPoolWorkloadGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def importance(self) -> pulumi.Output[Optional[str]]:
        """
        The workload group importance level.
        """
        return pulumi.get(self, "importance")

    @property
    @pulumi.getter(name="maxResourcePercent")
    def max_resource_percent(self) -> pulumi.Output[int]:
        """
        The workload group cap percentage resource.
        """
        return pulumi.get(self, "max_resource_percent")

    @property
    @pulumi.getter(name="maxResourcePercentPerRequest")
    def max_resource_percent_per_request(self) -> pulumi.Output[Optional[float]]:
        """
        The workload group request maximum grant percentage.
        """
        return pulumi.get(self, "max_resource_percent_per_request")

    @property
    @pulumi.getter(name="minResourcePercent")
    def min_resource_percent(self) -> pulumi.Output[int]:
        """
        The workload group minimum percentage resource.
        """
        return pulumi.get(self, "min_resource_percent")

    @property
    @pulumi.getter(name="minResourcePercentPerRequest")
    def min_resource_percent_per_request(self) -> pulumi.Output[float]:
        """
        The workload group request minimum grant percentage.
        """
        return pulumi.get(self, "min_resource_percent_per_request")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="queryExecutionTimeout")
    def query_execution_timeout(self) -> pulumi.Output[Optional[int]]:
        """
        The workload group query execution timeout.
        """
        return pulumi.get(self, "query_execution_timeout")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

