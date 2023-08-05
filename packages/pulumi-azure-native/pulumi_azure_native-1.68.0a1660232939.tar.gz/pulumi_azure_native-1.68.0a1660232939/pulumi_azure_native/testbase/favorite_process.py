# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = ['FavoriteProcessArgs', 'FavoriteProcess']

@pulumi.input_type
class FavoriteProcessArgs:
    def __init__(__self__, *,
                 actual_process_name: pulumi.Input[str],
                 package_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 test_base_account_name: pulumi.Input[str],
                 favorite_process_resource_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a FavoriteProcess resource.
        :param pulumi.Input[str] actual_process_name: The actual name of the favorite process. It will be equal to resource name except for the scenario that the process name contains characters that are not allowed in the resource name.
        :param pulumi.Input[str] package_name: The resource name of the Test Base Package.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource.
        :param pulumi.Input[str] test_base_account_name: The resource name of the Test Base Account.
        :param pulumi.Input[str] favorite_process_resource_name: The resource name of a favorite process in a package. If the process name contains characters that are not allowed in Azure Resource Name, we use 'actualProcessName' in request body to submit the name.
        """
        pulumi.set(__self__, "actual_process_name", actual_process_name)
        pulumi.set(__self__, "package_name", package_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "test_base_account_name", test_base_account_name)
        if favorite_process_resource_name is not None:
            pulumi.set(__self__, "favorite_process_resource_name", favorite_process_resource_name)

    @property
    @pulumi.getter(name="actualProcessName")
    def actual_process_name(self) -> pulumi.Input[str]:
        """
        The actual name of the favorite process. It will be equal to resource name except for the scenario that the process name contains characters that are not allowed in the resource name.
        """
        return pulumi.get(self, "actual_process_name")

    @actual_process_name.setter
    def actual_process_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "actual_process_name", value)

    @property
    @pulumi.getter(name="packageName")
    def package_name(self) -> pulumi.Input[str]:
        """
        The resource name of the Test Base Package.
        """
        return pulumi.get(self, "package_name")

    @package_name.setter
    def package_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "package_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the resource.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="testBaseAccountName")
    def test_base_account_name(self) -> pulumi.Input[str]:
        """
        The resource name of the Test Base Account.
        """
        return pulumi.get(self, "test_base_account_name")

    @test_base_account_name.setter
    def test_base_account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "test_base_account_name", value)

    @property
    @pulumi.getter(name="favoriteProcessResourceName")
    def favorite_process_resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        The resource name of a favorite process in a package. If the process name contains characters that are not allowed in Azure Resource Name, we use 'actualProcessName' in request body to submit the name.
        """
        return pulumi.get(self, "favorite_process_resource_name")

    @favorite_process_resource_name.setter
    def favorite_process_resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "favorite_process_resource_name", value)


class FavoriteProcess(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actual_process_name: Optional[pulumi.Input[str]] = None,
                 favorite_process_resource_name: Optional[pulumi.Input[str]] = None,
                 package_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 test_base_account_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A favorite process identifier.
        API Version: 2022-04-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] actual_process_name: The actual name of the favorite process. It will be equal to resource name except for the scenario that the process name contains characters that are not allowed in the resource name.
        :param pulumi.Input[str] favorite_process_resource_name: The resource name of a favorite process in a package. If the process name contains characters that are not allowed in Azure Resource Name, we use 'actualProcessName' in request body to submit the name.
        :param pulumi.Input[str] package_name: The resource name of the Test Base Package.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource.
        :param pulumi.Input[str] test_base_account_name: The resource name of the Test Base Account.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FavoriteProcessArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A favorite process identifier.
        API Version: 2022-04-01-preview.

        :param str resource_name: The name of the resource.
        :param FavoriteProcessArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FavoriteProcessArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actual_process_name: Optional[pulumi.Input[str]] = None,
                 favorite_process_resource_name: Optional[pulumi.Input[str]] = None,
                 package_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 test_base_account_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = FavoriteProcessArgs.__new__(FavoriteProcessArgs)

            if actual_process_name is None and not opts.urn:
                raise TypeError("Missing required property 'actual_process_name'")
            __props__.__dict__["actual_process_name"] = actual_process_name
            __props__.__dict__["favorite_process_resource_name"] = favorite_process_resource_name
            if package_name is None and not opts.urn:
                raise TypeError("Missing required property 'package_name'")
            __props__.__dict__["package_name"] = package_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if test_base_account_name is None and not opts.urn:
                raise TypeError("Missing required property 'test_base_account_name'")
            __props__.__dict__["test_base_account_name"] = test_base_account_name
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:testbase/v20201216preview:FavoriteProcess"), pulumi.Alias(type_="azure-native:testbase/v20220401preview:FavoriteProcess")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(FavoriteProcess, __self__).__init__(
            'azure-native:testbase:FavoriteProcess',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'FavoriteProcess':
        """
        Get an existing FavoriteProcess resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = FavoriteProcessArgs.__new__(FavoriteProcessArgs)

        __props__.__dict__["actual_process_name"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return FavoriteProcess(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="actualProcessName")
    def actual_process_name(self) -> pulumi.Output[str]:
        """
        The actual name of the favorite process. It will be equal to resource name except for the scenario that the process name contains characters that are not allowed in the resource name.
        """
        return pulumi.get(self, "actual_process_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata relating to this resource
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

