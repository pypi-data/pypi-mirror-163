# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetAutoscaleSettingResult',
    'AwaitableGetAutoscaleSettingResult',
    'get_autoscale_setting',
    'get_autoscale_setting_output',
]

warnings.warn("""Version 2014-04-01 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetAutoscaleSettingResult:
    """
    The autoscale setting resource.
    """
    def __init__(__self__, enabled=None, id=None, location=None, name=None, notifications=None, profiles=None, tags=None, target_resource_location=None, target_resource_uri=None, type=None):
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if notifications and not isinstance(notifications, list):
            raise TypeError("Expected argument 'notifications' to be a list")
        pulumi.set(__self__, "notifications", notifications)
        if profiles and not isinstance(profiles, list):
            raise TypeError("Expected argument 'profiles' to be a list")
        pulumi.set(__self__, "profiles", profiles)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if target_resource_location and not isinstance(target_resource_location, str):
            raise TypeError("Expected argument 'target_resource_location' to be a str")
        pulumi.set(__self__, "target_resource_location", target_resource_location)
        if target_resource_uri and not isinstance(target_resource_uri, str):
            raise TypeError("Expected argument 'target_resource_uri' to be a str")
        pulumi.set(__self__, "target_resource_uri", target_resource_uri)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        the enabled flag. Specifies whether automatic scaling is enabled for the resource. The default value is 'true'.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Azure resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def notifications(self) -> Optional[Sequence['outputs.AutoscaleNotificationResponse']]:
        """
        the collection of notifications.
        """
        return pulumi.get(self, "notifications")

    @property
    @pulumi.getter
    def profiles(self) -> Sequence['outputs.AutoscaleProfileResponse']:
        """
        the collection of automatic scaling profiles that specify different scaling parameters for different time periods. A maximum of 20 profiles can be specified.
        """
        return pulumi.get(self, "profiles")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetResourceLocation")
    def target_resource_location(self) -> Optional[str]:
        """
        the location of the resource that the autoscale setting should be added to.
        """
        return pulumi.get(self, "target_resource_location")

    @property
    @pulumi.getter(name="targetResourceUri")
    def target_resource_uri(self) -> Optional[str]:
        """
        the resource identifier of the resource that the autoscale setting should be added to.
        """
        return pulumi.get(self, "target_resource_uri")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetAutoscaleSettingResult(GetAutoscaleSettingResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAutoscaleSettingResult(
            enabled=self.enabled,
            id=self.id,
            location=self.location,
            name=self.name,
            notifications=self.notifications,
            profiles=self.profiles,
            tags=self.tags,
            target_resource_location=self.target_resource_location,
            target_resource_uri=self.target_resource_uri,
            type=self.type)


def get_autoscale_setting(autoscale_setting_name: Optional[str] = None,
                          resource_group_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAutoscaleSettingResult:
    """
    The autoscale setting resource.


    :param str autoscale_setting_name: The autoscale setting name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    pulumi.log.warn("""get_autoscale_setting is deprecated: Version 2014-04-01 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['autoscaleSettingName'] = autoscale_setting_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:insights/v20140401:getAutoscaleSetting', __args__, opts=opts, typ=GetAutoscaleSettingResult).value

    return AwaitableGetAutoscaleSettingResult(
        enabled=__ret__.enabled,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        notifications=__ret__.notifications,
        profiles=__ret__.profiles,
        tags=__ret__.tags,
        target_resource_location=__ret__.target_resource_location,
        target_resource_uri=__ret__.target_resource_uri,
        type=__ret__.type)


@_utilities.lift_output_func(get_autoscale_setting)
def get_autoscale_setting_output(autoscale_setting_name: Optional[pulumi.Input[str]] = None,
                                 resource_group_name: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAutoscaleSettingResult]:
    """
    The autoscale setting resource.


    :param str autoscale_setting_name: The autoscale setting name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    pulumi.log.warn("""get_autoscale_setting is deprecated: Version 2014-04-01 will be removed in v2 of the provider.""")
    ...
