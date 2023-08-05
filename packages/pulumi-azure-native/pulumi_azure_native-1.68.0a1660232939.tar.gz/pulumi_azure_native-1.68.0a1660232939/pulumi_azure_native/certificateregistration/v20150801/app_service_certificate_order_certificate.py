# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['AppServiceCertificateOrderCertificateArgs', 'AppServiceCertificateOrderCertificate']

@pulumi.input_type
class AppServiceCertificateOrderCertificateArgs:
    def __init__(__self__, *,
                 certificate_order_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 key_vault_id: Optional[pulumi.Input[str]] = None,
                 key_vault_secret_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a AppServiceCertificateOrderCertificate resource.
        :param pulumi.Input[str] certificate_order_name: Name of the certificate order.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] key_vault_id: Key Vault resource Id.
        :param pulumi.Input[str] key_vault_secret_name: Key Vault secret name.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input[str] name: Name of the certificate.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "certificate_order_name", certificate_order_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if key_vault_id is not None:
            pulumi.set(__self__, "key_vault_id", key_vault_id)
        if key_vault_secret_name is not None:
            pulumi.set(__self__, "key_vault_secret_name", key_vault_secret_name)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="certificateOrderName")
    def certificate_order_name(self) -> pulumi.Input[str]:
        """
        Name of the certificate order.
        """
        return pulumi.get(self, "certificate_order_name")

    @certificate_order_name.setter
    def certificate_order_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "certificate_order_name", value)

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
    @pulumi.getter(name="keyVaultId")
    def key_vault_id(self) -> Optional[pulumi.Input[str]]:
        """
        Key Vault resource Id.
        """
        return pulumi.get(self, "key_vault_id")

    @key_vault_id.setter
    def key_vault_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_id", value)

    @property
    @pulumi.getter(name="keyVaultSecretName")
    def key_vault_secret_name(self) -> Optional[pulumi.Input[str]]:
        """
        Key Vault secret name.
        """
        return pulumi.get(self, "key_vault_secret_name")

    @key_vault_secret_name.setter
    def key_vault_secret_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_secret_name", value)

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
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the certificate.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


warnings.warn("""Version 2015-08-01 will be removed in v2 of the provider.""", DeprecationWarning)


class AppServiceCertificateOrderCertificate(pulumi.CustomResource):
    warnings.warn("""Version 2015-08-01 will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate_order_name: Optional[pulumi.Input[str]] = None,
                 key_vault_id: Optional[pulumi.Input[str]] = None,
                 key_vault_secret_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Key Vault container ARM resource for a certificate that is purchased through Azure.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate_order_name: Name of the certificate order.
        :param pulumi.Input[str] key_vault_id: Key Vault resource Id.
        :param pulumi.Input[str] key_vault_secret_name: Key Vault secret name.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input[str] name: Name of the certificate.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AppServiceCertificateOrderCertificateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Key Vault container ARM resource for a certificate that is purchased through Azure.

        :param str resource_name: The name of the resource.
        :param AppServiceCertificateOrderCertificateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AppServiceCertificateOrderCertificateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate_order_name: Optional[pulumi.Input[str]] = None,
                 key_vault_id: Optional[pulumi.Input[str]] = None,
                 key_vault_secret_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        pulumi.log.warn("""AppServiceCertificateOrderCertificate is deprecated: Version 2015-08-01 will be removed in v2 of the provider.""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AppServiceCertificateOrderCertificateArgs.__new__(AppServiceCertificateOrderCertificateArgs)

            if certificate_order_name is None and not opts.urn:
                raise TypeError("Missing required property 'certificate_order_name'")
            __props__.__dict__["certificate_order_name"] = certificate_order_name
            __props__.__dict__["key_vault_id"] = key_vault_id
            __props__.__dict__["key_vault_secret_name"] = key_vault_secret_name
            __props__.__dict__["kind"] = kind
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:certificateregistration:AppServiceCertificateOrderCertificate"), pulumi.Alias(type_="azure-native:certificateregistration/v20180201:AppServiceCertificateOrderCertificate"), pulumi.Alias(type_="azure-native:certificateregistration/v20190801:AppServiceCertificateOrderCertificate"), pulumi.Alias(type_="azure-native:certificateregistration/v20200601:AppServiceCertificateOrderCertificate"), pulumi.Alias(type_="azure-native:certificateregistration/v20200901:AppServiceCertificateOrderCertificate"), pulumi.Alias(type_="azure-native:certificateregistration/v20201001:AppServiceCertificateOrderCertificate"), pulumi.Alias(type_="azure-native:certificateregistration/v20201201:AppServiceCertificateOrderCertificate"), pulumi.Alias(type_="azure-native:certificateregistration/v20210101:AppServiceCertificateOrderCertificate"), pulumi.Alias(type_="azure-native:certificateregistration/v20210115:AppServiceCertificateOrderCertificate"), pulumi.Alias(type_="azure-native:certificateregistration/v20210201:AppServiceCertificateOrderCertificate"), pulumi.Alias(type_="azure-native:certificateregistration/v20210301:AppServiceCertificateOrderCertificate"), pulumi.Alias(type_="azure-native:certificateregistration/v20220301:AppServiceCertificateOrderCertificate")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AppServiceCertificateOrderCertificate, __self__).__init__(
            'azure-native:certificateregistration/v20150801:AppServiceCertificateOrderCertificate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AppServiceCertificateOrderCertificate':
        """
        Get an existing AppServiceCertificateOrderCertificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AppServiceCertificateOrderCertificateArgs.__new__(AppServiceCertificateOrderCertificateArgs)

        __props__.__dict__["key_vault_id"] = None
        __props__.__dict__["key_vault_secret_name"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return AppServiceCertificateOrderCertificate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="keyVaultId")
    def key_vault_id(self) -> pulumi.Output[Optional[str]]:
        """
        Key Vault resource Id.
        """
        return pulumi.get(self, "key_vault_id")

    @property
    @pulumi.getter(name="keyVaultSecretName")
    def key_vault_secret_name(self) -> pulumi.Output[Optional[str]]:
        """
        Key Vault secret name.
        """
        return pulumi.get(self, "key_vault_secret_name")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Status of the Key Vault secret.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

