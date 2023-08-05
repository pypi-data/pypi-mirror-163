# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['ViewArgs', 'View']

@pulumi.input_type
class ViewArgs:
    def __init__(__self__, *,
                 definition: pulumi.Input[str],
                 hub_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 display_name: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 view_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a View resource.
        :param pulumi.Input[str] definition: View definition.
        :param pulumi.Input[str] hub_name: The name of the hub.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] display_name: Localized display name for the view.
        :param pulumi.Input[str] user_id: the user ID.
        :param pulumi.Input[str] view_name: The name of the view.
        """
        pulumi.set(__self__, "definition", definition)
        pulumi.set(__self__, "hub_name", hub_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if user_id is not None:
            pulumi.set(__self__, "user_id", user_id)
        if view_name is not None:
            pulumi.set(__self__, "view_name", view_name)

    @property
    @pulumi.getter
    def definition(self) -> pulumi.Input[str]:
        """
        View definition.
        """
        return pulumi.get(self, "definition")

    @definition.setter
    def definition(self, value: pulumi.Input[str]):
        pulumi.set(self, "definition", value)

    @property
    @pulumi.getter(name="hubName")
    def hub_name(self) -> pulumi.Input[str]:
        """
        The name of the hub.
        """
        return pulumi.get(self, "hub_name")

    @hub_name.setter
    def hub_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "hub_name", value)

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
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Localized display name for the view.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[pulumi.Input[str]]:
        """
        the user ID.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_id", value)

    @property
    @pulumi.getter(name="viewName")
    def view_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the view.
        """
        return pulumi.get(self, "view_name")

    @view_name.setter
    def view_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "view_name", value)


warnings.warn("""Version 2017-01-01 will be removed in v2 of the provider.""", DeprecationWarning)


class View(pulumi.CustomResource):
    warnings.warn("""Version 2017-01-01 will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 definition: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 hub_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 view_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The view resource format.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] definition: View definition.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] display_name: Localized display name for the view.
        :param pulumi.Input[str] hub_name: The name of the hub.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] user_id: the user ID.
        :param pulumi.Input[str] view_name: The name of the view.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ViewArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The view resource format.

        :param str resource_name: The name of the resource.
        :param ViewArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ViewArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 definition: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 hub_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 view_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""View is deprecated: Version 2017-01-01 will be removed in v2 of the provider.""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ViewArgs.__new__(ViewArgs)

            if definition is None and not opts.urn:
                raise TypeError("Missing required property 'definition'")
            __props__.__dict__["definition"] = definition
            __props__.__dict__["display_name"] = display_name
            if hub_name is None and not opts.urn:
                raise TypeError("Missing required property 'hub_name'")
            __props__.__dict__["hub_name"] = hub_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["user_id"] = user_id
            __props__.__dict__["view_name"] = view_name
            __props__.__dict__["changed"] = None
            __props__.__dict__["created"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["tenant_id"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:customerinsights:View"), pulumi.Alias(type_="azure-native:customerinsights/v20170426:View")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(View, __self__).__init__(
            'azure-native:customerinsights/v20170101:View',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'View':
        """
        Get an existing View resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ViewArgs.__new__(ViewArgs)

        __props__.__dict__["changed"] = None
        __props__.__dict__["created"] = None
        __props__.__dict__["definition"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["tenant_id"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["user_id"] = None
        __props__.__dict__["view_name"] = None
        return View(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def changed(self) -> pulumi.Output[str]:
        """
        Date time when view was last modified.
        """
        return pulumi.get(self, "changed")

    @property
    @pulumi.getter
    def created(self) -> pulumi.Output[str]:
        """
        Date time when view was created.
        """
        return pulumi.get(self, "created")

    @property
    @pulumi.getter
    def definition(self) -> pulumi.Output[str]:
        """
        View definition.
        """
        return pulumi.get(self, "definition")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Localized display name for the view.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> pulumi.Output[str]:
        """
        the hub name.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Output[Optional[str]]:
        """
        the user ID.
        """
        return pulumi.get(self, "user_id")

    @property
    @pulumi.getter(name="viewName")
    def view_name(self) -> pulumi.Output[str]:
        """
        Name of the view.
        """
        return pulumi.get(self, "view_name")

