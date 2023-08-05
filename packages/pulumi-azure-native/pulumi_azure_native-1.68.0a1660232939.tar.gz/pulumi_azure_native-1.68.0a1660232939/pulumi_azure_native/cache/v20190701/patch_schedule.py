# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['PatchScheduleArgs', 'PatchSchedule']

@pulumi.input_type
class PatchScheduleArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 schedule_entries: pulumi.Input[Sequence[pulumi.Input['ScheduleEntryArgs']]],
                 default: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a PatchSchedule resource.
        :param pulumi.Input[str] name: The name of the Redis cache.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input['ScheduleEntryArgs']]] schedule_entries: List of patch schedules for a Redis cache.
        :param pulumi.Input[str] default: Default string modeled as parameter for auto generation to work correctly.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "schedule_entries", schedule_entries)
        if default is not None:
            pulumi.set(__self__, "default", default)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the Redis cache.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="scheduleEntries")
    def schedule_entries(self) -> pulumi.Input[Sequence[pulumi.Input['ScheduleEntryArgs']]]:
        """
        List of patch schedules for a Redis cache.
        """
        return pulumi.get(self, "schedule_entries")

    @schedule_entries.setter
    def schedule_entries(self, value: pulumi.Input[Sequence[pulumi.Input['ScheduleEntryArgs']]]):
        pulumi.set(self, "schedule_entries", value)

    @property
    @pulumi.getter
    def default(self) -> Optional[pulumi.Input[str]]:
        """
        Default string modeled as parameter for auto generation to work correctly.
        """
        return pulumi.get(self, "default")

    @default.setter
    def default(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default", value)


warnings.warn("""Version 2019-07-01 will be removed in v2 of the provider.""", DeprecationWarning)


class PatchSchedule(pulumi.CustomResource):
    warnings.warn("""Version 2019-07-01 will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 default: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schedule_entries: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ScheduleEntryArgs']]]]] = None,
                 __props__=None):
        """
        Response to put/get patch schedules for Redis cache.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] default: Default string modeled as parameter for auto generation to work correctly.
        :param pulumi.Input[str] name: The name of the Redis cache.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ScheduleEntryArgs']]]] schedule_entries: List of patch schedules for a Redis cache.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PatchScheduleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Response to put/get patch schedules for Redis cache.

        :param str resource_name: The name of the resource.
        :param PatchScheduleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PatchScheduleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 default: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schedule_entries: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ScheduleEntryArgs']]]]] = None,
                 __props__=None):
        pulumi.log.warn("""PatchSchedule is deprecated: Version 2019-07-01 will be removed in v2 of the provider.""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PatchScheduleArgs.__new__(PatchScheduleArgs)

            __props__.__dict__["default"] = default
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if schedule_entries is None and not opts.urn:
                raise TypeError("Missing required property 'schedule_entries'")
            __props__.__dict__["schedule_entries"] = schedule_entries
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:cache:PatchSchedule"), pulumi.Alias(type_="azure-native:cache/v20171001:PatchSchedule"), pulumi.Alias(type_="azure-native:cache/v20180301:PatchSchedule"), pulumi.Alias(type_="azure-native:cache/v20200601:PatchSchedule"), pulumi.Alias(type_="azure-native:cache/v20201201:PatchSchedule"), pulumi.Alias(type_="azure-native:cache/v20210601:PatchSchedule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(PatchSchedule, __self__).__init__(
            'azure-native:cache/v20190701:PatchSchedule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PatchSchedule':
        """
        Get an existing PatchSchedule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PatchScheduleArgs.__new__(PatchScheduleArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["schedule_entries"] = None
        __props__.__dict__["type"] = None
        return PatchSchedule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="scheduleEntries")
    def schedule_entries(self) -> pulumi.Output[Sequence['outputs.ScheduleEntryResponse']]:
        """
        List of patch schedules for a Redis cache.
        """
        return pulumi.get(self, "schedule_entries")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

