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
    'ActionGroupsInformationArgs',
    'ActionGroupArgs',
    'ConditionsArgs',
    'ConditionArgs',
    'DetectorArgs',
    'DiagnosticsArgs',
    'ScopeArgs',
    'SuppressionConfigArgs',
    'SuppressionScheduleArgs',
    'SuppressionArgs',
    'ThrottlingInformationArgs',
]

@pulumi.input_type
class ActionGroupsInformationArgs:
    def __init__(__self__, *,
                 group_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 custom_email_subject: Optional[pulumi.Input[str]] = None,
                 custom_webhook_payload: Optional[pulumi.Input[str]] = None):
        """
        The Action Groups information, used by the alert rule.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] group_ids: The Action Group resource IDs.
        :param pulumi.Input[str] custom_email_subject: An optional custom email subject to use in email notifications.
        :param pulumi.Input[str] custom_webhook_payload: An optional custom web-hook payload to use in web-hook notifications.
        """
        pulumi.set(__self__, "group_ids", group_ids)
        if custom_email_subject is not None:
            pulumi.set(__self__, "custom_email_subject", custom_email_subject)
        if custom_webhook_payload is not None:
            pulumi.set(__self__, "custom_webhook_payload", custom_webhook_payload)

    @property
    @pulumi.getter(name="groupIds")
    def group_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The Action Group resource IDs.
        """
        return pulumi.get(self, "group_ids")

    @group_ids.setter
    def group_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "group_ids", value)

    @property
    @pulumi.getter(name="customEmailSubject")
    def custom_email_subject(self) -> Optional[pulumi.Input[str]]:
        """
        An optional custom email subject to use in email notifications.
        """
        return pulumi.get(self, "custom_email_subject")

    @custom_email_subject.setter
    def custom_email_subject(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_email_subject", value)

    @property
    @pulumi.getter(name="customWebhookPayload")
    def custom_webhook_payload(self) -> Optional[pulumi.Input[str]]:
        """
        An optional custom web-hook payload to use in web-hook notifications.
        """
        return pulumi.get(self, "custom_webhook_payload")

    @custom_webhook_payload.setter
    def custom_webhook_payload(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_webhook_payload", value)


@pulumi.input_type
class ActionGroupArgs:
    def __init__(__self__, *,
                 action_group_id: pulumi.Input[str],
                 type: pulumi.Input[str],
                 conditions: Optional[pulumi.Input['ConditionsArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input['ScopeArgs']] = None,
                 status: Optional[pulumi.Input[Union[str, 'ActionRuleStatus']]] = None):
        """
        Action rule with action group configuration
        :param pulumi.Input[str] action_group_id: Action group to trigger if action rule matches
        :param pulumi.Input[str] type: Indicates type of action rule
               Expected value is 'ActionGroup'.
        :param pulumi.Input['ConditionsArgs'] conditions: conditions on which alerts will be filtered
        :param pulumi.Input[str] description: Description of action rule
        :param pulumi.Input['ScopeArgs'] scope: scope on which action rule will apply
        :param pulumi.Input[Union[str, 'ActionRuleStatus']] status: Indicates if the given action rule is enabled or disabled
        """
        pulumi.set(__self__, "action_group_id", action_group_id)
        pulumi.set(__self__, "type", 'ActionGroup')
        if conditions is not None:
            pulumi.set(__self__, "conditions", conditions)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if scope is not None:
            pulumi.set(__self__, "scope", scope)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionGroupId")
    def action_group_id(self) -> pulumi.Input[str]:
        """
        Action group to trigger if action rule matches
        """
        return pulumi.get(self, "action_group_id")

    @action_group_id.setter
    def action_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "action_group_id", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Indicates type of action rule
        Expected value is 'ActionGroup'.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def conditions(self) -> Optional[pulumi.Input['ConditionsArgs']]:
        """
        conditions on which alerts will be filtered
        """
        return pulumi.get(self, "conditions")

    @conditions.setter
    def conditions(self, value: Optional[pulumi.Input['ConditionsArgs']]):
        pulumi.set(self, "conditions", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of action rule
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def scope(self) -> Optional[pulumi.Input['ScopeArgs']]:
        """
        scope on which action rule will apply
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: Optional[pulumi.Input['ScopeArgs']]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'ActionRuleStatus']]]:
        """
        Indicates if the given action rule is enabled or disabled
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'ActionRuleStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class ConditionsArgs:
    def __init__(__self__, *,
                 alert_context: Optional[pulumi.Input['ConditionArgs']] = None,
                 alert_rule_id: Optional[pulumi.Input['ConditionArgs']] = None,
                 description: Optional[pulumi.Input['ConditionArgs']] = None,
                 monitor_condition: Optional[pulumi.Input['ConditionArgs']] = None,
                 monitor_service: Optional[pulumi.Input['ConditionArgs']] = None,
                 severity: Optional[pulumi.Input['ConditionArgs']] = None,
                 target_resource_type: Optional[pulumi.Input['ConditionArgs']] = None):
        """
        Conditions in alert instance to be matched for a given action rule. Default value is all. Multiple values could be provided with comma separation.
        :param pulumi.Input['ConditionArgs'] alert_context: filter alerts by alert context (payload)
        :param pulumi.Input['ConditionArgs'] alert_rule_id: filter alerts by alert rule id
        :param pulumi.Input['ConditionArgs'] description: filter alerts by alert rule description
        :param pulumi.Input['ConditionArgs'] monitor_condition: filter alerts by monitor condition
        :param pulumi.Input['ConditionArgs'] monitor_service: filter alerts by monitor service
        :param pulumi.Input['ConditionArgs'] severity: filter alerts by severity
        :param pulumi.Input['ConditionArgs'] target_resource_type: filter alerts by target resource type
        """
        if alert_context is not None:
            pulumi.set(__self__, "alert_context", alert_context)
        if alert_rule_id is not None:
            pulumi.set(__self__, "alert_rule_id", alert_rule_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if monitor_condition is not None:
            pulumi.set(__self__, "monitor_condition", monitor_condition)
        if monitor_service is not None:
            pulumi.set(__self__, "monitor_service", monitor_service)
        if severity is not None:
            pulumi.set(__self__, "severity", severity)
        if target_resource_type is not None:
            pulumi.set(__self__, "target_resource_type", target_resource_type)

    @property
    @pulumi.getter(name="alertContext")
    def alert_context(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        filter alerts by alert context (payload)
        """
        return pulumi.get(self, "alert_context")

    @alert_context.setter
    def alert_context(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "alert_context", value)

    @property
    @pulumi.getter(name="alertRuleId")
    def alert_rule_id(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        filter alerts by alert rule id
        """
        return pulumi.get(self, "alert_rule_id")

    @alert_rule_id.setter
    def alert_rule_id(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "alert_rule_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        filter alerts by alert rule description
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="monitorCondition")
    def monitor_condition(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        filter alerts by monitor condition
        """
        return pulumi.get(self, "monitor_condition")

    @monitor_condition.setter
    def monitor_condition(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "monitor_condition", value)

    @property
    @pulumi.getter(name="monitorService")
    def monitor_service(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        filter alerts by monitor service
        """
        return pulumi.get(self, "monitor_service")

    @monitor_service.setter
    def monitor_service(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "monitor_service", value)

    @property
    @pulumi.getter
    def severity(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        filter alerts by severity
        """
        return pulumi.get(self, "severity")

    @severity.setter
    def severity(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "severity", value)

    @property
    @pulumi.getter(name="targetResourceType")
    def target_resource_type(self) -> Optional[pulumi.Input['ConditionArgs']]:
        """
        filter alerts by target resource type
        """
        return pulumi.get(self, "target_resource_type")

    @target_resource_type.setter
    def target_resource_type(self, value: Optional[pulumi.Input['ConditionArgs']]):
        pulumi.set(self, "target_resource_type", value)


@pulumi.input_type
class ConditionArgs:
    def __init__(__self__, *,
                 operator: Optional[pulumi.Input[Union[str, 'Operator']]] = None,
                 values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        condition to trigger an action rule
        :param pulumi.Input[Union[str, 'Operator']] operator: operator for a given condition
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: list of values to match for a given condition.
        """
        if operator is not None:
            pulumi.set(__self__, "operator", operator)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def operator(self) -> Optional[pulumi.Input[Union[str, 'Operator']]]:
        """
        operator for a given condition
        """
        return pulumi.get(self, "operator")

    @operator.setter
    def operator(self, value: Optional[pulumi.Input[Union[str, 'Operator']]]):
        pulumi.set(self, "operator", value)

    @property
    @pulumi.getter
    def values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        list of values to match for a given condition.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class DetectorArgs:
    def __init__(__self__, *,
                 id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 image_paths: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 supported_resource_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The detector information. By default this is not populated, unless it's specified in expandDetector
        :param pulumi.Input[str] id: The detector id.
        :param pulumi.Input[str] description: The Smart Detector description. By default this is not populated, unless it's specified in expandDetector
        :param pulumi.Input[Sequence[pulumi.Input[str]]] image_paths: The Smart Detector image path. By default this is not populated, unless it's specified in expandDetector
        :param pulumi.Input[str] name: The Smart Detector name. By default this is not populated, unless it's specified in expandDetector
        :param pulumi.Input[Mapping[str, Any]] parameters: The detector's parameters.'
        :param pulumi.Input[Sequence[pulumi.Input[str]]] supported_resource_types: The Smart Detector supported resource types. By default this is not populated, unless it's specified in expandDetector
        """
        pulumi.set(__self__, "id", id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if image_paths is not None:
            pulumi.set(__self__, "image_paths", image_paths)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if supported_resource_types is not None:
            pulumi.set(__self__, "supported_resource_types", supported_resource_types)

    @property
    @pulumi.getter
    def id(self) -> pulumi.Input[str]:
        """
        The detector id.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: pulumi.Input[str]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The Smart Detector description. By default this is not populated, unless it's specified in expandDetector
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="imagePaths")
    def image_paths(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The Smart Detector image path. By default this is not populated, unless it's specified in expandDetector
        """
        return pulumi.get(self, "image_paths")

    @image_paths.setter
    def image_paths(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "image_paths", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The Smart Detector name. By default this is not populated, unless it's specified in expandDetector
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        The detector's parameters.'
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter(name="supportedResourceTypes")
    def supported_resource_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The Smart Detector supported resource types. By default this is not populated, unless it's specified in expandDetector
        """
        return pulumi.get(self, "supported_resource_types")

    @supported_resource_types.setter
    def supported_resource_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "supported_resource_types", value)


@pulumi.input_type
class DiagnosticsArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 conditions: Optional[pulumi.Input['ConditionsArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input['ScopeArgs']] = None,
                 status: Optional[pulumi.Input[Union[str, 'ActionRuleStatus']]] = None):
        """
        Action rule with diagnostics configuration
        :param pulumi.Input[str] type: Indicates type of action rule
               Expected value is 'Diagnostics'.
        :param pulumi.Input['ConditionsArgs'] conditions: conditions on which alerts will be filtered
        :param pulumi.Input[str] description: Description of action rule
        :param pulumi.Input['ScopeArgs'] scope: scope on which action rule will apply
        :param pulumi.Input[Union[str, 'ActionRuleStatus']] status: Indicates if the given action rule is enabled or disabled
        """
        pulumi.set(__self__, "type", 'Diagnostics')
        if conditions is not None:
            pulumi.set(__self__, "conditions", conditions)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if scope is not None:
            pulumi.set(__self__, "scope", scope)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Indicates type of action rule
        Expected value is 'Diagnostics'.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def conditions(self) -> Optional[pulumi.Input['ConditionsArgs']]:
        """
        conditions on which alerts will be filtered
        """
        return pulumi.get(self, "conditions")

    @conditions.setter
    def conditions(self, value: Optional[pulumi.Input['ConditionsArgs']]):
        pulumi.set(self, "conditions", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of action rule
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def scope(self) -> Optional[pulumi.Input['ScopeArgs']]:
        """
        scope on which action rule will apply
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: Optional[pulumi.Input['ScopeArgs']]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'ActionRuleStatus']]]:
        """
        Indicates if the given action rule is enabled or disabled
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'ActionRuleStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class ScopeArgs:
    def __init__(__self__, *,
                 scope_type: Optional[pulumi.Input[Union[str, 'ScopeType']]] = None,
                 values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Target scope for a given action rule. By default scope will be the subscription. User can also provide list of resource groups or list of resources from the scope subscription as well.
        :param pulumi.Input[Union[str, 'ScopeType']] scope_type: type of target scope
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: list of ARM IDs of the given scope type which will be the target of the given action rule.
        """
        if scope_type is not None:
            pulumi.set(__self__, "scope_type", scope_type)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter(name="scopeType")
    def scope_type(self) -> Optional[pulumi.Input[Union[str, 'ScopeType']]]:
        """
        type of target scope
        """
        return pulumi.get(self, "scope_type")

    @scope_type.setter
    def scope_type(self, value: Optional[pulumi.Input[Union[str, 'ScopeType']]]):
        pulumi.set(self, "scope_type", value)

    @property
    @pulumi.getter
    def values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        list of ARM IDs of the given scope type which will be the target of the given action rule.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class SuppressionConfigArgs:
    def __init__(__self__, *,
                 recurrence_type: pulumi.Input[Union[str, 'SuppressionType']],
                 schedule: Optional[pulumi.Input['SuppressionScheduleArgs']] = None):
        """
        Suppression logic for a given action rule
        :param pulumi.Input[Union[str, 'SuppressionType']] recurrence_type: Specifies when the suppression should be applied
        :param pulumi.Input['SuppressionScheduleArgs'] schedule: suppression schedule configuration
        """
        pulumi.set(__self__, "recurrence_type", recurrence_type)
        if schedule is not None:
            pulumi.set(__self__, "schedule", schedule)

    @property
    @pulumi.getter(name="recurrenceType")
    def recurrence_type(self) -> pulumi.Input[Union[str, 'SuppressionType']]:
        """
        Specifies when the suppression should be applied
        """
        return pulumi.get(self, "recurrence_type")

    @recurrence_type.setter
    def recurrence_type(self, value: pulumi.Input[Union[str, 'SuppressionType']]):
        pulumi.set(self, "recurrence_type", value)

    @property
    @pulumi.getter
    def schedule(self) -> Optional[pulumi.Input['SuppressionScheduleArgs']]:
        """
        suppression schedule configuration
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: Optional[pulumi.Input['SuppressionScheduleArgs']]):
        pulumi.set(self, "schedule", value)


@pulumi.input_type
class SuppressionScheduleArgs:
    def __init__(__self__, *,
                 end_date: Optional[pulumi.Input[str]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 recurrence_values: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 start_date: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None):
        """
        Schedule for a given suppression configuration.
        :param pulumi.Input[str] end_date: End date for suppression
        :param pulumi.Input[str] end_time: End date for suppression
        :param pulumi.Input[Sequence[pulumi.Input[int]]] recurrence_values: Specifies the values for recurrence pattern
        :param pulumi.Input[str] start_date: Start date for suppression
        :param pulumi.Input[str] start_time: Start time for suppression
        """
        if end_date is not None:
            pulumi.set(__self__, "end_date", end_date)
        if end_time is not None:
            pulumi.set(__self__, "end_time", end_time)
        if recurrence_values is not None:
            pulumi.set(__self__, "recurrence_values", recurrence_values)
        if start_date is not None:
            pulumi.set(__self__, "start_date", start_date)
        if start_time is not None:
            pulumi.set(__self__, "start_time", start_time)

    @property
    @pulumi.getter(name="endDate")
    def end_date(self) -> Optional[pulumi.Input[str]]:
        """
        End date for suppression
        """
        return pulumi.get(self, "end_date")

    @end_date.setter
    def end_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end_date", value)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> Optional[pulumi.Input[str]]:
        """
        End date for suppression
        """
        return pulumi.get(self, "end_time")

    @end_time.setter
    def end_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end_time", value)

    @property
    @pulumi.getter(name="recurrenceValues")
    def recurrence_values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        """
        Specifies the values for recurrence pattern
        """
        return pulumi.get(self, "recurrence_values")

    @recurrence_values.setter
    def recurrence_values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "recurrence_values", value)

    @property
    @pulumi.getter(name="startDate")
    def start_date(self) -> Optional[pulumi.Input[str]]:
        """
        Start date for suppression
        """
        return pulumi.get(self, "start_date")

    @start_date.setter
    def start_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_date", value)

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> Optional[pulumi.Input[str]]:
        """
        Start time for suppression
        """
        return pulumi.get(self, "start_time")

    @start_time.setter
    def start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_time", value)


@pulumi.input_type
class SuppressionArgs:
    def __init__(__self__, *,
                 suppression_config: pulumi.Input['SuppressionConfigArgs'],
                 type: pulumi.Input[str],
                 conditions: Optional[pulumi.Input['ConditionsArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input['ScopeArgs']] = None,
                 status: Optional[pulumi.Input[Union[str, 'ActionRuleStatus']]] = None):
        """
        Action rule with suppression configuration
        :param pulumi.Input['SuppressionConfigArgs'] suppression_config: suppression configuration for the action rule
        :param pulumi.Input[str] type: Indicates type of action rule
               Expected value is 'Suppression'.
        :param pulumi.Input['ConditionsArgs'] conditions: conditions on which alerts will be filtered
        :param pulumi.Input[str] description: Description of action rule
        :param pulumi.Input['ScopeArgs'] scope: scope on which action rule will apply
        :param pulumi.Input[Union[str, 'ActionRuleStatus']] status: Indicates if the given action rule is enabled or disabled
        """
        pulumi.set(__self__, "suppression_config", suppression_config)
        pulumi.set(__self__, "type", 'Suppression')
        if conditions is not None:
            pulumi.set(__self__, "conditions", conditions)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if scope is not None:
            pulumi.set(__self__, "scope", scope)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="suppressionConfig")
    def suppression_config(self) -> pulumi.Input['SuppressionConfigArgs']:
        """
        suppression configuration for the action rule
        """
        return pulumi.get(self, "suppression_config")

    @suppression_config.setter
    def suppression_config(self, value: pulumi.Input['SuppressionConfigArgs']):
        pulumi.set(self, "suppression_config", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Indicates type of action rule
        Expected value is 'Suppression'.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def conditions(self) -> Optional[pulumi.Input['ConditionsArgs']]:
        """
        conditions on which alerts will be filtered
        """
        return pulumi.get(self, "conditions")

    @conditions.setter
    def conditions(self, value: Optional[pulumi.Input['ConditionsArgs']]):
        pulumi.set(self, "conditions", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of action rule
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def scope(self) -> Optional[pulumi.Input['ScopeArgs']]:
        """
        scope on which action rule will apply
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: Optional[pulumi.Input['ScopeArgs']]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'ActionRuleStatus']]]:
        """
        Indicates if the given action rule is enabled or disabled
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'ActionRuleStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class ThrottlingInformationArgs:
    def __init__(__self__, *,
                 duration: Optional[pulumi.Input[str]] = None):
        """
        Optional throttling information for the alert rule.
        :param pulumi.Input[str] duration: The required duration (in ISO8601 format) to wait before notifying on the alert rule again. The time granularity must be in minutes and minimum value is 0 minutes
        """
        if duration is not None:
            pulumi.set(__self__, "duration", duration)

    @property
    @pulumi.getter
    def duration(self) -> Optional[pulumi.Input[str]]:
        """
        The required duration (in ISO8601 format) to wait before notifying on the alert rule again. The time granularity must be in minutes and minimum value is 0 minutes
        """
        return pulumi.get(self, "duration")

    @duration.setter
    def duration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "duration", value)


