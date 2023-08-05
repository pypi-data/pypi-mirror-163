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

__all__ = ['ProtectedItemArgs', 'ProtectedItem']

@pulumi.input_type
class ProtectedItemArgs:
    def __init__(__self__, *,
                 container_name: pulumi.Input[str],
                 fabric_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 vault_name: pulumi.Input[str],
                 e_tag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Union['AzureFileshareProtectedItemArgs', 'AzureIaaSClassicComputeVMProtectedItemArgs', 'AzureIaaSComputeVMProtectedItemArgs', 'AzureIaaSVMProtectedItemArgs', 'AzureSqlProtectedItemArgs', 'AzureVmWorkloadProtectedItemArgs', 'AzureVmWorkloadSAPAseDatabaseProtectedItemArgs', 'AzureVmWorkloadSAPHanaDatabaseProtectedItemArgs', 'AzureVmWorkloadSQLDatabaseProtectedItemArgs', 'DPMProtectedItemArgs', 'GenericProtectedItemArgs', 'MabFileFolderProtectedItemArgs']]] = None,
                 protected_item_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ProtectedItem resource.
        :param pulumi.Input[str] container_name: Container name associated with the backup item.
        :param pulumi.Input[str] fabric_name: Fabric name associated with the backup item.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the recovery services vault is present.
        :param pulumi.Input[str] vault_name: The name of the recovery services vault.
        :param pulumi.Input[str] e_tag: Optional ETag.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Union['AzureFileshareProtectedItemArgs', 'AzureIaaSClassicComputeVMProtectedItemArgs', 'AzureIaaSComputeVMProtectedItemArgs', 'AzureIaaSVMProtectedItemArgs', 'AzureSqlProtectedItemArgs', 'AzureVmWorkloadProtectedItemArgs', 'AzureVmWorkloadSAPAseDatabaseProtectedItemArgs', 'AzureVmWorkloadSAPHanaDatabaseProtectedItemArgs', 'AzureVmWorkloadSQLDatabaseProtectedItemArgs', 'DPMProtectedItemArgs', 'GenericProtectedItemArgs', 'MabFileFolderProtectedItemArgs']] properties: ProtectedItemResource properties
        :param pulumi.Input[str] protected_item_name: Item name to be backed up.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "container_name", container_name)
        pulumi.set(__self__, "fabric_name", fabric_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "vault_name", vault_name)
        if e_tag is not None:
            pulumi.set(__self__, "e_tag", e_tag)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if protected_item_name is not None:
            pulumi.set(__self__, "protected_item_name", protected_item_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="containerName")
    def container_name(self) -> pulumi.Input[str]:
        """
        Container name associated with the backup item.
        """
        return pulumi.get(self, "container_name")

    @container_name.setter
    def container_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "container_name", value)

    @property
    @pulumi.getter(name="fabricName")
    def fabric_name(self) -> pulumi.Input[str]:
        """
        Fabric name associated with the backup item.
        """
        return pulumi.get(self, "fabric_name")

    @fabric_name.setter
    def fabric_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "fabric_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group where the recovery services vault is present.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="vaultName")
    def vault_name(self) -> pulumi.Input[str]:
        """
        The name of the recovery services vault.
        """
        return pulumi.get(self, "vault_name")

    @vault_name.setter
    def vault_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "vault_name", value)

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> Optional[pulumi.Input[str]]:
        """
        Optional ETag.
        """
        return pulumi.get(self, "e_tag")

    @e_tag.setter
    def e_tag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "e_tag", value)

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
    def properties(self) -> Optional[pulumi.Input[Union['AzureFileshareProtectedItemArgs', 'AzureIaaSClassicComputeVMProtectedItemArgs', 'AzureIaaSComputeVMProtectedItemArgs', 'AzureIaaSVMProtectedItemArgs', 'AzureSqlProtectedItemArgs', 'AzureVmWorkloadProtectedItemArgs', 'AzureVmWorkloadSAPAseDatabaseProtectedItemArgs', 'AzureVmWorkloadSAPHanaDatabaseProtectedItemArgs', 'AzureVmWorkloadSQLDatabaseProtectedItemArgs', 'DPMProtectedItemArgs', 'GenericProtectedItemArgs', 'MabFileFolderProtectedItemArgs']]]:
        """
        ProtectedItemResource properties
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input[Union['AzureFileshareProtectedItemArgs', 'AzureIaaSClassicComputeVMProtectedItemArgs', 'AzureIaaSComputeVMProtectedItemArgs', 'AzureIaaSVMProtectedItemArgs', 'AzureSqlProtectedItemArgs', 'AzureVmWorkloadProtectedItemArgs', 'AzureVmWorkloadSAPAseDatabaseProtectedItemArgs', 'AzureVmWorkloadSAPHanaDatabaseProtectedItemArgs', 'AzureVmWorkloadSQLDatabaseProtectedItemArgs', 'DPMProtectedItemArgs', 'GenericProtectedItemArgs', 'MabFileFolderProtectedItemArgs']]]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="protectedItemName")
    def protected_item_name(self) -> Optional[pulumi.Input[str]]:
        """
        Item name to be backed up.
        """
        return pulumi.get(self, "protected_item_name")

    @protected_item_name.setter
    def protected_item_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protected_item_name", value)

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


class ProtectedItem(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 container_name: Optional[pulumi.Input[str]] = None,
                 e_tag: Optional[pulumi.Input[str]] = None,
                 fabric_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Union[pulumi.InputType['AzureFileshareProtectedItemArgs'], pulumi.InputType['AzureIaaSClassicComputeVMProtectedItemArgs'], pulumi.InputType['AzureIaaSComputeVMProtectedItemArgs'], pulumi.InputType['AzureIaaSVMProtectedItemArgs'], pulumi.InputType['AzureSqlProtectedItemArgs'], pulumi.InputType['AzureVmWorkloadProtectedItemArgs'], pulumi.InputType['AzureVmWorkloadSAPAseDatabaseProtectedItemArgs'], pulumi.InputType['AzureVmWorkloadSAPHanaDatabaseProtectedItemArgs'], pulumi.InputType['AzureVmWorkloadSQLDatabaseProtectedItemArgs'], pulumi.InputType['DPMProtectedItemArgs'], pulumi.InputType['GenericProtectedItemArgs'], pulumi.InputType['MabFileFolderProtectedItemArgs']]]] = None,
                 protected_item_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vault_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Base class for backup items.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] container_name: Container name associated with the backup item.
        :param pulumi.Input[str] e_tag: Optional ETag.
        :param pulumi.Input[str] fabric_name: Fabric name associated with the backup item.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Union[pulumi.InputType['AzureFileshareProtectedItemArgs'], pulumi.InputType['AzureIaaSClassicComputeVMProtectedItemArgs'], pulumi.InputType['AzureIaaSComputeVMProtectedItemArgs'], pulumi.InputType['AzureIaaSVMProtectedItemArgs'], pulumi.InputType['AzureSqlProtectedItemArgs'], pulumi.InputType['AzureVmWorkloadProtectedItemArgs'], pulumi.InputType['AzureVmWorkloadSAPAseDatabaseProtectedItemArgs'], pulumi.InputType['AzureVmWorkloadSAPHanaDatabaseProtectedItemArgs'], pulumi.InputType['AzureVmWorkloadSQLDatabaseProtectedItemArgs'], pulumi.InputType['DPMProtectedItemArgs'], pulumi.InputType['GenericProtectedItemArgs'], pulumi.InputType['MabFileFolderProtectedItemArgs']]] properties: ProtectedItemResource properties
        :param pulumi.Input[str] protected_item_name: Item name to be backed up.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the recovery services vault is present.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] vault_name: The name of the recovery services vault.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ProtectedItemArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Base class for backup items.

        :param str resource_name: The name of the resource.
        :param ProtectedItemArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProtectedItemArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 container_name: Optional[pulumi.Input[str]] = None,
                 e_tag: Optional[pulumi.Input[str]] = None,
                 fabric_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Union[pulumi.InputType['AzureFileshareProtectedItemArgs'], pulumi.InputType['AzureIaaSClassicComputeVMProtectedItemArgs'], pulumi.InputType['AzureIaaSComputeVMProtectedItemArgs'], pulumi.InputType['AzureIaaSVMProtectedItemArgs'], pulumi.InputType['AzureSqlProtectedItemArgs'], pulumi.InputType['AzureVmWorkloadProtectedItemArgs'], pulumi.InputType['AzureVmWorkloadSAPAseDatabaseProtectedItemArgs'], pulumi.InputType['AzureVmWorkloadSAPHanaDatabaseProtectedItemArgs'], pulumi.InputType['AzureVmWorkloadSQLDatabaseProtectedItemArgs'], pulumi.InputType['DPMProtectedItemArgs'], pulumi.InputType['GenericProtectedItemArgs'], pulumi.InputType['MabFileFolderProtectedItemArgs']]]] = None,
                 protected_item_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vault_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = ProtectedItemArgs.__new__(ProtectedItemArgs)

            if container_name is None and not opts.urn:
                raise TypeError("Missing required property 'container_name'")
            __props__.__dict__["container_name"] = container_name
            __props__.__dict__["e_tag"] = e_tag
            if fabric_name is None and not opts.urn:
                raise TypeError("Missing required property 'fabric_name'")
            __props__.__dict__["fabric_name"] = fabric_name
            __props__.__dict__["location"] = location
            __props__.__dict__["properties"] = properties
            __props__.__dict__["protected_item_name"] = protected_item_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            if vault_name is None and not opts.urn:
                raise TypeError("Missing required property 'vault_name'")
            __props__.__dict__["vault_name"] = vault_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:recoveryservices:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20160601:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20190513:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20190615:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20201001:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20201201:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20210101:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20210201:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20210201preview:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20210210:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20210301:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20210401:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20210701:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20210801:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20211001:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20211201:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20220101:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20220201:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20220301:ProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20220601preview:ProtectedItem")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ProtectedItem, __self__).__init__(
            'azure-native:recoveryservices/v20210601:ProtectedItem',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ProtectedItem':
        """
        Get an existing ProtectedItem resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ProtectedItemArgs.__new__(ProtectedItemArgs)

        __props__.__dict__["e_tag"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return ProtectedItem(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> pulumi.Output[Optional[str]]:
        """
        Optional ETag.
        """
        return pulumi.get(self, "e_tag")

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
        Resource name associated with the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output[Any]:
        """
        ProtectedItemResource properties
        """
        return pulumi.get(self, "properties")

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
        Resource type represents the complete path of the form Namespace/ResourceType/ResourceType/...
        """
        return pulumi.get(self, "type")

