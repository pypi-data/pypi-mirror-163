# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *

__all__ = ['DpsCertificateArgs', 'DpsCertificate']

@pulumi.input_type
class DpsCertificateArgs:
    def __init__(__self__, *,
                 provisioning_service_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 certificate_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['CertificatePropertiesArgs']] = None):
        """
        The set of arguments for constructing a DpsCertificate resource.
        :param pulumi.Input[str] provisioning_service_name: The name of the provisioning service.
        :param pulumi.Input[str] resource_group_name: Resource group identifier.
        :param pulumi.Input[str] certificate_name: The name of the certificate create or update.
        :param pulumi.Input['CertificatePropertiesArgs'] properties: properties of a certificate
        """
        pulumi.set(__self__, "provisioning_service_name", provisioning_service_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if certificate_name is not None:
            pulumi.set(__self__, "certificate_name", certificate_name)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter(name="provisioningServiceName")
    def provisioning_service_name(self) -> pulumi.Input[str]:
        """
        The name of the provisioning service.
        """
        return pulumi.get(self, "provisioning_service_name")

    @provisioning_service_name.setter
    def provisioning_service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "provisioning_service_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Resource group identifier.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="certificateName")
    def certificate_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the certificate create or update.
        """
        return pulumi.get(self, "certificate_name")

    @certificate_name.setter
    def certificate_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_name", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['CertificatePropertiesArgs']]:
        """
        properties of a certificate
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['CertificatePropertiesArgs']]):
        pulumi.set(self, "properties", value)


class DpsCertificate(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['CertificatePropertiesArgs']]] = None,
                 provisioning_service_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The X509 Certificate.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate_name: The name of the certificate create or update.
        :param pulumi.Input[pulumi.InputType['CertificatePropertiesArgs']] properties: properties of a certificate
        :param pulumi.Input[str] provisioning_service_name: The name of the provisioning service.
        :param pulumi.Input[str] resource_group_name: Resource group identifier.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DpsCertificateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The X509 Certificate.

        :param str resource_name: The name of the resource.
        :param DpsCertificateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DpsCertificateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['CertificatePropertiesArgs']]] = None,
                 provisioning_service_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = DpsCertificateArgs.__new__(DpsCertificateArgs)

            __props__.__dict__["certificate_name"] = certificate_name
            __props__.__dict__["properties"] = properties
            if provisioning_service_name is None and not opts.urn:
                raise TypeError("Missing required property 'provisioning_service_name'")
            __props__.__dict__["provisioning_service_name"] = provisioning_service_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:devices:DpsCertificate"), pulumi.Alias(type_="azure-native:devices/v20170821preview:DpsCertificate"), pulumi.Alias(type_="azure-native:devices/v20171115:DpsCertificate"), pulumi.Alias(type_="azure-native:devices/v20180122:DpsCertificate"), pulumi.Alias(type_="azure-native:devices/v20200101:DpsCertificate"), pulumi.Alias(type_="azure-native:devices/v20200301:DpsCertificate"), pulumi.Alias(type_="azure-native:devices/v20200901preview:DpsCertificate"), pulumi.Alias(type_="azure-native:devices/v20211015:DpsCertificate")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DpsCertificate, __self__).__init__(
            'azure-native:devices/v20220205:DpsCertificate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DpsCertificate':
        """
        Get an existing DpsCertificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DpsCertificateArgs.__new__(DpsCertificateArgs)

        __props__.__dict__["etag"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return DpsCertificate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        The entity tag.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the certificate.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.CertificatePropertiesResponse']:
        """
        properties of a certificate
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

