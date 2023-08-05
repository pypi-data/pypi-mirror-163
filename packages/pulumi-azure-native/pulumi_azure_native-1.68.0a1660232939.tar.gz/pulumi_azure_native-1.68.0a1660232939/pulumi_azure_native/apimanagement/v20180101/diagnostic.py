# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['DiagnosticArgs', 'Diagnostic']

@pulumi.input_type
class DiagnosticArgs:
    def __init__(__self__, *,
                 enabled: pulumi.Input[bool],
                 resource_group_name: pulumi.Input[str],
                 service_name: pulumi.Input[str],
                 diagnostic_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Diagnostic resource.
        :param pulumi.Input[bool] enabled: Indicates whether a diagnostic should receive data or not.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[str] diagnostic_id: Diagnostic identifier. Must be unique in the current API Management service instance.
        """
        pulumi.set(__self__, "enabled", enabled)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "service_name", service_name)
        if diagnostic_id is not None:
            pulumi.set(__self__, "diagnostic_id", diagnostic_id)

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Input[bool]:
        """
        Indicates whether a diagnostic should receive data or not.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enabled", value)

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
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Input[str]:
        """
        The name of the API Management service.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_name", value)

    @property
    @pulumi.getter(name="diagnosticId")
    def diagnostic_id(self) -> Optional[pulumi.Input[str]]:
        """
        Diagnostic identifier. Must be unique in the current API Management service instance.
        """
        return pulumi.get(self, "diagnostic_id")

    @diagnostic_id.setter
    def diagnostic_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "diagnostic_id", value)


class Diagnostic(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 diagnostic_id: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Diagnostic details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] diagnostic_id: Diagnostic identifier. Must be unique in the current API Management service instance.
        :param pulumi.Input[bool] enabled: Indicates whether a diagnostic should receive data or not.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DiagnosticArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Diagnostic details.

        :param str resource_name: The name of the resource.
        :param DiagnosticArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DiagnosticArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 diagnostic_id: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = DiagnosticArgs.__new__(DiagnosticArgs)

            __props__.__dict__["diagnostic_id"] = diagnostic_id
            if enabled is None and not opts.urn:
                raise TypeError("Missing required property 'enabled'")
            __props__.__dict__["enabled"] = enabled
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__.__dict__["service_name"] = service_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:apimanagement:Diagnostic"), pulumi.Alias(type_="azure-native:apimanagement/v20170301:Diagnostic"), pulumi.Alias(type_="azure-native:apimanagement/v20180601preview:Diagnostic"), pulumi.Alias(type_="azure-native:apimanagement/v20190101:Diagnostic"), pulumi.Alias(type_="azure-native:apimanagement/v20191201:Diagnostic"), pulumi.Alias(type_="azure-native:apimanagement/v20191201preview:Diagnostic"), pulumi.Alias(type_="azure-native:apimanagement/v20200601preview:Diagnostic"), pulumi.Alias(type_="azure-native:apimanagement/v20201201:Diagnostic"), pulumi.Alias(type_="azure-native:apimanagement/v20210101preview:Diagnostic"), pulumi.Alias(type_="azure-native:apimanagement/v20210401preview:Diagnostic"), pulumi.Alias(type_="azure-native:apimanagement/v20210801:Diagnostic"), pulumi.Alias(type_="azure-native:apimanagement/v20211201preview:Diagnostic")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Diagnostic, __self__).__init__(
            'azure-native:apimanagement/v20180101:Diagnostic',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Diagnostic':
        """
        Get an existing Diagnostic resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DiagnosticArgs.__new__(DiagnosticArgs)

        __props__.__dict__["enabled"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["type"] = None
        return Diagnostic(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[bool]:
        """
        Indicates whether a diagnostic should receive data or not.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")

