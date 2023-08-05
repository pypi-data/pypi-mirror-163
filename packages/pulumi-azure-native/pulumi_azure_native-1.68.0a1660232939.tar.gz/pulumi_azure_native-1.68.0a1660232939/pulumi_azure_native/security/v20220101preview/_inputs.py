# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'GovernanceAssignmentAdditionalDataArgs',
    'GovernanceEmailNotificationArgs',
    'GovernanceRuleEmailNotificationArgs',
    'GovernanceRuleOwnerSourceArgs',
    'RemediationEtaArgs',
]

@pulumi.input_type
class GovernanceAssignmentAdditionalDataArgs:
    def __init__(__self__, *,
                 ticket_link: Optional[pulumi.Input[str]] = None,
                 ticket_number: Optional[pulumi.Input[int]] = None,
                 ticket_status: Optional[pulumi.Input[str]] = None):
        """
        Describe the additional data of GovernanceAssignment - optional
        :param pulumi.Input[str] ticket_link: Ticket link associated with this GovernanceAssignment - for example: https://snow.com
        :param pulumi.Input[int] ticket_number: Ticket number associated with this GovernanceAssignment
        :param pulumi.Input[str] ticket_status: The ticket status associated with this GovernanceAssignment - for example: Active
        """
        if ticket_link is not None:
            pulumi.set(__self__, "ticket_link", ticket_link)
        if ticket_number is not None:
            pulumi.set(__self__, "ticket_number", ticket_number)
        if ticket_status is not None:
            pulumi.set(__self__, "ticket_status", ticket_status)

    @property
    @pulumi.getter(name="ticketLink")
    def ticket_link(self) -> Optional[pulumi.Input[str]]:
        """
        Ticket link associated with this GovernanceAssignment - for example: https://snow.com
        """
        return pulumi.get(self, "ticket_link")

    @ticket_link.setter
    def ticket_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ticket_link", value)

    @property
    @pulumi.getter(name="ticketNumber")
    def ticket_number(self) -> Optional[pulumi.Input[int]]:
        """
        Ticket number associated with this GovernanceAssignment
        """
        return pulumi.get(self, "ticket_number")

    @ticket_number.setter
    def ticket_number(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ticket_number", value)

    @property
    @pulumi.getter(name="ticketStatus")
    def ticket_status(self) -> Optional[pulumi.Input[str]]:
        """
        The ticket status associated with this GovernanceAssignment - for example: Active
        """
        return pulumi.get(self, "ticket_status")

    @ticket_status.setter
    def ticket_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ticket_status", value)


@pulumi.input_type
class GovernanceEmailNotificationArgs:
    def __init__(__self__, *,
                 disable_manager_email_notification: Optional[pulumi.Input[bool]] = None,
                 disable_owner_email_notification: Optional[pulumi.Input[bool]] = None):
        """
        The governance email weekly notification configuration.
        :param pulumi.Input[bool] disable_manager_email_notification: Exclude manager from weekly email notification.
        :param pulumi.Input[bool] disable_owner_email_notification: Exclude  owner from weekly email notification.
        """
        if disable_manager_email_notification is not None:
            pulumi.set(__self__, "disable_manager_email_notification", disable_manager_email_notification)
        if disable_owner_email_notification is not None:
            pulumi.set(__self__, "disable_owner_email_notification", disable_owner_email_notification)

    @property
    @pulumi.getter(name="disableManagerEmailNotification")
    def disable_manager_email_notification(self) -> Optional[pulumi.Input[bool]]:
        """
        Exclude manager from weekly email notification.
        """
        return pulumi.get(self, "disable_manager_email_notification")

    @disable_manager_email_notification.setter
    def disable_manager_email_notification(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_manager_email_notification", value)

    @property
    @pulumi.getter(name="disableOwnerEmailNotification")
    def disable_owner_email_notification(self) -> Optional[pulumi.Input[bool]]:
        """
        Exclude  owner from weekly email notification.
        """
        return pulumi.get(self, "disable_owner_email_notification")

    @disable_owner_email_notification.setter
    def disable_owner_email_notification(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_owner_email_notification", value)


@pulumi.input_type
class GovernanceRuleEmailNotificationArgs:
    def __init__(__self__, *,
                 disable_manager_email_notification: Optional[pulumi.Input[bool]] = None,
                 disable_owner_email_notification: Optional[pulumi.Input[bool]] = None):
        """
        The governance email weekly notification configuration.
        :param pulumi.Input[bool] disable_manager_email_notification: Defines whether manager email notifications are disabled.
        :param pulumi.Input[bool] disable_owner_email_notification: Defines whether owner email notifications are disabled.
        """
        if disable_manager_email_notification is not None:
            pulumi.set(__self__, "disable_manager_email_notification", disable_manager_email_notification)
        if disable_owner_email_notification is not None:
            pulumi.set(__self__, "disable_owner_email_notification", disable_owner_email_notification)

    @property
    @pulumi.getter(name="disableManagerEmailNotification")
    def disable_manager_email_notification(self) -> Optional[pulumi.Input[bool]]:
        """
        Defines whether manager email notifications are disabled.
        """
        return pulumi.get(self, "disable_manager_email_notification")

    @disable_manager_email_notification.setter
    def disable_manager_email_notification(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_manager_email_notification", value)

    @property
    @pulumi.getter(name="disableOwnerEmailNotification")
    def disable_owner_email_notification(self) -> Optional[pulumi.Input[bool]]:
        """
        Defines whether owner email notifications are disabled.
        """
        return pulumi.get(self, "disable_owner_email_notification")

    @disable_owner_email_notification.setter
    def disable_owner_email_notification(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_owner_email_notification", value)


@pulumi.input_type
class GovernanceRuleOwnerSourceArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input[Union[str, 'GovernanceRuleOwnerSourceType']]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        Describe the owner source of governance rule
        :param pulumi.Input[Union[str, 'GovernanceRuleOwnerSourceType']] type: The owner type for the governance rule owner source
        :param pulumi.Input[str] value: The source value e.g. tag key like owner name or email address
        """
        if type is not None:
            pulumi.set(__self__, "type", type)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'GovernanceRuleOwnerSourceType']]]:
        """
        The owner type for the governance rule owner source
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'GovernanceRuleOwnerSourceType']]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        The source value e.g. tag key like owner name or email address
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class RemediationEtaArgs:
    def __init__(__self__, *,
                 eta: pulumi.Input[str],
                 justification: pulumi.Input[str]):
        """
        The ETA (estimated time of arrival) for remediation
        :param pulumi.Input[str] eta: ETA for remediation.
        :param pulumi.Input[str] justification: Justification for change of Eta.
        """
        pulumi.set(__self__, "eta", eta)
        pulumi.set(__self__, "justification", justification)

    @property
    @pulumi.getter
    def eta(self) -> pulumi.Input[str]:
        """
        ETA for remediation.
        """
        return pulumi.get(self, "eta")

    @eta.setter
    def eta(self, value: pulumi.Input[str]):
        pulumi.set(self, "eta", value)

    @property
    @pulumi.getter
    def justification(self) -> pulumi.Input[str]:
        """
        Justification for change of Eta.
        """
        return pulumi.get(self, "justification")

    @justification.setter
    def justification(self, value: pulumi.Input[str]):
        pulumi.set(self, "justification", value)


