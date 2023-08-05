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

__all__ = ['AnalyticsItemArgs', 'AnalyticsItem']

@pulumi.input_type
class AnalyticsItemArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 resource_name: pulumi.Input[str],
                 scope_path: pulumi.Input[str],
                 content: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 override_item: Optional[pulumi.Input[bool]] = None,
                 properties: Optional[pulumi.Input['ApplicationInsightsComponentAnalyticsItemPropertiesArgs']] = None,
                 scope: Optional[pulumi.Input[Union[str, 'ItemScope']]] = None,
                 type: Optional[pulumi.Input[Union[str, 'ItemType']]] = None):
        """
        The set of arguments for constructing a AnalyticsItem resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] resource_name: The name of the Application Insights component resource.
        :param pulumi.Input[str] scope_path: Enum indicating if this item definition is owned by a specific user or is shared between all users with access to the Application Insights component.
        :param pulumi.Input[str] content: The content of this item
        :param pulumi.Input[str] id: Internally assigned unique id of the item definition.
        :param pulumi.Input[str] name: The user-defined name of the item.
        :param pulumi.Input[bool] override_item: Flag indicating whether or not to force save an item. This allows overriding an item if it already exists.
        :param pulumi.Input['ApplicationInsightsComponentAnalyticsItemPropertiesArgs'] properties: A set of properties that can be defined in the context of a specific item type. Each type may have its own properties.
        :param pulumi.Input[Union[str, 'ItemScope']] scope: Enum indicating if this item definition is owned by a specific user or is shared between all users with access to the Application Insights component.
        :param pulumi.Input[Union[str, 'ItemType']] type: Enum indicating the type of the Analytics item.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "resource_name", resource_name)
        pulumi.set(__self__, "scope_path", scope_path)
        if content is not None:
            pulumi.set(__self__, "content", content)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if override_item is not None:
            pulumi.set(__self__, "override_item", override_item)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if scope is not None:
            pulumi.set(__self__, "scope", scope)
        if type is not None:
            pulumi.set(__self__, "type", type)

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
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> pulumi.Input[str]:
        """
        The name of the Application Insights component resource.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter(name="scopePath")
    def scope_path(self) -> pulumi.Input[str]:
        """
        Enum indicating if this item definition is owned by a specific user or is shared between all users with access to the Application Insights component.
        """
        return pulumi.get(self, "scope_path")

    @scope_path.setter
    def scope_path(self, value: pulumi.Input[str]):
        pulumi.set(self, "scope_path", value)

    @property
    @pulumi.getter
    def content(self) -> Optional[pulumi.Input[str]]:
        """
        The content of this item
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Internally assigned unique id of the item definition.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The user-defined name of the item.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="overrideItem")
    def override_item(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag indicating whether or not to force save an item. This allows overriding an item if it already exists.
        """
        return pulumi.get(self, "override_item")

    @override_item.setter
    def override_item(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "override_item", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['ApplicationInsightsComponentAnalyticsItemPropertiesArgs']]:
        """
        A set of properties that can be defined in the context of a specific item type. Each type may have its own properties.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['ApplicationInsightsComponentAnalyticsItemPropertiesArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter
    def scope(self) -> Optional[pulumi.Input[Union[str, 'ItemScope']]]:
        """
        Enum indicating if this item definition is owned by a specific user or is shared between all users with access to the Application Insights component.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: Optional[pulumi.Input[Union[str, 'ItemScope']]]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'ItemType']]]:
        """
        Enum indicating the type of the Analytics item.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'ItemType']]]):
        pulumi.set(self, "type", value)


class AnalyticsItem(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 content: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 override_item: Optional[pulumi.Input[bool]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['ApplicationInsightsComponentAnalyticsItemPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[Union[str, 'ItemScope']]] = None,
                 scope_path: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[Union[str, 'ItemType']]] = None,
                 __props__=None):
        """
        Properties that define an Analytics item that is associated to an Application Insights component.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] content: The content of this item
        :param pulumi.Input[str] id: Internally assigned unique id of the item definition.
        :param pulumi.Input[str] name: The user-defined name of the item.
        :param pulumi.Input[bool] override_item: Flag indicating whether or not to force save an item. This allows overriding an item if it already exists.
        :param pulumi.Input[pulumi.InputType['ApplicationInsightsComponentAnalyticsItemPropertiesArgs']] properties: A set of properties that can be defined in the context of a specific item type. Each type may have its own properties.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] resource_name_: The name of the Application Insights component resource.
        :param pulumi.Input[Union[str, 'ItemScope']] scope: Enum indicating if this item definition is owned by a specific user or is shared between all users with access to the Application Insights component.
        :param pulumi.Input[str] scope_path: Enum indicating if this item definition is owned by a specific user or is shared between all users with access to the Application Insights component.
        :param pulumi.Input[Union[str, 'ItemType']] type: Enum indicating the type of the Analytics item.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AnalyticsItemArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Properties that define an Analytics item that is associated to an Application Insights component.

        :param str resource_name: The name of the resource.
        :param AnalyticsItemArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AnalyticsItemArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 content: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 override_item: Optional[pulumi.Input[bool]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['ApplicationInsightsComponentAnalyticsItemPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[Union[str, 'ItemScope']]] = None,
                 scope_path: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[Union[str, 'ItemType']]] = None,
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
            __props__ = AnalyticsItemArgs.__new__(AnalyticsItemArgs)

            __props__.__dict__["content"] = content
            __props__.__dict__["id"] = id
            __props__.__dict__["name"] = name
            __props__.__dict__["override_item"] = override_item
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["scope"] = scope
            if scope_path is None and not opts.urn:
                raise TypeError("Missing required property 'scope_path'")
            __props__.__dict__["scope_path"] = scope_path
            __props__.__dict__["type"] = type
            __props__.__dict__["time_created"] = None
            __props__.__dict__["time_modified"] = None
            __props__.__dict__["version"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:insights:AnalyticsItem")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AnalyticsItem, __self__).__init__(
            'azure-native:insights/v20150501:AnalyticsItem',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AnalyticsItem':
        """
        Get an existing AnalyticsItem resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AnalyticsItemArgs.__new__(AnalyticsItemArgs)

        __props__.__dict__["content"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["scope"] = None
        __props__.__dict__["time_created"] = None
        __props__.__dict__["time_modified"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["version"] = None
        return AnalyticsItem(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def content(self) -> pulumi.Output[Optional[str]]:
        """
        The content of this item
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The user-defined name of the item.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.ApplicationInsightsComponentAnalyticsItemPropertiesResponse']:
        """
        A set of properties that can be defined in the context of a specific item type. Each type may have its own properties.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Output[Optional[str]]:
        """
        Enum indicating if this item definition is owned by a specific user or is shared between all users with access to the Application Insights component.
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter(name="timeCreated")
    def time_created(self) -> pulumi.Output[str]:
        """
        Date and time in UTC when this item was created.
        """
        return pulumi.get(self, "time_created")

    @property
    @pulumi.getter(name="timeModified")
    def time_modified(self) -> pulumi.Output[str]:
        """
        Date and time in UTC of the last modification that was made to this item.
        """
        return pulumi.get(self, "time_modified")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[Optional[str]]:
        """
        Enum indicating the type of the Analytics item.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        This instance's version of the data model. This can change as new features are added.
        """
        return pulumi.get(self, "version")

