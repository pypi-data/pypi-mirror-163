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

__all__ = [
    'ActionsResponse',
    'ConditionResponse',
    'ConditionResponseFailingPeriods',
    'DimensionResponse',
    'ScheduledQueryRuleCriteriaResponse',
    'SystemDataResponse',
    'UserAssignedIdentityResponse',
    'WorkbookResourceResponseIdentity',
]

@pulumi.output_type
class ActionsResponse(dict):
    """
    Actions to invoke when the alert fires.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "actionGroups":
            suggest = "action_groups"
        elif key == "customProperties":
            suggest = "custom_properties"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ActionsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ActionsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ActionsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 action_groups: Optional[Sequence[str]] = None,
                 custom_properties: Optional[Mapping[str, str]] = None):
        """
        Actions to invoke when the alert fires.
        :param Sequence[str] action_groups: Action Group resource Ids to invoke when the alert fires.
        :param Mapping[str, str] custom_properties: The properties of an alert payload.
        """
        if action_groups is not None:
            pulumi.set(__self__, "action_groups", action_groups)
        if custom_properties is not None:
            pulumi.set(__self__, "custom_properties", custom_properties)

    @property
    @pulumi.getter(name="actionGroups")
    def action_groups(self) -> Optional[Sequence[str]]:
        """
        Action Group resource Ids to invoke when the alert fires.
        """
        return pulumi.get(self, "action_groups")

    @property
    @pulumi.getter(name="customProperties")
    def custom_properties(self) -> Optional[Mapping[str, str]]:
        """
        The properties of an alert payload.
        """
        return pulumi.get(self, "custom_properties")


@pulumi.output_type
class ConditionResponse(dict):
    """
    A condition of the scheduled query rule.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "failingPeriods":
            suggest = "failing_periods"
        elif key == "metricMeasureColumn":
            suggest = "metric_measure_column"
        elif key == "metricName":
            suggest = "metric_name"
        elif key == "resourceIdColumn":
            suggest = "resource_id_column"
        elif key == "timeAggregation":
            suggest = "time_aggregation"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConditionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConditionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConditionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 dimensions: Optional[Sequence['outputs.DimensionResponse']] = None,
                 failing_periods: Optional['outputs.ConditionResponseFailingPeriods'] = None,
                 metric_measure_column: Optional[str] = None,
                 metric_name: Optional[str] = None,
                 operator: Optional[str] = None,
                 query: Optional[str] = None,
                 resource_id_column: Optional[str] = None,
                 threshold: Optional[float] = None,
                 time_aggregation: Optional[str] = None):
        """
        A condition of the scheduled query rule.
        :param Sequence['DimensionResponse'] dimensions: List of Dimensions conditions
        :param 'ConditionResponseFailingPeriods' failing_periods: The minimum number of violations required within the selected lookback time window required to raise an alert. Relevant only for rules of the kind LogAlert.
        :param str metric_measure_column: The column containing the metric measure number. Relevant only for rules of the kind LogAlert.
        :param str metric_name: The name of the metric to be sent. Relevant and required only for rules of the kind LogToMetric.
        :param str operator: The criteria operator. Relevant and required only for rules of the kind LogAlert.
        :param str query: Log query alert
        :param str resource_id_column: The column containing the resource id. The content of the column must be a uri formatted as resource id. Relevant only for rules of the kind LogAlert.
        :param float threshold: the criteria threshold value that activates the alert. Relevant and required only for rules of the kind LogAlert.
        :param str time_aggregation: Aggregation type. Relevant and required only for rules of the kind LogAlert.
        """
        if dimensions is not None:
            pulumi.set(__self__, "dimensions", dimensions)
        if failing_periods is not None:
            pulumi.set(__self__, "failing_periods", failing_periods)
        if metric_measure_column is not None:
            pulumi.set(__self__, "metric_measure_column", metric_measure_column)
        if metric_name is not None:
            pulumi.set(__self__, "metric_name", metric_name)
        if operator is not None:
            pulumi.set(__self__, "operator", operator)
        if query is not None:
            pulumi.set(__self__, "query", query)
        if resource_id_column is not None:
            pulumi.set(__self__, "resource_id_column", resource_id_column)
        if threshold is not None:
            pulumi.set(__self__, "threshold", threshold)
        if time_aggregation is not None:
            pulumi.set(__self__, "time_aggregation", time_aggregation)

    @property
    @pulumi.getter
    def dimensions(self) -> Optional[Sequence['outputs.DimensionResponse']]:
        """
        List of Dimensions conditions
        """
        return pulumi.get(self, "dimensions")

    @property
    @pulumi.getter(name="failingPeriods")
    def failing_periods(self) -> Optional['outputs.ConditionResponseFailingPeriods']:
        """
        The minimum number of violations required within the selected lookback time window required to raise an alert. Relevant only for rules of the kind LogAlert.
        """
        return pulumi.get(self, "failing_periods")

    @property
    @pulumi.getter(name="metricMeasureColumn")
    def metric_measure_column(self) -> Optional[str]:
        """
        The column containing the metric measure number. Relevant only for rules of the kind LogAlert.
        """
        return pulumi.get(self, "metric_measure_column")

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> Optional[str]:
        """
        The name of the metric to be sent. Relevant and required only for rules of the kind LogToMetric.
        """
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter
    def operator(self) -> Optional[str]:
        """
        The criteria operator. Relevant and required only for rules of the kind LogAlert.
        """
        return pulumi.get(self, "operator")

    @property
    @pulumi.getter
    def query(self) -> Optional[str]:
        """
        Log query alert
        """
        return pulumi.get(self, "query")

    @property
    @pulumi.getter(name="resourceIdColumn")
    def resource_id_column(self) -> Optional[str]:
        """
        The column containing the resource id. The content of the column must be a uri formatted as resource id. Relevant only for rules of the kind LogAlert.
        """
        return pulumi.get(self, "resource_id_column")

    @property
    @pulumi.getter
    def threshold(self) -> Optional[float]:
        """
        the criteria threshold value that activates the alert. Relevant and required only for rules of the kind LogAlert.
        """
        return pulumi.get(self, "threshold")

    @property
    @pulumi.getter(name="timeAggregation")
    def time_aggregation(self) -> Optional[str]:
        """
        Aggregation type. Relevant and required only for rules of the kind LogAlert.
        """
        return pulumi.get(self, "time_aggregation")


@pulumi.output_type
class ConditionResponseFailingPeriods(dict):
    """
    The minimum number of violations required within the selected lookback time window required to raise an alert. Relevant only for rules of the kind LogAlert.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "minFailingPeriodsToAlert":
            suggest = "min_failing_periods_to_alert"
        elif key == "numberOfEvaluationPeriods":
            suggest = "number_of_evaluation_periods"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConditionResponseFailingPeriods. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConditionResponseFailingPeriods.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConditionResponseFailingPeriods.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 min_failing_periods_to_alert: Optional[float] = None,
                 number_of_evaluation_periods: Optional[float] = None):
        """
        The minimum number of violations required within the selected lookback time window required to raise an alert. Relevant only for rules of the kind LogAlert.
        :param float min_failing_periods_to_alert: The number of violations to trigger an alert. Should be smaller or equal to numberOfEvaluationPeriods. Default value is 1
        :param float number_of_evaluation_periods: The number of aggregated lookback points. The lookback time window is calculated based on the aggregation granularity (windowSize) and the selected number of aggregated points. Default value is 1
        """
        if min_failing_periods_to_alert is None:
            min_failing_periods_to_alert = 1
        if min_failing_periods_to_alert is not None:
            pulumi.set(__self__, "min_failing_periods_to_alert", min_failing_periods_to_alert)
        if number_of_evaluation_periods is None:
            number_of_evaluation_periods = 1
        if number_of_evaluation_periods is not None:
            pulumi.set(__self__, "number_of_evaluation_periods", number_of_evaluation_periods)

    @property
    @pulumi.getter(name="minFailingPeriodsToAlert")
    def min_failing_periods_to_alert(self) -> Optional[float]:
        """
        The number of violations to trigger an alert. Should be smaller or equal to numberOfEvaluationPeriods. Default value is 1
        """
        return pulumi.get(self, "min_failing_periods_to_alert")

    @property
    @pulumi.getter(name="numberOfEvaluationPeriods")
    def number_of_evaluation_periods(self) -> Optional[float]:
        """
        The number of aggregated lookback points. The lookback time window is calculated based on the aggregation granularity (windowSize) and the selected number of aggregated points. Default value is 1
        """
        return pulumi.get(self, "number_of_evaluation_periods")


@pulumi.output_type
class DimensionResponse(dict):
    """
    Dimension splitting and filtering definition
    """
    def __init__(__self__, *,
                 name: str,
                 operator: str,
                 values: Sequence[str]):
        """
        Dimension splitting and filtering definition
        :param str name: Name of the dimension
        :param str operator: Operator for dimension values
        :param Sequence[str] values: List of dimension values
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "operator", operator)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the dimension
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def operator(self) -> str:
        """
        Operator for dimension values
        """
        return pulumi.get(self, "operator")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        """
        List of dimension values
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class ScheduledQueryRuleCriteriaResponse(dict):
    """
    The rule criteria that defines the conditions of the scheduled query rule.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "allOf":
            suggest = "all_of"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScheduledQueryRuleCriteriaResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScheduledQueryRuleCriteriaResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScheduledQueryRuleCriteriaResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 all_of: Optional[Sequence['outputs.ConditionResponse']] = None):
        """
        The rule criteria that defines the conditions of the scheduled query rule.
        :param Sequence['ConditionResponse'] all_of: A list of conditions to evaluate against the specified scopes
        """
        if all_of is not None:
            pulumi.set(__self__, "all_of", all_of)

    @property
    @pulumi.getter(name="allOf")
    def all_of(self) -> Optional[Sequence['outputs.ConditionResponse']]:
        """
        A list of conditions to evaluate against the specified scopes
        """
        return pulumi.get(self, "all_of")


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdAt":
            suggest = "created_at"
        elif key == "createdBy":
            suggest = "created_by"
        elif key == "createdByType":
            suggest = "created_by_type"
        elif key == "lastModifiedAt":
            suggest = "last_modified_at"
        elif key == "lastModifiedBy":
            suggest = "last_modified_by"
        elif key == "lastModifiedByType":
            suggest = "last_modified_by_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SystemDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 created_by: Optional[str] = None,
                 created_by_type: Optional[str] = None,
                 last_modified_at: Optional[str] = None,
                 last_modified_by: Optional[str] = None,
                 last_modified_by_type: Optional[str] = None):
        """
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The timestamp of resource last modification (UTC)
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if created_by_type is not None:
            pulumi.set(__self__, "created_by_type", created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")


@pulumi.output_type
class UserAssignedIdentityResponse(dict):
    """
    User assigned identity properties
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientId":
            suggest = "client_id"
        elif key == "principalId":
            suggest = "principal_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UserAssignedIdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UserAssignedIdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        UserAssignedIdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_id: str,
                 principal_id: str):
        """
        User assigned identity properties
        :param str client_id: The client ID of the assigned identity.
        :param str principal_id: The principal ID of the assigned identity.
        """
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "principal_id", principal_id)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        """
        The client ID of the assigned identity.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal ID of the assigned identity.
        """
        return pulumi.get(self, "principal_id")


@pulumi.output_type
class WorkbookResourceResponseIdentity(dict):
    """
    Identity used for BYOS
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"
        elif key == "userAssignedIdentities":
            suggest = "user_assigned_identities"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkbookResourceResponseIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkbookResourceResponseIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkbookResourceResponseIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: str,
                 user_assigned_identities: Optional[Mapping[str, 'outputs.UserAssignedIdentityResponse']] = None):
        """
        Identity used for BYOS
        :param str principal_id: The service principal ID of the system assigned identity. This property will only be provided for a system assigned identity.
        :param str tenant_id: The tenant ID of the system assigned identity. This property will only be provided for a system assigned identity.
        :param str type: Type of managed service identity (where both SystemAssigned and UserAssigned types are allowed).
        :param Mapping[str, 'UserAssignedIdentityResponse'] user_assigned_identities: The set of user assigned identities associated with the resource. The userAssignedIdentities dictionary keys will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}. The dictionary values can be empty objects ({}) in requests.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The service principal ID of the system assigned identity. This property will only be provided for a system assigned identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant ID of the system assigned identity. This property will only be provided for a system assigned identity.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of managed service identity (where both SystemAssigned and UserAssigned types are allowed).
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[Mapping[str, 'outputs.UserAssignedIdentityResponse']]:
        """
        The set of user assigned identities associated with the resource. The userAssignedIdentities dictionary keys will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}. The dictionary values can be empty objects ({}) in requests.
        """
        return pulumi.get(self, "user_assigned_identities")


