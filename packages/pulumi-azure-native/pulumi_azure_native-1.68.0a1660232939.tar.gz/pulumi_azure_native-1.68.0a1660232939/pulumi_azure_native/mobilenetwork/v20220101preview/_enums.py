# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'CoreNetworkType',
    'CreatedByType',
    'NaptEnabled',
    'PduSessionType',
    'PreemptionCapability',
    'PreemptionVulnerability',
    'SdfDirection',
    'TrafficControlPermission',
]


class CoreNetworkType(str, Enum):
    """
    The core network technology generation.
    """
    CORE_NETWORK_TYPE_5_GC = "5GC"
    EPC = "EPC"


class CreatedByType(str, Enum):
    """
    The type of identity that last modified the resource.
    """
    USER = "User"
    APPLICATION = "Application"
    MANAGED_IDENTITY = "ManagedIdentity"
    KEY = "Key"


class NaptEnabled(str, Enum):
    """
    Whether NAPT is enabled for connections to this attachedDataNetwork.
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class PduSessionType(str, Enum):
    """
    The default PDU session type, which is used if the UE does not request a specific session type.
    """
    I_PV4 = "IPv4"
    I_PV6 = "IPv6"


class PreemptionCapability(str, Enum):
    """
    Default QoS Flow preemption capability.  The Preemption Capability of a QoS Flow controls whether it can preempt another QoS Flow with a lower priority level. See 3GPP TS23.501 section 5.7.2.2 for a full description of the ARP parameters.
    """
    NOT_PREEMPT = "NotPreempt"
    MAY_PREEMPT = "MayPreempt"


class PreemptionVulnerability(str, Enum):
    """
    Default QoS Flow preemption vulnerability.  The Preemption Vulnerability of a QoS Flow controls whether it can be preempted by QoS Flow with a higher priority level. See 3GPP TS23.501 section 5.7.2.2 for a full description of the ARP parameters.
    """
    NOT_PREEMPTABLE = "NotPreemptable"
    PREEMPTABLE = "Preemptable"


class SdfDirection(str, Enum):
    """
    The direction of this flow.
    """
    UPLINK = "Uplink"
    DOWNLINK = "Downlink"
    BIDIRECTIONAL = "Bidirectional"


class TrafficControlPermission(str, Enum):
    """
    Determines whether flows that match this PCC Rule are permitted.
    """
    ENABLED = "Enabled"
    BLOCKED = "Blocked"
