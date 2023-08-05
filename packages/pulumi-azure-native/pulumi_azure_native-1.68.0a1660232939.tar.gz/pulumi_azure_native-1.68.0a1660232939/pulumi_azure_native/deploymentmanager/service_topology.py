# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ServiceTopologyArgs', 'ServiceTopology']

@pulumi.input_type
class ServiceTopologyArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 artifact_source_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 service_topology_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ServiceTopology resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] artifact_source_id: The resource Id of the artifact source that contains the artifacts that can be referenced in the service units.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] service_topology_name: The name of the service topology .
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if artifact_source_id is not None:
            pulumi.set(__self__, "artifact_source_id", artifact_source_id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if service_topology_name is not None:
            pulumi.set(__self__, "service_topology_name", service_topology_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

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
    @pulumi.getter(name="artifactSourceId")
    def artifact_source_id(self) -> Optional[pulumi.Input[str]]:
        """
        The resource Id of the artifact source that contains the artifacts that can be referenced in the service units.
        """
        return pulumi.get(self, "artifact_source_id")

    @artifact_source_id.setter
    def artifact_source_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "artifact_source_id", value)

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
    @pulumi.getter(name="serviceTopologyName")
    def service_topology_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the service topology .
        """
        return pulumi.get(self, "service_topology_name")

    @service_topology_name.setter
    def service_topology_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_topology_name", value)

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


class ServiceTopology(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 artifact_source_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_topology_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        The resource representation of a service topology.
        API Version: 2019-11-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] artifact_source_id: The resource Id of the artifact source that contains the artifacts that can be referenced in the service units.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] service_topology_name: The name of the service topology .
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServiceTopologyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The resource representation of a service topology.
        API Version: 2019-11-01-preview.

        :param str resource_name: The name of the resource.
        :param ServiceTopologyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceTopologyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 artifact_source_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_topology_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = ServiceTopologyArgs.__new__(ServiceTopologyArgs)

            __props__.__dict__["artifact_source_id"] = artifact_source_id
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["service_topology_name"] = service_topology_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:deploymentmanager/v20180901preview:ServiceTopology"), pulumi.Alias(type_="azure-native:deploymentmanager/v20191101preview:ServiceTopology")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ServiceTopology, __self__).__init__(
            'azure-native:deploymentmanager:ServiceTopology',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ServiceTopology':
        """
        Get an existing ServiceTopology resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ServiceTopologyArgs.__new__(ServiceTopologyArgs)

        __props__.__dict__["artifact_source_id"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return ServiceTopology(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="artifactSourceId")
    def artifact_source_id(self) -> pulumi.Output[Optional[str]]:
        """
        The resource Id of the artifact source that contains the artifacts that can be referenced in the service units.
        """
        return pulumi.get(self, "artifact_source_id")

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

