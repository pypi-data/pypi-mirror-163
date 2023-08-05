# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ActionType',
    'CustomRuleEnabledState',
    'FrontDoorMatchVariable',
    'ManagedRuleEnabledState',
    'ManagedRuleExclusionMatchVariable',
    'ManagedRuleExclusionSelectorMatchOperator',
    'ManagedRuleSetActionType',
    'Operator',
    'PolicyEnabledState',
    'PolicyMode',
    'PolicyRequestBodyCheck',
    'RuleType',
    'SkuName',
    'TransformType',
]


class ActionType(str, Enum):
    """
    Describes the override action to be applied when rule matches.
    """
    ALLOW = "Allow"
    BLOCK = "Block"
    LOG = "Log"
    REDIRECT = "Redirect"


class CustomRuleEnabledState(str, Enum):
    """
    Describes if the custom rule is in enabled or disabled state. Defaults to Enabled if not specified.
    """
    DISABLED = "Disabled"
    ENABLED = "Enabled"


class FrontDoorMatchVariable(str, Enum):
    """
    Request variable to compare with.
    """
    REMOTE_ADDR = "RemoteAddr"
    REQUEST_METHOD = "RequestMethod"
    QUERY_STRING = "QueryString"
    POST_ARGS = "PostArgs"
    REQUEST_URI = "RequestUri"
    REQUEST_HEADER = "RequestHeader"
    REQUEST_BODY = "RequestBody"
    COOKIES = "Cookies"
    SOCKET_ADDR = "SocketAddr"


class ManagedRuleEnabledState(str, Enum):
    """
    Describes if the managed rule is in enabled or disabled state. Defaults to Disabled if not specified.
    """
    DISABLED = "Disabled"
    ENABLED = "Enabled"


class ManagedRuleExclusionMatchVariable(str, Enum):
    """
    The variable type to be excluded.
    """
    REQUEST_HEADER_NAMES = "RequestHeaderNames"
    REQUEST_COOKIE_NAMES = "RequestCookieNames"
    QUERY_STRING_ARG_NAMES = "QueryStringArgNames"
    REQUEST_BODY_POST_ARG_NAMES = "RequestBodyPostArgNames"
    REQUEST_BODY_JSON_ARG_NAMES = "RequestBodyJsonArgNames"


class ManagedRuleExclusionSelectorMatchOperator(str, Enum):
    """
    Comparison operator to apply to the selector when specifying which elements in the collection this exclusion applies to.
    """
    EQUALS = "Equals"
    CONTAINS = "Contains"
    STARTS_WITH = "StartsWith"
    ENDS_WITH = "EndsWith"
    EQUALS_ANY = "EqualsAny"


class ManagedRuleSetActionType(str, Enum):
    """
    Defines the rule set action.
    """
    BLOCK = "Block"
    LOG = "Log"
    REDIRECT = "Redirect"


class Operator(str, Enum):
    """
    Comparison type to use for matching with the variable value.
    """
    ANY = "Any"
    IP_MATCH = "IPMatch"
    GEO_MATCH = "GeoMatch"
    EQUAL = "Equal"
    CONTAINS = "Contains"
    LESS_THAN = "LessThan"
    GREATER_THAN = "GreaterThan"
    LESS_THAN_OR_EQUAL = "LessThanOrEqual"
    GREATER_THAN_OR_EQUAL = "GreaterThanOrEqual"
    BEGINS_WITH = "BeginsWith"
    ENDS_WITH = "EndsWith"
    REG_EX = "RegEx"


class PolicyEnabledState(str, Enum):
    """
    Describes if the policy is in enabled or disabled state. Defaults to Enabled if not specified.
    """
    DISABLED = "Disabled"
    ENABLED = "Enabled"


class PolicyMode(str, Enum):
    """
    Describes if it is in detection mode or prevention mode at policy level.
    """
    PREVENTION = "Prevention"
    DETECTION = "Detection"


class PolicyRequestBodyCheck(str, Enum):
    """
    Describes if policy managed rules will inspect the request body content.
    """
    DISABLED = "Disabled"
    ENABLED = "Enabled"


class RuleType(str, Enum):
    """
    Describes type of rule.
    """
    MATCH_RULE = "MatchRule"
    RATE_LIMIT_RULE = "RateLimitRule"


class SkuName(str, Enum):
    """
    Name of the pricing tier.
    """
    CLASSIC_AZURE_FRONT_DOOR = "Classic_AzureFrontDoor"
    STANDARD_AZURE_FRONT_DOOR = "Standard_AzureFrontDoor"
    PREMIUM_AZURE_FRONT_DOOR = "Premium_AzureFrontDoor"


class TransformType(str, Enum):
    """
    Describes what transforms applied before matching.
    """
    LOWERCASE = "Lowercase"
    UPPERCASE = "Uppercase"
    TRIM = "Trim"
    URL_DECODE = "UrlDecode"
    URL_ENCODE = "UrlEncode"
    REMOVE_NULLS = "RemoveNulls"
