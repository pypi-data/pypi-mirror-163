# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._inputs import *

__all__ = ['AttestationProviderArgs', 'AttestationProvider']

@pulumi.input_type
class AttestationProviderArgs:
    def __init__(__self__, *,
                 properties: pulumi.Input['AttestationServiceCreationSpecificParamsArgs'],
                 resource_group_name: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 provider_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a AttestationProvider resource.
        :param pulumi.Input['AttestationServiceCreationSpecificParamsArgs'] properties: Properties of the attestation service instance
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] location: The supported Azure location where the attestation service instance should be created.
        :param pulumi.Input[str] provider_name: Name of the attestation service instance.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags that will be assigned to the attestation service instance.
        """
        pulumi.set(__self__, "properties", properties)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if provider_name is not None:
            pulumi.set(__self__, "provider_name", provider_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Input['AttestationServiceCreationSpecificParamsArgs']:
        """
        Properties of the attestation service instance
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: pulumi.Input['AttestationServiceCreationSpecificParamsArgs']):
        pulumi.set(self, "properties", value)

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
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The supported Azure location where the attestation service instance should be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="providerName")
    def provider_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the attestation service instance.
        """
        return pulumi.get(self, "provider_name")

    @provider_name.setter
    def provider_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "provider_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The tags that will be assigned to the attestation service instance.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


warnings.warn("""Version 2018-09-01-preview will be removed in v2 of the provider.""", DeprecationWarning)


class AttestationProvider(pulumi.CustomResource):
    warnings.warn("""Version 2018-09-01-preview will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['AttestationServiceCreationSpecificParamsArgs']]] = None,
                 provider_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Attestation service response message.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The supported Azure location where the attestation service instance should be created.
        :param pulumi.Input[pulumi.InputType['AttestationServiceCreationSpecificParamsArgs']] properties: Properties of the attestation service instance
        :param pulumi.Input[str] provider_name: Name of the attestation service instance.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags that will be assigned to the attestation service instance.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AttestationProviderArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Attestation service response message.

        :param str resource_name: The name of the resource.
        :param AttestationProviderArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AttestationProviderArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['AttestationServiceCreationSpecificParamsArgs']]] = None,
                 provider_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        pulumi.log.warn("""AttestationProvider is deprecated: Version 2018-09-01-preview will be removed in v2 of the provider.""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AttestationProviderArgs.__new__(AttestationProviderArgs)

            __props__.__dict__["location"] = location
            if properties is None and not opts.urn:
                raise TypeError("Missing required property 'properties'")
            __props__.__dict__["properties"] = properties
            __props__.__dict__["provider_name"] = provider_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["attest_uri"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["trust_model"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:attestation:AttestationProvider"), pulumi.Alias(type_="azure-native:attestation/v20201001:AttestationProvider"), pulumi.Alias(type_="azure-native:attestation/v20210601preview:AttestationProvider")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AttestationProvider, __self__).__init__(
            'azure-native:attestation/v20180901preview:AttestationProvider',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AttestationProvider':
        """
        Get an existing AttestationProvider resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AttestationProviderArgs.__new__(AttestationProviderArgs)

        __props__.__dict__["attest_uri"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["trust_model"] = None
        __props__.__dict__["type"] = None
        return AttestationProvider(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="attestUri")
    def attest_uri(self) -> pulumi.Output[Optional[str]]:
        """
        Gets the uri of attestation service
        """
        return pulumi.get(self, "attest_uri")

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
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        Status of attestation service.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="trustModel")
    def trust_model(self) -> pulumi.Output[Optional[str]]:
        """
        Trust model for the attestation service instance.
        """
        return pulumi.get(self, "trust_model")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

