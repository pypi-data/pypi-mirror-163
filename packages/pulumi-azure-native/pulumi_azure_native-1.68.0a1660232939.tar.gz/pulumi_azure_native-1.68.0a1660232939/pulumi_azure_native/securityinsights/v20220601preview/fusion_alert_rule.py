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

__all__ = ['FusionAlertRuleArgs', 'FusionAlertRule']

@pulumi.input_type
class FusionAlertRuleArgs:
    def __init__(__self__, *,
                 alert_rule_template_name: pulumi.Input[str],
                 enabled: pulumi.Input[bool],
                 kind: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 workspace_name: pulumi.Input[str],
                 rule_id: Optional[pulumi.Input[str]] = None,
                 scenario_exclusion_patterns: Optional[pulumi.Input[Sequence[pulumi.Input['FusionScenarioExclusionPatternArgs']]]] = None,
                 source_settings: Optional[pulumi.Input[Sequence[pulumi.Input['FusionSourceSettingsArgs']]]] = None):
        """
        The set of arguments for constructing a FusionAlertRule resource.
        :param pulumi.Input[str] alert_rule_template_name: The Name of the alert rule template used to create this rule.
        :param pulumi.Input[bool] enabled: Determines whether this alert rule is enabled or disabled.
        :param pulumi.Input[str] kind: The kind of the alert rule
               Expected value is 'Fusion'.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        :param pulumi.Input[str] rule_id: Alert rule ID
        :param pulumi.Input[Sequence[pulumi.Input['FusionScenarioExclusionPatternArgs']]] scenario_exclusion_patterns: Configuration to exclude scenarios in fusion detection.
        :param pulumi.Input[Sequence[pulumi.Input['FusionSourceSettingsArgs']]] source_settings: Configuration for all supported source signals in fusion detection.
        """
        pulumi.set(__self__, "alert_rule_template_name", alert_rule_template_name)
        pulumi.set(__self__, "enabled", enabled)
        pulumi.set(__self__, "kind", 'Fusion')
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "workspace_name", workspace_name)
        if rule_id is not None:
            pulumi.set(__self__, "rule_id", rule_id)
        if scenario_exclusion_patterns is not None:
            pulumi.set(__self__, "scenario_exclusion_patterns", scenario_exclusion_patterns)
        if source_settings is not None:
            pulumi.set(__self__, "source_settings", source_settings)

    @property
    @pulumi.getter(name="alertRuleTemplateName")
    def alert_rule_template_name(self) -> pulumi.Input[str]:
        """
        The Name of the alert rule template used to create this rule.
        """
        return pulumi.get(self, "alert_rule_template_name")

    @alert_rule_template_name.setter
    def alert_rule_template_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "alert_rule_template_name", value)

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Input[bool]:
        """
        Determines whether this alert rule is enabled or disabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[str]:
        """
        The kind of the alert rule
        Expected value is 'Fusion'.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: pulumi.Input[str]):
        pulumi.set(self, "kind", value)

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
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> pulumi.Input[str]:
        """
        The name of the workspace.
        """
        return pulumi.get(self, "workspace_name")

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_name", value)

    @property
    @pulumi.getter(name="ruleId")
    def rule_id(self) -> Optional[pulumi.Input[str]]:
        """
        Alert rule ID
        """
        return pulumi.get(self, "rule_id")

    @rule_id.setter
    def rule_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rule_id", value)

    @property
    @pulumi.getter(name="scenarioExclusionPatterns")
    def scenario_exclusion_patterns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FusionScenarioExclusionPatternArgs']]]]:
        """
        Configuration to exclude scenarios in fusion detection.
        """
        return pulumi.get(self, "scenario_exclusion_patterns")

    @scenario_exclusion_patterns.setter
    def scenario_exclusion_patterns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FusionScenarioExclusionPatternArgs']]]]):
        pulumi.set(self, "scenario_exclusion_patterns", value)

    @property
    @pulumi.getter(name="sourceSettings")
    def source_settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FusionSourceSettingsArgs']]]]:
        """
        Configuration for all supported source signals in fusion detection.
        """
        return pulumi.get(self, "source_settings")

    @source_settings.setter
    def source_settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FusionSourceSettingsArgs']]]]):
        pulumi.set(self, "source_settings", value)


class FusionAlertRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 alert_rule_template_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rule_id: Optional[pulumi.Input[str]] = None,
                 scenario_exclusion_patterns: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FusionScenarioExclusionPatternArgs']]]]] = None,
                 source_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FusionSourceSettingsArgs']]]]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Represents Fusion alert rule.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] alert_rule_template_name: The Name of the alert rule template used to create this rule.
        :param pulumi.Input[bool] enabled: Determines whether this alert rule is enabled or disabled.
        :param pulumi.Input[str] kind: The kind of the alert rule
               Expected value is 'Fusion'.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] rule_id: Alert rule ID
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FusionScenarioExclusionPatternArgs']]]] scenario_exclusion_patterns: Configuration to exclude scenarios in fusion detection.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FusionSourceSettingsArgs']]]] source_settings: Configuration for all supported source signals in fusion detection.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FusionAlertRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents Fusion alert rule.

        :param str resource_name: The name of the resource.
        :param FusionAlertRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FusionAlertRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 alert_rule_template_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rule_id: Optional[pulumi.Input[str]] = None,
                 scenario_exclusion_patterns: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FusionScenarioExclusionPatternArgs']]]]] = None,
                 source_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FusionSourceSettingsArgs']]]]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = FusionAlertRuleArgs.__new__(FusionAlertRuleArgs)

            if alert_rule_template_name is None and not opts.urn:
                raise TypeError("Missing required property 'alert_rule_template_name'")
            __props__.__dict__["alert_rule_template_name"] = alert_rule_template_name
            if enabled is None and not opts.urn:
                raise TypeError("Missing required property 'enabled'")
            __props__.__dict__["enabled"] = enabled
            if kind is None and not opts.urn:
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__["kind"] = 'Fusion'
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["rule_id"] = rule_id
            __props__.__dict__["scenario_exclusion_patterns"] = scenario_exclusion_patterns
            __props__.__dict__["source_settings"] = source_settings
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__["workspace_name"] = workspace_name
            __props__.__dict__["description"] = None
            __props__.__dict__["display_name"] = None
            __props__.__dict__["etag"] = None
            __props__.__dict__["last_modified_utc"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["severity"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["tactics"] = None
            __props__.__dict__["techniques"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:securityinsights:FusionAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20190101preview:FusionAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20200101:FusionAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20210301preview:FusionAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20210901preview:FusionAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20211001:FusionAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20211001preview:FusionAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20220101preview:FusionAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20220401preview:FusionAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20220501preview:FusionAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20220701preview:FusionAlertRule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(FusionAlertRule, __self__).__init__(
            'azure-native:securityinsights/v20220601preview:FusionAlertRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'FusionAlertRule':
        """
        Get an existing FusionAlertRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = FusionAlertRuleArgs.__new__(FusionAlertRuleArgs)

        __props__.__dict__["alert_rule_template_name"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["enabled"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["last_modified_utc"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["scenario_exclusion_patterns"] = None
        __props__.__dict__["severity"] = None
        __props__.__dict__["source_settings"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tactics"] = None
        __props__.__dict__["techniques"] = None
        __props__.__dict__["type"] = None
        return FusionAlertRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="alertRuleTemplateName")
    def alert_rule_template_name(self) -> pulumi.Output[str]:
        """
        The Name of the alert rule template used to create this rule.
        """
        return pulumi.get(self, "alert_rule_template_name")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        The description of the alert rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The display name for alerts created by this alert rule.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[bool]:
        """
        Determines whether this alert rule is enabled or disabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        The kind of the alert rule
        Expected value is 'Fusion'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastModifiedUtc")
    def last_modified_utc(self) -> pulumi.Output[str]:
        """
        The last time that this alert has been modified.
        """
        return pulumi.get(self, "last_modified_utc")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="scenarioExclusionPatterns")
    def scenario_exclusion_patterns(self) -> pulumi.Output[Optional[Sequence['outputs.FusionScenarioExclusionPatternResponse']]]:
        """
        Configuration to exclude scenarios in fusion detection.
        """
        return pulumi.get(self, "scenario_exclusion_patterns")

    @property
    @pulumi.getter
    def severity(self) -> pulumi.Output[str]:
        """
        The severity for alerts created by this alert rule.
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter(name="sourceSettings")
    def source_settings(self) -> pulumi.Output[Optional[Sequence['outputs.FusionSourceSettingsResponse']]]:
        """
        Configuration for all supported source signals in fusion detection.
        """
        return pulumi.get(self, "source_settings")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tactics(self) -> pulumi.Output[Sequence[str]]:
        """
        The tactics of the alert rule
        """
        return pulumi.get(self, "tactics")

    @property
    @pulumi.getter
    def techniques(self) -> pulumi.Output[Sequence[str]]:
        """
        The techniques of the alert rule
        """
        return pulumi.get(self, "techniques")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

