# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['StaticSiteCustomDomainArgs', 'StaticSiteCustomDomain']

@pulumi.input_type
class StaticSiteCustomDomainArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 domain_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 validation_method: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a StaticSiteCustomDomain resource.
        :param pulumi.Input[str] name: Name of the static site.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] domain_name: The custom domain to create.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] validation_method: Validation method for adding a custom domain
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if domain_name is not None:
            pulumi.set(__self__, "domain_name", domain_name)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if validation_method is None:
            validation_method = 'cname-delegation'
        if validation_method is not None:
            pulumi.set(__self__, "validation_method", validation_method)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the static site.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group to which the resource belongs.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        The custom domain to create.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter(name="validationMethod")
    def validation_method(self) -> Optional[pulumi.Input[str]]:
        """
        Validation method for adding a custom domain
        """
        return pulumi.get(self, "validation_method")

    @validation_method.setter
    def validation_method(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "validation_method", value)


class StaticSiteCustomDomain(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 validation_method: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Static Site Custom Domain Overview ARM resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] domain_name: The custom domain to create.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: Name of the static site.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] validation_method: Validation method for adding a custom domain
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StaticSiteCustomDomainArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Static Site Custom Domain Overview ARM resource.

        :param str resource_name: The name of the resource.
        :param StaticSiteCustomDomainArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StaticSiteCustomDomainArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 validation_method: Optional[pulumi.Input[str]] = None,
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
            __props__ = StaticSiteCustomDomainArgs.__new__(StaticSiteCustomDomainArgs)

            __props__.__dict__["domain_name"] = domain_name
            __props__.__dict__["kind"] = kind
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if validation_method is None:
                validation_method = 'cname-delegation'
            __props__.__dict__["validation_method"] = validation_method
            __props__.__dict__["created_on"] = None
            __props__.__dict__["error_message"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["validation_token"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:web:StaticSiteCustomDomain"), pulumi.Alias(type_="azure-native:web/v20210101:StaticSiteCustomDomain"), pulumi.Alias(type_="azure-native:web/v20210115:StaticSiteCustomDomain"), pulumi.Alias(type_="azure-native:web/v20210201:StaticSiteCustomDomain"), pulumi.Alias(type_="azure-native:web/v20210301:StaticSiteCustomDomain"), pulumi.Alias(type_="azure-native:web/v20220301:StaticSiteCustomDomain")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StaticSiteCustomDomain, __self__).__init__(
            'azure-native:web/v20201201:StaticSiteCustomDomain',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StaticSiteCustomDomain':
        """
        Get an existing StaticSiteCustomDomain resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = StaticSiteCustomDomainArgs.__new__(StaticSiteCustomDomainArgs)

        __props__.__dict__["created_on"] = None
        __props__.__dict__["domain_name"] = None
        __props__.__dict__["error_message"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["validation_token"] = None
        return StaticSiteCustomDomain(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdOn")
    def created_on(self) -> pulumi.Output[str]:
        """
        The date and time on which the custom domain was created for the static site.
        """
        return pulumi.get(self, "created_on")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Output[str]:
        """
        The domain name for the static site custom domain.
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter(name="errorMessage")
    def error_message(self) -> pulumi.Output[str]:
        return pulumi.get(self, "error_message")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the custom domain
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="validationToken")
    def validation_token(self) -> pulumi.Output[str]:
        """
        The TXT record validation token
        """
        return pulumi.get(self, "validation_token")

