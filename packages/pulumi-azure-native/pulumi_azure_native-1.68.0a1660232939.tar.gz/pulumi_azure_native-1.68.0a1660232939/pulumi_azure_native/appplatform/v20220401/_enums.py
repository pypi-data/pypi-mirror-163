# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'BindingType',
    'ManagedIdentityType',
]


class BindingType(str, Enum):
    """
    Buildpack Binding Type
    """
    APPLICATION_INSIGHTS = "ApplicationInsights"
    APACHE_SKY_WALKING = "ApacheSkyWalking"
    APP_DYNAMICS = "AppDynamics"
    DYNATRACE = "Dynatrace"
    NEW_RELIC = "NewRelic"
    ELASTIC_APM = "ElasticAPM"


class ManagedIdentityType(str, Enum):
    """
    Type of the managed identity
    """
    NONE = "None"
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned,UserAssigned"
