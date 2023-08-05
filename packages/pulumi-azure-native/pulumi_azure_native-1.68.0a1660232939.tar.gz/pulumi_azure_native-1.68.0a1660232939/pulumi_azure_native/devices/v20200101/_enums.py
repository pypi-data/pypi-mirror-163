# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AccessRightsDescription',
    'AllocationPolicy',
    'IotDpsSku',
    'IpFilterActionType',
    'IpFilterTargetType',
    'State',
]


class AccessRightsDescription(str, Enum):
    """
    Rights that this key has.
    """
    SERVICE_CONFIG = "ServiceConfig"
    ENROLLMENT_READ = "EnrollmentRead"
    ENROLLMENT_WRITE = "EnrollmentWrite"
    DEVICE_CONNECT = "DeviceConnect"
    REGISTRATION_STATUS_READ = "RegistrationStatusRead"
    REGISTRATION_STATUS_WRITE = "RegistrationStatusWrite"


class AllocationPolicy(str, Enum):
    """
    Allocation policy to be used by this provisioning service.
    """
    HASHED = "Hashed"
    GEO_LATENCY = "GeoLatency"
    STATIC = "Static"


class IotDpsSku(str, Enum):
    """
    Sku name.
    """
    S1 = "S1"


class IpFilterActionType(str, Enum):
    """
    The desired action for requests captured by this rule.
    """
    ACCEPT = "Accept"
    REJECT = "Reject"


class IpFilterTargetType(str, Enum):
    """
    Target for requests captured by this rule.
    """
    ALL = "all"
    SERVICE_API = "serviceApi"
    DEVICE_API = "deviceApi"


class State(str, Enum):
    """
    Current state of the provisioning service.
    """
    ACTIVATING = "Activating"
    ACTIVE = "Active"
    DELETING = "Deleting"
    DELETED = "Deleted"
    ACTIVATION_FAILED = "ActivationFailed"
    DELETION_FAILED = "DeletionFailed"
    TRANSITIONING = "Transitioning"
    SUSPENDING = "Suspending"
    SUSPENDED = "Suspended"
    RESUMING = "Resuming"
    FAILING_OVER = "FailingOver"
    FAILOVER_FAILED = "FailoverFailed"
