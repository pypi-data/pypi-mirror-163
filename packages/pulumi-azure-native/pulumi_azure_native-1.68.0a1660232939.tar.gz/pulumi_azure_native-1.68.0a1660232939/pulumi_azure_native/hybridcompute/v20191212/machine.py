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

__all__ = ['MachineArgs', 'Machine']

@pulumi.input_type
class MachineArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 client_public_key: Optional[pulumi.Input[str]] = None,
                 extensions: Optional[pulumi.Input[Sequence[pulumi.Input['MachineExtensionInstanceViewArgs']]]] = None,
                 identity: Optional[pulumi.Input['MachineIdentityArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 location_data: Optional[pulumi.Input['LocationDataArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vm_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Machine resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] client_public_key: Public Key that the client provides to be used during initial resource onboarding
        :param pulumi.Input[Sequence[pulumi.Input['MachineExtensionInstanceViewArgs']]] extensions: Machine Extensions information
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input['LocationDataArgs'] location_data: Metadata pertaining to the geographic location of the resource.
        :param pulumi.Input[str] name: The name of the hybrid machine.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] vm_id: Specifies the hybrid machine unique ID.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if client_public_key is not None:
            pulumi.set(__self__, "client_public_key", client_public_key)
        if extensions is not None:
            pulumi.set(__self__, "extensions", extensions)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if location_data is not None:
            pulumi.set(__self__, "location_data", location_data)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if vm_id is not None:
            pulumi.set(__self__, "vm_id", vm_id)

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
    @pulumi.getter(name="clientPublicKey")
    def client_public_key(self) -> Optional[pulumi.Input[str]]:
        """
        Public Key that the client provides to be used during initial resource onboarding
        """
        return pulumi.get(self, "client_public_key")

    @client_public_key.setter
    def client_public_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_public_key", value)

    @property
    @pulumi.getter
    def extensions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['MachineExtensionInstanceViewArgs']]]]:
        """
        Machine Extensions information
        """
        return pulumi.get(self, "extensions")

    @extensions.setter
    def extensions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['MachineExtensionInstanceViewArgs']]]]):
        pulumi.set(self, "extensions", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['MachineIdentityArgs']]:
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['MachineIdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="locationData")
    def location_data(self) -> Optional[pulumi.Input['LocationDataArgs']]:
        """
        Metadata pertaining to the geographic location of the resource.
        """
        return pulumi.get(self, "location_data")

    @location_data.setter
    def location_data(self, value: Optional[pulumi.Input['LocationDataArgs']]):
        pulumi.set(self, "location_data", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the hybrid machine.
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

    @property
    @pulumi.getter(name="vmId")
    def vm_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the hybrid machine unique ID.
        """
        return pulumi.get(self, "vm_id")

    @vm_id.setter
    def vm_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vm_id", value)


warnings.warn("""Version 2019-12-12 will be removed in v2 of the provider.""", DeprecationWarning)


class Machine(pulumi.CustomResource):
    warnings.warn("""Version 2019-12-12 will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 client_public_key: Optional[pulumi.Input[str]] = None,
                 extensions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MachineExtensionInstanceViewArgs']]]]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['MachineIdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 location_data: Optional[pulumi.Input[pulumi.InputType['LocationDataArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vm_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Describes a hybrid machine.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] client_public_key: Public Key that the client provides to be used during initial resource onboarding
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MachineExtensionInstanceViewArgs']]]] extensions: Machine Extensions information
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[pulumi.InputType['LocationDataArgs']] location_data: Metadata pertaining to the geographic location of the resource.
        :param pulumi.Input[str] name: The name of the hybrid machine.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] vm_id: Specifies the hybrid machine unique ID.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MachineArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Describes a hybrid machine.

        :param str resource_name: The name of the resource.
        :param MachineArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MachineArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 client_public_key: Optional[pulumi.Input[str]] = None,
                 extensions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MachineExtensionInstanceViewArgs']]]]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['MachineIdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 location_data: Optional[pulumi.Input[pulumi.InputType['LocationDataArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vm_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""Machine is deprecated: Version 2019-12-12 will be removed in v2 of the provider.""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MachineArgs.__new__(MachineArgs)

            __props__.__dict__["client_public_key"] = client_public_key
            __props__.__dict__["extensions"] = extensions
            __props__.__dict__["identity"] = identity
            __props__.__dict__["location"] = location
            __props__.__dict__["location_data"] = location_data
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["vm_id"] = vm_id
            __props__.__dict__["agent_version"] = None
            __props__.__dict__["display_name"] = None
            __props__.__dict__["error_details"] = None
            __props__.__dict__["last_status_change"] = None
            __props__.__dict__["machine_fqdn"] = None
            __props__.__dict__["os_name"] = None
            __props__.__dict__["os_profile"] = None
            __props__.__dict__["os_version"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:hybridcompute:Machine"), pulumi.Alias(type_="azure-native:hybridcompute/v20190318preview:Machine"), pulumi.Alias(type_="azure-native:hybridcompute/v20190802preview:Machine"), pulumi.Alias(type_="azure-native:hybridcompute/v20200730preview:Machine"), pulumi.Alias(type_="azure-native:hybridcompute/v20200802:Machine"), pulumi.Alias(type_="azure-native:hybridcompute/v20200815preview:Machine"), pulumi.Alias(type_="azure-native:hybridcompute/v20210128preview:Machine"), pulumi.Alias(type_="azure-native:hybridcompute/v20210325preview:Machine"), pulumi.Alias(type_="azure-native:hybridcompute/v20210422preview:Machine"), pulumi.Alias(type_="azure-native:hybridcompute/v20210517preview:Machine"), pulumi.Alias(type_="azure-native:hybridcompute/v20210520:Machine"), pulumi.Alias(type_="azure-native:hybridcompute/v20210610preview:Machine"), pulumi.Alias(type_="azure-native:hybridcompute/v20211210preview:Machine"), pulumi.Alias(type_="azure-native:hybridcompute/v20220310:Machine"), pulumi.Alias(type_="azure-native:hybridcompute/v20220510preview:Machine")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Machine, __self__).__init__(
            'azure-native:hybridcompute/v20191212:Machine',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Machine':
        """
        Get an existing Machine resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MachineArgs.__new__(MachineArgs)

        __props__.__dict__["agent_version"] = None
        __props__.__dict__["client_public_key"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["error_details"] = None
        __props__.__dict__["extensions"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["last_status_change"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["location_data"] = None
        __props__.__dict__["machine_fqdn"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["os_name"] = None
        __props__.__dict__["os_profile"] = None
        __props__.__dict__["os_version"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["vm_id"] = None
        return Machine(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="agentVersion")
    def agent_version(self) -> pulumi.Output[str]:
        """
        The hybrid machine agent full version.
        """
        return pulumi.get(self, "agent_version")

    @property
    @pulumi.getter(name="clientPublicKey")
    def client_public_key(self) -> pulumi.Output[Optional[str]]:
        """
        Public Key that the client provides to be used during initial resource onboarding
        """
        return pulumi.get(self, "client_public_key")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        Specifies the hybrid machine display name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="errorDetails")
    def error_details(self) -> pulumi.Output[Sequence['outputs.ErrorDetailResponse']]:
        """
        Details about the error state.
        """
        return pulumi.get(self, "error_details")

    @property
    @pulumi.getter
    def extensions(self) -> pulumi.Output[Optional[Sequence['outputs.MachineExtensionInstanceViewResponse']]]:
        """
        Machine Extensions information
        """
        return pulumi.get(self, "extensions")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.MachineResponseIdentity']]:
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="lastStatusChange")
    def last_status_change(self) -> pulumi.Output[str]:
        """
        The time of the last status change.
        """
        return pulumi.get(self, "last_status_change")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="locationData")
    def location_data(self) -> pulumi.Output[Optional['outputs.LocationDataResponse']]:
        """
        Metadata pertaining to the geographic location of the resource.
        """
        return pulumi.get(self, "location_data")

    @property
    @pulumi.getter(name="machineFqdn")
    def machine_fqdn(self) -> pulumi.Output[str]:
        """
        Specifies the hybrid machine FQDN.
        """
        return pulumi.get(self, "machine_fqdn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="osName")
    def os_name(self) -> pulumi.Output[str]:
        """
        The Operating System running on the hybrid machine.
        """
        return pulumi.get(self, "os_name")

    @property
    @pulumi.getter(name="osProfile")
    def os_profile(self) -> pulumi.Output[Optional['outputs.MachinePropertiesResponseOsProfile']]:
        """
        Specifies the operating system settings for the hybrid machine.
        """
        return pulumi.get(self, "os_profile")

    @property
    @pulumi.getter(name="osVersion")
    def os_version(self) -> pulumi.Output[str]:
        """
        The version of Operating System running on the hybrid machine.
        """
        return pulumi.get(self, "os_version")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the hybrid machine agent.
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
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vmId")
    def vm_id(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the hybrid machine unique ID.
        """
        return pulumi.get(self, "vm_id")

