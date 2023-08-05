# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *

__all__ = ['SchemaRegistryArgs', 'SchemaRegistry']

@pulumi.input_type
class SchemaRegistryArgs:
    def __init__(__self__, *,
                 namespace_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 group_properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 schema_compatibility: Optional[pulumi.Input[Union[str, 'SchemaCompatibility']]] = None,
                 schema_group_name: Optional[pulumi.Input[str]] = None,
                 schema_type: Optional[pulumi.Input[Union[str, 'SchemaType']]] = None):
        """
        The set of arguments for constructing a SchemaRegistry resource.
        :param pulumi.Input[str] namespace_name: The Namespace name
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the azure subscription.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] group_properties: dictionary object for SchemaGroup group properties
        :param pulumi.Input[str] schema_group_name: The Schema Group name 
        """
        pulumi.set(__self__, "namespace_name", namespace_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if group_properties is not None:
            pulumi.set(__self__, "group_properties", group_properties)
        if schema_compatibility is not None:
            pulumi.set(__self__, "schema_compatibility", schema_compatibility)
        if schema_group_name is not None:
            pulumi.set(__self__, "schema_group_name", schema_group_name)
        if schema_type is not None:
            pulumi.set(__self__, "schema_type", schema_type)

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> pulumi.Input[str]:
        """
        The Namespace name
        """
        return pulumi.get(self, "namespace_name")

    @namespace_name.setter
    def namespace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "namespace_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group within the azure subscription.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="groupProperties")
    def group_properties(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        dictionary object for SchemaGroup group properties
        """
        return pulumi.get(self, "group_properties")

    @group_properties.setter
    def group_properties(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "group_properties", value)

    @property
    @pulumi.getter(name="schemaCompatibility")
    def schema_compatibility(self) -> Optional[pulumi.Input[Union[str, 'SchemaCompatibility']]]:
        return pulumi.get(self, "schema_compatibility")

    @schema_compatibility.setter
    def schema_compatibility(self, value: Optional[pulumi.Input[Union[str, 'SchemaCompatibility']]]):
        pulumi.set(self, "schema_compatibility", value)

    @property
    @pulumi.getter(name="schemaGroupName")
    def schema_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Schema Group name 
        """
        return pulumi.get(self, "schema_group_name")

    @schema_group_name.setter
    def schema_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schema_group_name", value)

    @property
    @pulumi.getter(name="schemaType")
    def schema_type(self) -> Optional[pulumi.Input[Union[str, 'SchemaType']]]:
        return pulumi.get(self, "schema_type")

    @schema_type.setter
    def schema_type(self, value: Optional[pulumi.Input[Union[str, 'SchemaType']]]):
        pulumi.set(self, "schema_type", value)


class SchemaRegistry(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schema_compatibility: Optional[pulumi.Input[Union[str, 'SchemaCompatibility']]] = None,
                 schema_group_name: Optional[pulumi.Input[str]] = None,
                 schema_type: Optional[pulumi.Input[Union[str, 'SchemaType']]] = None,
                 __props__=None):
        """
        Single item in List or Get Schema Group operation
        API Version: 2022-01-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] group_properties: dictionary object for SchemaGroup group properties
        :param pulumi.Input[str] namespace_name: The Namespace name
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the azure subscription.
        :param pulumi.Input[str] schema_group_name: The Schema Group name 
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SchemaRegistryArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Single item in List or Get Schema Group operation
        API Version: 2022-01-01-preview.

        :param str resource_name: The name of the resource.
        :param SchemaRegistryArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SchemaRegistryArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schema_compatibility: Optional[pulumi.Input[Union[str, 'SchemaCompatibility']]] = None,
                 schema_group_name: Optional[pulumi.Input[str]] = None,
                 schema_type: Optional[pulumi.Input[Union[str, 'SchemaType']]] = None,
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
            __props__ = SchemaRegistryArgs.__new__(SchemaRegistryArgs)

            __props__.__dict__["group_properties"] = group_properties
            if namespace_name is None and not opts.urn:
                raise TypeError("Missing required property 'namespace_name'")
            __props__.__dict__["namespace_name"] = namespace_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["schema_compatibility"] = schema_compatibility
            __props__.__dict__["schema_group_name"] = schema_group_name
            __props__.__dict__["schema_type"] = schema_type
            __props__.__dict__["created_at_utc"] = None
            __props__.__dict__["e_tag"] = None
            __props__.__dict__["location"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["updated_at_utc"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:eventhub/v20211101:SchemaRegistry"), pulumi.Alias(type_="azure-native:eventhub/v20220101preview:SchemaRegistry")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SchemaRegistry, __self__).__init__(
            'azure-native:eventhub:SchemaRegistry',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SchemaRegistry':
        """
        Get an existing SchemaRegistry resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SchemaRegistryArgs.__new__(SchemaRegistryArgs)

        __props__.__dict__["created_at_utc"] = None
        __props__.__dict__["e_tag"] = None
        __props__.__dict__["group_properties"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["schema_compatibility"] = None
        __props__.__dict__["schema_type"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["updated_at_utc"] = None
        return SchemaRegistry(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdAtUtc")
    def created_at_utc(self) -> pulumi.Output[str]:
        """
        Exact time the Schema Group was created.
        """
        return pulumi.get(self, "created_at_utc")

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> pulumi.Output[str]:
        """
        The ETag value.
        """
        return pulumi.get(self, "e_tag")

    @property
    @pulumi.getter(name="groupProperties")
    def group_properties(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        dictionary object for SchemaGroup group properties
        """
        return pulumi.get(self, "group_properties")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="schemaCompatibility")
    def schema_compatibility(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "schema_compatibility")

    @property
    @pulumi.getter(name="schemaType")
    def schema_type(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "schema_type")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.EventHub/Namespaces" or "Microsoft.EventHub/Namespaces/EventHubs"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedAtUtc")
    def updated_at_utc(self) -> pulumi.Output[str]:
        """
        Exact time the Schema Group was updated
        """
        return pulumi.get(self, "updated_at_utc")

