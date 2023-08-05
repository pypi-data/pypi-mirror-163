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

__all__ = ['SmartDetectorAlertRuleArgs', 'SmartDetectorAlertRule']

@pulumi.input_type
class SmartDetectorAlertRuleArgs:
    def __init__(__self__, *,
                 action_groups: pulumi.Input['ActionGroupsInformationArgs'],
                 detector: pulumi.Input['DetectorArgs'],
                 frequency: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 scope: pulumi.Input[Sequence[pulumi.Input[str]]],
                 severity: pulumi.Input[Union[str, 'Severity']],
                 state: pulumi.Input[Union[str, 'AlertRuleState']],
                 alert_rule_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 throttling: Optional[pulumi.Input['ThrottlingInformationArgs']] = None):
        """
        The set of arguments for constructing a SmartDetectorAlertRule resource.
        :param pulumi.Input['ActionGroupsInformationArgs'] action_groups: The alert rule actions.
        :param pulumi.Input['DetectorArgs'] detector: The alert rule's detector.
        :param pulumi.Input[str] frequency: The alert rule frequency in ISO8601 format. The time granularity must be in minutes and minimum value is 5 minutes.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] scope: The alert rule resources scope.
        :param pulumi.Input[Union[str, 'Severity']] severity: The alert rule severity.
        :param pulumi.Input[Union[str, 'AlertRuleState']] state: The alert rule state.
        :param pulumi.Input[str] alert_rule_name: The name of the alert rule.
        :param pulumi.Input[str] description: The alert rule description.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        :param pulumi.Input['ThrottlingInformationArgs'] throttling: The alert rule throttling information.
        """
        pulumi.set(__self__, "action_groups", action_groups)
        pulumi.set(__self__, "detector", detector)
        pulumi.set(__self__, "frequency", frequency)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "scope", scope)
        pulumi.set(__self__, "severity", severity)
        pulumi.set(__self__, "state", state)
        if alert_rule_name is not None:
            pulumi.set(__self__, "alert_rule_name", alert_rule_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if location is None:
            location = 'global'
        if location is not None:
            pulumi.set(__self__, "location", location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if throttling is not None:
            pulumi.set(__self__, "throttling", throttling)

    @property
    @pulumi.getter(name="actionGroups")
    def action_groups(self) -> pulumi.Input['ActionGroupsInformationArgs']:
        """
        The alert rule actions.
        """
        return pulumi.get(self, "action_groups")

    @action_groups.setter
    def action_groups(self, value: pulumi.Input['ActionGroupsInformationArgs']):
        pulumi.set(self, "action_groups", value)

    @property
    @pulumi.getter
    def detector(self) -> pulumi.Input['DetectorArgs']:
        """
        The alert rule's detector.
        """
        return pulumi.get(self, "detector")

    @detector.setter
    def detector(self, value: pulumi.Input['DetectorArgs']):
        pulumi.set(self, "detector", value)

    @property
    @pulumi.getter
    def frequency(self) -> pulumi.Input[str]:
        """
        The alert rule frequency in ISO8601 format. The time granularity must be in minutes and minimum value is 5 minutes.
        """
        return pulumi.get(self, "frequency")

    @frequency.setter
    def frequency(self, value: pulumi.Input[str]):
        pulumi.set(self, "frequency", value)

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
    @pulumi.getter
    def scope(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The alert rule resources scope.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def severity(self) -> pulumi.Input[Union[str, 'Severity']]:
        """
        The alert rule severity.
        """
        return pulumi.get(self, "severity")

    @severity.setter
    def severity(self, value: pulumi.Input[Union[str, 'Severity']]):
        pulumi.set(self, "severity", value)

    @property
    @pulumi.getter
    def state(self) -> pulumi.Input[Union[str, 'AlertRuleState']]:
        """
        The alert rule state.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: pulumi.Input[Union[str, 'AlertRuleState']]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter(name="alertRuleName")
    def alert_rule_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the alert rule.
        """
        return pulumi.get(self, "alert_rule_name")

    @alert_rule_name.setter
    def alert_rule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "alert_rule_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The alert rule description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def throttling(self) -> Optional[pulumi.Input['ThrottlingInformationArgs']]:
        """
        The alert rule throttling information.
        """
        return pulumi.get(self, "throttling")

    @throttling.setter
    def throttling(self, value: Optional[pulumi.Input['ThrottlingInformationArgs']]):
        pulumi.set(self, "throttling", value)


class SmartDetectorAlertRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action_groups: Optional[pulumi.Input[pulumi.InputType['ActionGroupsInformationArgs']]] = None,
                 alert_rule_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 detector: Optional[pulumi.Input[pulumi.InputType['DetectorArgs']]] = None,
                 frequency: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 severity: Optional[pulumi.Input[Union[str, 'Severity']]] = None,
                 state: Optional[pulumi.Input[Union[str, 'AlertRuleState']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 throttling: Optional[pulumi.Input[pulumi.InputType['ThrottlingInformationArgs']]] = None,
                 __props__=None):
        """
        The alert rule information

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ActionGroupsInformationArgs']] action_groups: The alert rule actions.
        :param pulumi.Input[str] alert_rule_name: The name of the alert rule.
        :param pulumi.Input[str] description: The alert rule description.
        :param pulumi.Input[pulumi.InputType['DetectorArgs']] detector: The alert rule's detector.
        :param pulumi.Input[str] frequency: The alert rule frequency in ISO8601 format. The time granularity must be in minutes and minimum value is 5 minutes.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] scope: The alert rule resources scope.
        :param pulumi.Input[Union[str, 'Severity']] severity: The alert rule severity.
        :param pulumi.Input[Union[str, 'AlertRuleState']] state: The alert rule state.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        :param pulumi.Input[pulumi.InputType['ThrottlingInformationArgs']] throttling: The alert rule throttling information.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SmartDetectorAlertRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The alert rule information

        :param str resource_name: The name of the resource.
        :param SmartDetectorAlertRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SmartDetectorAlertRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action_groups: Optional[pulumi.Input[pulumi.InputType['ActionGroupsInformationArgs']]] = None,
                 alert_rule_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 detector: Optional[pulumi.Input[pulumi.InputType['DetectorArgs']]] = None,
                 frequency: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 severity: Optional[pulumi.Input[Union[str, 'Severity']]] = None,
                 state: Optional[pulumi.Input[Union[str, 'AlertRuleState']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 throttling: Optional[pulumi.Input[pulumi.InputType['ThrottlingInformationArgs']]] = None,
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
            __props__ = SmartDetectorAlertRuleArgs.__new__(SmartDetectorAlertRuleArgs)

            if action_groups is None and not opts.urn:
                raise TypeError("Missing required property 'action_groups'")
            __props__.__dict__["action_groups"] = action_groups
            __props__.__dict__["alert_rule_name"] = alert_rule_name
            __props__.__dict__["description"] = description
            if detector is None and not opts.urn:
                raise TypeError("Missing required property 'detector'")
            __props__.__dict__["detector"] = detector
            if frequency is None and not opts.urn:
                raise TypeError("Missing required property 'frequency'")
            __props__.__dict__["frequency"] = frequency
            if location is None:
                location = 'global'
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__.__dict__["scope"] = scope
            if severity is None and not opts.urn:
                raise TypeError("Missing required property 'severity'")
            __props__.__dict__["severity"] = severity
            if state is None and not opts.urn:
                raise TypeError("Missing required property 'state'")
            __props__.__dict__["state"] = state
            __props__.__dict__["tags"] = tags
            __props__.__dict__["throttling"] = throttling
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:alertsmanagement:SmartDetectorAlertRule"), pulumi.Alias(type_="azure-native:alertsmanagement/v20190301:SmartDetectorAlertRule"), pulumi.Alias(type_="azure-native:alertsmanagement/v20210401:SmartDetectorAlertRule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SmartDetectorAlertRule, __self__).__init__(
            'azure-native:alertsmanagement/v20190601:SmartDetectorAlertRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SmartDetectorAlertRule':
        """
        Get an existing SmartDetectorAlertRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SmartDetectorAlertRuleArgs.__new__(SmartDetectorAlertRuleArgs)

        __props__.__dict__["action_groups"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["detector"] = None
        __props__.__dict__["frequency"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["scope"] = None
        __props__.__dict__["severity"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["throttling"] = None
        __props__.__dict__["type"] = None
        return SmartDetectorAlertRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="actionGroups")
    def action_groups(self) -> pulumi.Output['outputs.ActionGroupsInformationResponse']:
        """
        The alert rule actions.
        """
        return pulumi.get(self, "action_groups")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The alert rule description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def detector(self) -> pulumi.Output['outputs.DetectorResponse']:
        """
        The alert rule's detector.
        """
        return pulumi.get(self, "detector")

    @property
    @pulumi.getter
    def frequency(self) -> pulumi.Output[str]:
        """
        The alert rule frequency in ISO8601 format. The time granularity must be in minutes and minimum value is 5 minutes.
        """
        return pulumi.get(self, "frequency")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Output[Sequence[str]]:
        """
        The alert rule resources scope.
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def severity(self) -> pulumi.Output[str]:
        """
        The alert rule severity.
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The alert rule state.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def throttling(self) -> pulumi.Output[Optional['outputs.ThrottlingInformationResponse']]:
        """
        The alert rule throttling information.
        """
        return pulumi.get(self, "throttling")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

