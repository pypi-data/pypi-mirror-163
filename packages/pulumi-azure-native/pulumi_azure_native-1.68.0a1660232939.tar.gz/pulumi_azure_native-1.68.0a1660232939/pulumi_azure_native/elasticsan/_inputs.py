# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'NetworkRuleSetArgs',
    'SkuArgs',
    'SourceCreationDataArgs',
    'VirtualNetworkRuleArgs',
]

@pulumi.input_type
class NetworkRuleSetArgs:
    def __init__(__self__, *,
                 virtual_network_rules: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualNetworkRuleArgs']]]] = None):
        """
        A set of rules governing the network accessibility.
        :param pulumi.Input[Sequence[pulumi.Input['VirtualNetworkRuleArgs']]] virtual_network_rules: The list of virtual network rules.
        """
        if virtual_network_rules is not None:
            pulumi.set(__self__, "virtual_network_rules", virtual_network_rules)

    @property
    @pulumi.getter(name="virtualNetworkRules")
    def virtual_network_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VirtualNetworkRuleArgs']]]]:
        """
        The list of virtual network rules.
        """
        return pulumi.get(self, "virtual_network_rules")

    @virtual_network_rules.setter
    def virtual_network_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualNetworkRuleArgs']]]]):
        pulumi.set(self, "virtual_network_rules", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[Union[str, 'Name']]] = None,
                 tier: Optional[pulumi.Input[Union[str, 'Tier']]] = None):
        """
        The SKU name. Required for account creation; optional for update.
        :param pulumi.Input[Union[str, 'Name']] name: The sku name.
        :param pulumi.Input[Union[str, 'Tier']] tier: The sku tier.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[Union[str, 'Name']]]:
        """
        The sku name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[Union[str, 'Name']]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input[Union[str, 'Tier']]]:
        """
        The sku tier.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input[Union[str, 'Tier']]]):
        pulumi.set(self, "tier", value)


@pulumi.input_type
class SourceCreationDataArgs:
    def __init__(__self__, *,
                 create_source: pulumi.Input['VolumeCreateOption'],
                 source_uri: Optional[pulumi.Input[str]] = None):
        """
        Data source used when creating the volume.
        :param pulumi.Input['VolumeCreateOption'] create_source: This enumerates the possible sources of a volume creation.
        :param pulumi.Input[str] source_uri: If createOption is Copy, this is the ARM id of the source snapshot or disk. If createOption is Restore, this is the ARM-like id of the source disk restore point.
        """
        pulumi.set(__self__, "create_source", create_source)
        if source_uri is not None:
            pulumi.set(__self__, "source_uri", source_uri)

    @property
    @pulumi.getter(name="createSource")
    def create_source(self) -> pulumi.Input['VolumeCreateOption']:
        """
        This enumerates the possible sources of a volume creation.
        """
        return pulumi.get(self, "create_source")

    @create_source.setter
    def create_source(self, value: pulumi.Input['VolumeCreateOption']):
        pulumi.set(self, "create_source", value)

    @property
    @pulumi.getter(name="sourceUri")
    def source_uri(self) -> Optional[pulumi.Input[str]]:
        """
        If createOption is Copy, this is the ARM id of the source snapshot or disk. If createOption is Restore, this is the ARM-like id of the source disk restore point.
        """
        return pulumi.get(self, "source_uri")

    @source_uri.setter
    def source_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_uri", value)


@pulumi.input_type
class VirtualNetworkRuleArgs:
    def __init__(__self__, *,
                 virtual_network_resource_id: pulumi.Input[str],
                 action: Optional[pulumi.Input['Action']] = None):
        """
        Virtual Network rule.
        :param pulumi.Input[str] virtual_network_resource_id: Resource ID of a subnet, for example: /subscriptions/{subscriptionId}/resourceGroups/{groupName}/providers/Microsoft.Network/virtualNetworks/{vnetName}/subnets/{subnetName}.
        :param pulumi.Input['Action'] action: The action of virtual network rule.
        """
        pulumi.set(__self__, "virtual_network_resource_id", virtual_network_resource_id)
        if action is None:
            action = 'Allow'
        if action is not None:
            pulumi.set(__self__, "action", action)

    @property
    @pulumi.getter(name="virtualNetworkResourceId")
    def virtual_network_resource_id(self) -> pulumi.Input[str]:
        """
        Resource ID of a subnet, for example: /subscriptions/{subscriptionId}/resourceGroups/{groupName}/providers/Microsoft.Network/virtualNetworks/{vnetName}/subnets/{subnetName}.
        """
        return pulumi.get(self, "virtual_network_resource_id")

    @virtual_network_resource_id.setter
    def virtual_network_resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_network_resource_id", value)

    @property
    @pulumi.getter
    def action(self) -> Optional[pulumi.Input['Action']]:
        """
        The action of virtual network rule.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: Optional[pulumi.Input['Action']]):
        pulumi.set(self, "action", value)


