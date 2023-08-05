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

__all__ = ['StaticSiteArgs', 'StaticSite']

@pulumi.input_type
class StaticSiteArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 allow_config_file_updates: Optional[pulumi.Input[bool]] = None,
                 branch: Optional[pulumi.Input[str]] = None,
                 build_properties: Optional[pulumi.Input['StaticSiteBuildPropertiesArgs']] = None,
                 identity: Optional[pulumi.Input['ManagedServiceIdentityArgs']] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 repository_token: Optional[pulumi.Input[str]] = None,
                 repository_url: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input['SkuDescriptionArgs']] = None,
                 staging_environment_policy: Optional[pulumi.Input['StagingEnvironmentPolicy']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 template_properties: Optional[pulumi.Input['StaticSiteTemplateOptionsArgs']] = None):
        """
        The set of arguments for constructing a StaticSite resource.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[bool] allow_config_file_updates: <code>false</code> if config file is locked for this static web app; otherwise, <code>true</code>.
        :param pulumi.Input[str] branch: The target branch in the repository.
        :param pulumi.Input['StaticSiteBuildPropertiesArgs'] build_properties: Build properties to configure on the repository.
        :param pulumi.Input['ManagedServiceIdentityArgs'] identity: Managed service identity.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input[str] name: Name of the static site to create or update.
        :param pulumi.Input[str] repository_token: A user's github repository token. This is used to setup the Github Actions workflow file and API secrets.
        :param pulumi.Input[str] repository_url: URL for the repository of the static site.
        :param pulumi.Input['SkuDescriptionArgs'] sku: Description of a SKU for a scalable resource.
        :param pulumi.Input['StagingEnvironmentPolicy'] staging_environment_policy: State indicating whether staging environments are allowed or not allowed for a static web app.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input['StaticSiteTemplateOptionsArgs'] template_properties: Template options for generating a new repository.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if allow_config_file_updates is not None:
            pulumi.set(__self__, "allow_config_file_updates", allow_config_file_updates)
        if branch is not None:
            pulumi.set(__self__, "branch", branch)
        if build_properties is not None:
            pulumi.set(__self__, "build_properties", build_properties)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if repository_token is not None:
            pulumi.set(__self__, "repository_token", repository_token)
        if repository_url is not None:
            pulumi.set(__self__, "repository_url", repository_url)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if staging_environment_policy is not None:
            pulumi.set(__self__, "staging_environment_policy", staging_environment_policy)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if template_properties is not None:
            pulumi.set(__self__, "template_properties", template_properties)

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
    @pulumi.getter(name="allowConfigFileUpdates")
    def allow_config_file_updates(self) -> Optional[pulumi.Input[bool]]:
        """
        <code>false</code> if config file is locked for this static web app; otherwise, <code>true</code>.
        """
        return pulumi.get(self, "allow_config_file_updates")

    @allow_config_file_updates.setter
    def allow_config_file_updates(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_config_file_updates", value)

    @property
    @pulumi.getter
    def branch(self) -> Optional[pulumi.Input[str]]:
        """
        The target branch in the repository.
        """
        return pulumi.get(self, "branch")

    @branch.setter
    def branch(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "branch", value)

    @property
    @pulumi.getter(name="buildProperties")
    def build_properties(self) -> Optional[pulumi.Input['StaticSiteBuildPropertiesArgs']]:
        """
        Build properties to configure on the repository.
        """
        return pulumi.get(self, "build_properties")

    @build_properties.setter
    def build_properties(self, value: Optional[pulumi.Input['StaticSiteBuildPropertiesArgs']]):
        pulumi.set(self, "build_properties", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ManagedServiceIdentityArgs']]:
        """
        Managed service identity.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ManagedServiceIdentityArgs']]):
        pulumi.set(self, "identity", value)

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
        Name of the static site to create or update.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="repositoryToken")
    def repository_token(self) -> Optional[pulumi.Input[str]]:
        """
        A user's github repository token. This is used to setup the Github Actions workflow file and API secrets.
        """
        return pulumi.get(self, "repository_token")

    @repository_token.setter
    def repository_token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "repository_token", value)

    @property
    @pulumi.getter(name="repositoryUrl")
    def repository_url(self) -> Optional[pulumi.Input[str]]:
        """
        URL for the repository of the static site.
        """
        return pulumi.get(self, "repository_url")

    @repository_url.setter
    def repository_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "repository_url", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['SkuDescriptionArgs']]:
        """
        Description of a SKU for a scalable resource.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['SkuDescriptionArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter(name="stagingEnvironmentPolicy")
    def staging_environment_policy(self) -> Optional[pulumi.Input['StagingEnvironmentPolicy']]:
        """
        State indicating whether staging environments are allowed or not allowed for a static web app.
        """
        return pulumi.get(self, "staging_environment_policy")

    @staging_environment_policy.setter
    def staging_environment_policy(self, value: Optional[pulumi.Input['StagingEnvironmentPolicy']]):
        pulumi.set(self, "staging_environment_policy", value)

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

    @property
    @pulumi.getter(name="templateProperties")
    def template_properties(self) -> Optional[pulumi.Input['StaticSiteTemplateOptionsArgs']]:
        """
        Template options for generating a new repository.
        """
        return pulumi.get(self, "template_properties")

    @template_properties.setter
    def template_properties(self, value: Optional[pulumi.Input['StaticSiteTemplateOptionsArgs']]):
        pulumi.set(self, "template_properties", value)


class StaticSite(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_config_file_updates: Optional[pulumi.Input[bool]] = None,
                 branch: Optional[pulumi.Input[str]] = None,
                 build_properties: Optional[pulumi.Input[pulumi.InputType['StaticSiteBuildPropertiesArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 repository_token: Optional[pulumi.Input[str]] = None,
                 repository_url: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuDescriptionArgs']]] = None,
                 staging_environment_policy: Optional[pulumi.Input['StagingEnvironmentPolicy']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 template_properties: Optional[pulumi.Input[pulumi.InputType['StaticSiteTemplateOptionsArgs']]] = None,
                 __props__=None):
        """
        Static Site ARM resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_config_file_updates: <code>false</code> if config file is locked for this static web app; otherwise, <code>true</code>.
        :param pulumi.Input[str] branch: The target branch in the repository.
        :param pulumi.Input[pulumi.InputType['StaticSiteBuildPropertiesArgs']] build_properties: Build properties to configure on the repository.
        :param pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']] identity: Managed service identity.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input[str] name: Name of the static site to create or update.
        :param pulumi.Input[str] repository_token: A user's github repository token. This is used to setup the Github Actions workflow file and API secrets.
        :param pulumi.Input[str] repository_url: URL for the repository of the static site.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[pulumi.InputType['SkuDescriptionArgs']] sku: Description of a SKU for a scalable resource.
        :param pulumi.Input['StagingEnvironmentPolicy'] staging_environment_policy: State indicating whether staging environments are allowed or not allowed for a static web app.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[pulumi.InputType['StaticSiteTemplateOptionsArgs']] template_properties: Template options for generating a new repository.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StaticSiteArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Static Site ARM resource.

        :param str resource_name: The name of the resource.
        :param StaticSiteArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StaticSiteArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_config_file_updates: Optional[pulumi.Input[bool]] = None,
                 branch: Optional[pulumi.Input[str]] = None,
                 build_properties: Optional[pulumi.Input[pulumi.InputType['StaticSiteBuildPropertiesArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 repository_token: Optional[pulumi.Input[str]] = None,
                 repository_url: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuDescriptionArgs']]] = None,
                 staging_environment_policy: Optional[pulumi.Input['StagingEnvironmentPolicy']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 template_properties: Optional[pulumi.Input[pulumi.InputType['StaticSiteTemplateOptionsArgs']]] = None,
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
            __props__ = StaticSiteArgs.__new__(StaticSiteArgs)

            __props__.__dict__["allow_config_file_updates"] = allow_config_file_updates
            __props__.__dict__["branch"] = branch
            __props__.__dict__["build_properties"] = build_properties
            __props__.__dict__["identity"] = identity
            __props__.__dict__["kind"] = kind
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["repository_token"] = repository_token
            __props__.__dict__["repository_url"] = repository_url
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["staging_environment_policy"] = staging_environment_policy
            __props__.__dict__["tags"] = tags
            __props__.__dict__["template_properties"] = template_properties
            __props__.__dict__["content_distribution_endpoint"] = None
            __props__.__dict__["custom_domains"] = None
            __props__.__dict__["default_hostname"] = None
            __props__.__dict__["key_vault_reference_identity"] = None
            __props__.__dict__["private_endpoint_connections"] = None
            __props__.__dict__["provider"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["user_provided_function_apps"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:web:StaticSite"), pulumi.Alias(type_="azure-native:web/v20190801:StaticSite"), pulumi.Alias(type_="azure-native:web/v20200601:StaticSite"), pulumi.Alias(type_="azure-native:web/v20200901:StaticSite"), pulumi.Alias(type_="azure-native:web/v20201001:StaticSite"), pulumi.Alias(type_="azure-native:web/v20201201:StaticSite"), pulumi.Alias(type_="azure-native:web/v20210115:StaticSite"), pulumi.Alias(type_="azure-native:web/v20210201:StaticSite"), pulumi.Alias(type_="azure-native:web/v20210301:StaticSite"), pulumi.Alias(type_="azure-native:web/v20220301:StaticSite")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StaticSite, __self__).__init__(
            'azure-native:web/v20210101:StaticSite',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StaticSite':
        """
        Get an existing StaticSite resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = StaticSiteArgs.__new__(StaticSiteArgs)

        __props__.__dict__["allow_config_file_updates"] = None
        __props__.__dict__["branch"] = None
        __props__.__dict__["build_properties"] = None
        __props__.__dict__["content_distribution_endpoint"] = None
        __props__.__dict__["custom_domains"] = None
        __props__.__dict__["default_hostname"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["key_vault_reference_identity"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["private_endpoint_connections"] = None
        __props__.__dict__["provider"] = None
        __props__.__dict__["repository_token"] = None
        __props__.__dict__["repository_url"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["staging_environment_policy"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["template_properties"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["user_provided_function_apps"] = None
        return StaticSite(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowConfigFileUpdates")
    def allow_config_file_updates(self) -> pulumi.Output[Optional[bool]]:
        """
        <code>false</code> if config file is locked for this static web app; otherwise, <code>true</code>.
        """
        return pulumi.get(self, "allow_config_file_updates")

    @property
    @pulumi.getter
    def branch(self) -> pulumi.Output[Optional[str]]:
        """
        The target branch in the repository.
        """
        return pulumi.get(self, "branch")

    @property
    @pulumi.getter(name="buildProperties")
    def build_properties(self) -> pulumi.Output[Optional['outputs.StaticSiteBuildPropertiesResponse']]:
        """
        Build properties to configure on the repository.
        """
        return pulumi.get(self, "build_properties")

    @property
    @pulumi.getter(name="contentDistributionEndpoint")
    def content_distribution_endpoint(self) -> pulumi.Output[str]:
        """
        The content distribution endpoint for the static site.
        """
        return pulumi.get(self, "content_distribution_endpoint")

    @property
    @pulumi.getter(name="customDomains")
    def custom_domains(self) -> pulumi.Output[Sequence[str]]:
        """
        The custom domains associated with this static site.
        """
        return pulumi.get(self, "custom_domains")

    @property
    @pulumi.getter(name="defaultHostname")
    def default_hostname(self) -> pulumi.Output[str]:
        """
        The default autogenerated hostname for the static site.
        """
        return pulumi.get(self, "default_hostname")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ManagedServiceIdentityResponse']]:
        """
        Managed service identity.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="keyVaultReferenceIdentity")
    def key_vault_reference_identity(self) -> pulumi.Output[str]:
        """
        Identity to use for Key Vault Reference authentication.
        """
        return pulumi.get(self, "key_vault_reference_identity")

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
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> pulumi.Output[Sequence['outputs.ResponseMessageEnvelopeRemotePrivateEndpointConnectionResponse']]:
        """
        Private endpoint connections
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter
    def provider(self) -> pulumi.Output[str]:
        """
        The provider that submitted the last deployment to the primary environment of the static site.
        """
        return pulumi.get(self, "provider")

    @property
    @pulumi.getter(name="repositoryToken")
    def repository_token(self) -> pulumi.Output[Optional[str]]:
        """
        A user's github repository token. This is used to setup the Github Actions workflow file and API secrets.
        """
        return pulumi.get(self, "repository_token")

    @property
    @pulumi.getter(name="repositoryUrl")
    def repository_url(self) -> pulumi.Output[Optional[str]]:
        """
        URL for the repository of the static site.
        """
        return pulumi.get(self, "repository_url")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuDescriptionResponse']]:
        """
        Description of a SKU for a scalable resource.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="stagingEnvironmentPolicy")
    def staging_environment_policy(self) -> pulumi.Output[Optional[str]]:
        """
        State indicating whether staging environments are allowed or not allowed for a static web app.
        """
        return pulumi.get(self, "staging_environment_policy")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="templateProperties")
    def template_properties(self) -> pulumi.Output[Optional['outputs.StaticSiteTemplateOptionsResponse']]:
        """
        Template options for generating a new repository.
        """
        return pulumi.get(self, "template_properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userProvidedFunctionApps")
    def user_provided_function_apps(self) -> pulumi.Output[Sequence['outputs.StaticSiteUserProvidedFunctionAppResponse']]:
        """
        User provided function apps registered with the static site
        """
        return pulumi.get(self, "user_provided_function_apps")

