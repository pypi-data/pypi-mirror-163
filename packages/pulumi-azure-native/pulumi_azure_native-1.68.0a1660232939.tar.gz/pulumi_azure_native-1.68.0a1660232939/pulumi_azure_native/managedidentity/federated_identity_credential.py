# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['FederatedIdentityCredentialArgs', 'FederatedIdentityCredential']

@pulumi.input_type
class FederatedIdentityCredentialArgs:
    def __init__(__self__, *,
                 audiences: pulumi.Input[Sequence[pulumi.Input[str]]],
                 issuer: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 resource_name: pulumi.Input[str],
                 subject: pulumi.Input[str],
                 federated_identity_credential_resource_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a FederatedIdentityCredential resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] audiences: The list of audiences that can appear in the issued token.
        :param pulumi.Input[str] issuer: The URL of the issuer to be trusted.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group to which the identity belongs.
        :param pulumi.Input[str] resource_name: The name of the identity resource.
        :param pulumi.Input[str] subject: The identifier of the external identity.
        :param pulumi.Input[str] federated_identity_credential_resource_name: The name of the federated identity credential resource.
        """
        pulumi.set(__self__, "audiences", audiences)
        pulumi.set(__self__, "issuer", issuer)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "resource_name", resource_name)
        pulumi.set(__self__, "subject", subject)
        if federated_identity_credential_resource_name is not None:
            pulumi.set(__self__, "federated_identity_credential_resource_name", federated_identity_credential_resource_name)

    @property
    @pulumi.getter
    def audiences(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The list of audiences that can appear in the issued token.
        """
        return pulumi.get(self, "audiences")

    @audiences.setter
    def audiences(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "audiences", value)

    @property
    @pulumi.getter
    def issuer(self) -> pulumi.Input[str]:
        """
        The URL of the issuer to be trusted.
        """
        return pulumi.get(self, "issuer")

    @issuer.setter
    def issuer(self, value: pulumi.Input[str]):
        pulumi.set(self, "issuer", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group to which the identity belongs.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> pulumi.Input[str]:
        """
        The name of the identity resource.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter
    def subject(self) -> pulumi.Input[str]:
        """
        The identifier of the external identity.
        """
        return pulumi.get(self, "subject")

    @subject.setter
    def subject(self, value: pulumi.Input[str]):
        pulumi.set(self, "subject", value)

    @property
    @pulumi.getter(name="federatedIdentityCredentialResourceName")
    def federated_identity_credential_resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the federated identity credential resource.
        """
        return pulumi.get(self, "federated_identity_credential_resource_name")

    @federated_identity_credential_resource_name.setter
    def federated_identity_credential_resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "federated_identity_credential_resource_name", value)


class FederatedIdentityCredential(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 audiences: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 federated_identity_credential_resource_name: Optional[pulumi.Input[str]] = None,
                 issuer: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 subject: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Describes a federated identity credential.
        API Version: 2022-01-31-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] audiences: The list of audiences that can appear in the issued token.
        :param pulumi.Input[str] federated_identity_credential_resource_name: The name of the federated identity credential resource.
        :param pulumi.Input[str] issuer: The URL of the issuer to be trusted.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group to which the identity belongs.
        :param pulumi.Input[str] resource_name_: The name of the identity resource.
        :param pulumi.Input[str] subject: The identifier of the external identity.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FederatedIdentityCredentialArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Describes a federated identity credential.
        API Version: 2022-01-31-preview.

        :param str resource_name: The name of the resource.
        :param FederatedIdentityCredentialArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FederatedIdentityCredentialArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 audiences: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 federated_identity_credential_resource_name: Optional[pulumi.Input[str]] = None,
                 issuer: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 subject: Optional[pulumi.Input[str]] = None,
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
            __props__ = FederatedIdentityCredentialArgs.__new__(FederatedIdentityCredentialArgs)

            if audiences is None and not opts.urn:
                raise TypeError("Missing required property 'audiences'")
            __props__.__dict__["audiences"] = audiences
            __props__.__dict__["federated_identity_credential_resource_name"] = federated_identity_credential_resource_name
            if issuer is None and not opts.urn:
                raise TypeError("Missing required property 'issuer'")
            __props__.__dict__["issuer"] = issuer
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__["resource_name"] = resource_name_
            if subject is None and not opts.urn:
                raise TypeError("Missing required property 'subject'")
            __props__.__dict__["subject"] = subject
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:managedidentity/v20220131preview:FederatedIdentityCredential")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(FederatedIdentityCredential, __self__).__init__(
            'azure-native:managedidentity:FederatedIdentityCredential',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'FederatedIdentityCredential':
        """
        Get an existing FederatedIdentityCredential resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = FederatedIdentityCredentialArgs.__new__(FederatedIdentityCredentialArgs)

        __props__.__dict__["audiences"] = None
        __props__.__dict__["issuer"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["subject"] = None
        __props__.__dict__["type"] = None
        return FederatedIdentityCredential(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def audiences(self) -> pulumi.Output[Sequence[str]]:
        """
        The list of audiences that can appear in the issued token.
        """
        return pulumi.get(self, "audiences")

    @property
    @pulumi.getter
    def issuer(self) -> pulumi.Output[str]:
        """
        The URL of the issuer to be trusted.
        """
        return pulumi.get(self, "issuer")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def subject(self) -> pulumi.Output[str]:
        """
        The identifier of the external identity.
        """
        return pulumi.get(self, "subject")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

