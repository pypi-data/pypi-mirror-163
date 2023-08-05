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

__all__ = ['NspAssociationsProxyArgs', 'NspAssociationsProxy']

@pulumi.input_type
class NspAssociationsProxyArgs:
    def __init__(__self__, *,
                 network_security_perimeter_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 access_mode: Optional[pulumi.Input[Union[str, 'AssociationAccessMode']]] = None,
                 association_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_link_resource: Optional[pulumi.Input['SubResourceArgs']] = None,
                 profile: Optional[pulumi.Input['SubResourceArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a NspAssociationsProxy resource.
        :param pulumi.Input[str] network_security_perimeter_name: The name of the network security perimeter.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Union[str, 'AssociationAccessMode']] access_mode: Access mode on the association.
        :param pulumi.Input[str] association_name: The name of the NSP association.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input['SubResourceArgs'] private_link_resource: The PaaS resource to be associated.
        :param pulumi.Input['SubResourceArgs'] profile: Profile id to which the PaaS resource is associated.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "network_security_perimeter_name", network_security_perimeter_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if access_mode is not None:
            pulumi.set(__self__, "access_mode", access_mode)
        if association_name is not None:
            pulumi.set(__self__, "association_name", association_name)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if private_link_resource is not None:
            pulumi.set(__self__, "private_link_resource", private_link_resource)
        if profile is not None:
            pulumi.set(__self__, "profile", profile)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="networkSecurityPerimeterName")
    def network_security_perimeter_name(self) -> pulumi.Input[str]:
        """
        The name of the network security perimeter.
        """
        return pulumi.get(self, "network_security_perimeter_name")

    @network_security_perimeter_name.setter
    def network_security_perimeter_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "network_security_perimeter_name", value)

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
    @pulumi.getter(name="accessMode")
    def access_mode(self) -> Optional[pulumi.Input[Union[str, 'AssociationAccessMode']]]:
        """
        Access mode on the association.
        """
        return pulumi.get(self, "access_mode")

    @access_mode.setter
    def access_mode(self, value: Optional[pulumi.Input[Union[str, 'AssociationAccessMode']]]):
        pulumi.set(self, "access_mode", value)

    @property
    @pulumi.getter(name="associationName")
    def association_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the NSP association.
        """
        return pulumi.get(self, "association_name")

    @association_name.setter
    def association_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "association_name", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="privateLinkResource")
    def private_link_resource(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        The PaaS resource to be associated.
        """
        return pulumi.get(self, "private_link_resource")

    @private_link_resource.setter
    def private_link_resource(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, "private_link_resource", value)

    @property
    @pulumi.getter
    def profile(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        Profile id to which the PaaS resource is associated.
        """
        return pulumi.get(self, "profile")

    @profile.setter
    def profile(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, "profile", value)

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


class NspAssociationsProxy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_mode: Optional[pulumi.Input[Union[str, 'AssociationAccessMode']]] = None,
                 association_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_security_perimeter_name: Optional[pulumi.Input[str]] = None,
                 private_link_resource: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 profile: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        The NSP resource association resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'AssociationAccessMode']] access_mode: Access mode on the association.
        :param pulumi.Input[str] association_name: The name of the NSP association.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[str] network_security_perimeter_name: The name of the network security perimeter.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] private_link_resource: The PaaS resource to be associated.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] profile: Profile id to which the PaaS resource is associated.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NspAssociationsProxyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The NSP resource association resource

        :param str resource_name: The name of the resource.
        :param NspAssociationsProxyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NspAssociationsProxyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_mode: Optional[pulumi.Input[Union[str, 'AssociationAccessMode']]] = None,
                 association_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_security_perimeter_name: Optional[pulumi.Input[str]] = None,
                 private_link_resource: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 profile: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
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
            __props__ = NspAssociationsProxyArgs.__new__(NspAssociationsProxyArgs)

            __props__.__dict__["access_mode"] = access_mode
            __props__.__dict__["association_name"] = association_name
            __props__.__dict__["id"] = id
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if network_security_perimeter_name is None and not opts.urn:
                raise TypeError("Missing required property 'network_security_perimeter_name'")
            __props__.__dict__["network_security_perimeter_name"] = network_security_perimeter_name
            __props__.__dict__["private_link_resource"] = private_link_resource
            __props__.__dict__["profile"] = profile
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["has_provisioning_issues"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:NspAssociationsProxy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(NspAssociationsProxy, __self__).__init__(
            'azure-native:network/v20210201preview:NspAssociationsProxy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'NspAssociationsProxy':
        """
        Get an existing NspAssociationsProxy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = NspAssociationsProxyArgs.__new__(NspAssociationsProxyArgs)

        __props__.__dict__["access_mode"] = None
        __props__.__dict__["has_provisioning_issues"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["private_link_resource"] = None
        __props__.__dict__["profile"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return NspAssociationsProxy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessMode")
    def access_mode(self) -> pulumi.Output[Optional[str]]:
        """
        Access mode on the association.
        """
        return pulumi.get(self, "access_mode")

    @property
    @pulumi.getter(name="hasProvisioningIssues")
    def has_provisioning_issues(self) -> pulumi.Output[str]:
        """
        Specifies if there are provisioning issues
        """
        return pulumi.get(self, "has_provisioning_issues")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateLinkResource")
    def private_link_resource(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        The PaaS resource to be associated.
        """
        return pulumi.get(self, "private_link_resource")

    @property
    @pulumi.getter
    def profile(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        Profile id to which the PaaS resource is associated.
        """
        return pulumi.get(self, "profile")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the resource  association resource.
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

