# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'BackendEnabledState',
    'DynamicCompressionEnabled',
    'EnforceCertificateNameCheckEnabledState',
    'FrontDoorEnabledState',
    'FrontDoorForwardingProtocol',
    'FrontDoorHealthProbeMethod',
    'FrontDoorProtocol',
    'FrontDoorQuery',
    'FrontDoorRedirectProtocol',
    'FrontDoorRedirectType',
    'HealthProbeEnabled',
    'RoutingRuleEnabledState',
    'SessionAffinityEnabledState',
]


class BackendEnabledState(str, Enum):
    """
    Whether to enable use of this backend. Permitted values are 'Enabled' or 'Disabled'
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class DynamicCompressionEnabled(str, Enum):
    """
    Whether to use dynamic compression for cached content
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class EnforceCertificateNameCheckEnabledState(str, Enum):
    """
    Whether to enforce certificate name check on HTTPS requests to all backend pools. No effect on non-HTTPS requests.
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class FrontDoorEnabledState(str, Enum):
    """
    Operational status of the Front Door load balancer. Permitted values are 'Enabled' or 'Disabled'
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class FrontDoorForwardingProtocol(str, Enum):
    """
    Protocol this rule will use when forwarding traffic to backends.
    """
    HTTP_ONLY = "HttpOnly"
    HTTPS_ONLY = "HttpsOnly"
    MATCH_REQUEST = "MatchRequest"


class FrontDoorHealthProbeMethod(str, Enum):
    """
    Configures which HTTP method to use to probe the backends defined under backendPools.
    """
    GET = "GET"
    HEAD = "HEAD"


class FrontDoorProtocol(str, Enum):
    """
    Accepted protocol schemes.
    """
    HTTP = "Http"
    HTTPS = "Https"


class FrontDoorQuery(str, Enum):
    """
    Treatment of URL query terms when forming the cache key.
    """
    STRIP_NONE = "StripNone"
    STRIP_ALL = "StripAll"


class FrontDoorRedirectProtocol(str, Enum):
    """
    The protocol of the destination to where the traffic is redirected
    """
    HTTP_ONLY = "HttpOnly"
    HTTPS_ONLY = "HttpsOnly"
    MATCH_REQUEST = "MatchRequest"


class FrontDoorRedirectType(str, Enum):
    """
    The redirect type the rule will use when redirecting traffic.
    """
    MOVED = "Moved"
    FOUND = "Found"
    TEMPORARY_REDIRECT = "TemporaryRedirect"
    PERMANENT_REDIRECT = "PermanentRedirect"


class HealthProbeEnabled(str, Enum):
    """
    Whether to enable health probes to be made against backends defined under backendPools. Health probes can only be disabled if there is a single enabled backend in single enabled backend pool.
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class RoutingRuleEnabledState(str, Enum):
    """
    Whether to enable use of this rule. Permitted values are 'Enabled' or 'Disabled'
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class SessionAffinityEnabledState(str, Enum):
    """
    Whether to allow session affinity on this host. Valid options are 'Enabled' or 'Disabled'
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"
