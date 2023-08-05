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
    'MigrationRequestPropertiesArgs',
    'MsixPackageApplicationsArgs',
    'MsixPackageDependenciesArgs',
    'PrivateLinkServiceConnectionStateArgs',
    'RegistrationInfoArgs',
    'ResourceModelWithAllowedPropertySetIdentityArgs',
    'ResourceModelWithAllowedPropertySetPlanArgs',
    'ResourceModelWithAllowedPropertySetSkuArgs',
    'ScalingHostPoolReferenceArgs',
    'ScalingScheduleArgs',
    'TimeArgs',
]

@pulumi.input_type
class MigrationRequestPropertiesArgs:
    def __init__(__self__, *,
                 migration_path: Optional[pulumi.Input[str]] = None,
                 operation: Optional[pulumi.Input[Union[str, 'Operation']]] = None):
        """
        Properties for arm migration.
        :param pulumi.Input[str] migration_path: The path to the legacy object to migrate.
        :param pulumi.Input[Union[str, 'Operation']] operation: The type of operation for migration.
        """
        if migration_path is not None:
            pulumi.set(__self__, "migration_path", migration_path)
        if operation is not None:
            pulumi.set(__self__, "operation", operation)

    @property
    @pulumi.getter(name="migrationPath")
    def migration_path(self) -> Optional[pulumi.Input[str]]:
        """
        The path to the legacy object to migrate.
        """
        return pulumi.get(self, "migration_path")

    @migration_path.setter
    def migration_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "migration_path", value)

    @property
    @pulumi.getter
    def operation(self) -> Optional[pulumi.Input[Union[str, 'Operation']]]:
        """
        The type of operation for migration.
        """
        return pulumi.get(self, "operation")

    @operation.setter
    def operation(self, value: Optional[pulumi.Input[Union[str, 'Operation']]]):
        pulumi.set(self, "operation", value)


@pulumi.input_type
class MsixPackageApplicationsArgs:
    def __init__(__self__, *,
                 app_id: Optional[pulumi.Input[str]] = None,
                 app_user_model_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 icon_image_name: Optional[pulumi.Input[str]] = None,
                 raw_icon: Optional[pulumi.Input[str]] = None,
                 raw_png: Optional[pulumi.Input[str]] = None):
        """
        Schema for MSIX Package Application properties.
        :param pulumi.Input[str] app_id: Package Application Id, found in appxmanifest.xml.
        :param pulumi.Input[str] app_user_model_id: Used to activate Package Application. Consists of Package Name and ApplicationID. Found in appxmanifest.xml.
        :param pulumi.Input[str] description: Description of Package Application.
        :param pulumi.Input[str] friendly_name: User friendly name.
        :param pulumi.Input[str] icon_image_name: User friendly name.
        :param pulumi.Input[str] raw_icon: the icon a 64 bit string as a byte array.
        :param pulumi.Input[str] raw_png: the icon a 64 bit string as a byte array.
        """
        if app_id is not None:
            pulumi.set(__self__, "app_id", app_id)
        if app_user_model_id is not None:
            pulumi.set(__self__, "app_user_model_id", app_user_model_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if friendly_name is not None:
            pulumi.set(__self__, "friendly_name", friendly_name)
        if icon_image_name is not None:
            pulumi.set(__self__, "icon_image_name", icon_image_name)
        if raw_icon is not None:
            pulumi.set(__self__, "raw_icon", raw_icon)
        if raw_png is not None:
            pulumi.set(__self__, "raw_png", raw_png)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> Optional[pulumi.Input[str]]:
        """
        Package Application Id, found in appxmanifest.xml.
        """
        return pulumi.get(self, "app_id")

    @app_id.setter
    def app_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "app_id", value)

    @property
    @pulumi.getter(name="appUserModelID")
    def app_user_model_id(self) -> Optional[pulumi.Input[str]]:
        """
        Used to activate Package Application. Consists of Package Name and ApplicationID. Found in appxmanifest.xml.
        """
        return pulumi.get(self, "app_user_model_id")

    @app_user_model_id.setter
    def app_user_model_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "app_user_model_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of Package Application.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> Optional[pulumi.Input[str]]:
        """
        User friendly name.
        """
        return pulumi.get(self, "friendly_name")

    @friendly_name.setter
    def friendly_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "friendly_name", value)

    @property
    @pulumi.getter(name="iconImageName")
    def icon_image_name(self) -> Optional[pulumi.Input[str]]:
        """
        User friendly name.
        """
        return pulumi.get(self, "icon_image_name")

    @icon_image_name.setter
    def icon_image_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "icon_image_name", value)

    @property
    @pulumi.getter(name="rawIcon")
    def raw_icon(self) -> Optional[pulumi.Input[str]]:
        """
        the icon a 64 bit string as a byte array.
        """
        return pulumi.get(self, "raw_icon")

    @raw_icon.setter
    def raw_icon(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "raw_icon", value)

    @property
    @pulumi.getter(name="rawPng")
    def raw_png(self) -> Optional[pulumi.Input[str]]:
        """
        the icon a 64 bit string as a byte array.
        """
        return pulumi.get(self, "raw_png")

    @raw_png.setter
    def raw_png(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "raw_png", value)


@pulumi.input_type
class MsixPackageDependenciesArgs:
    def __init__(__self__, *,
                 dependency_name: Optional[pulumi.Input[str]] = None,
                 min_version: Optional[pulumi.Input[str]] = None,
                 publisher: Optional[pulumi.Input[str]] = None):
        """
        Schema for MSIX Package Dependencies properties.
        :param pulumi.Input[str] dependency_name: Name of package dependency.
        :param pulumi.Input[str] min_version: Dependency version required.
        :param pulumi.Input[str] publisher: Name of dependency publisher.
        """
        if dependency_name is not None:
            pulumi.set(__self__, "dependency_name", dependency_name)
        if min_version is not None:
            pulumi.set(__self__, "min_version", min_version)
        if publisher is not None:
            pulumi.set(__self__, "publisher", publisher)

    @property
    @pulumi.getter(name="dependencyName")
    def dependency_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of package dependency.
        """
        return pulumi.get(self, "dependency_name")

    @dependency_name.setter
    def dependency_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dependency_name", value)

    @property
    @pulumi.getter(name="minVersion")
    def min_version(self) -> Optional[pulumi.Input[str]]:
        """
        Dependency version required.
        """
        return pulumi.get(self, "min_version")

    @min_version.setter
    def min_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "min_version", value)

    @property
    @pulumi.getter
    def publisher(self) -> Optional[pulumi.Input[str]]:
        """
        Name of dependency publisher.
        """
        return pulumi.get(self, "publisher")

    @publisher.setter
    def publisher(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "publisher", value)


@pulumi.input_type
class PrivateLinkServiceConnectionStateArgs:
    def __init__(__self__, *,
                 actions_required: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]] = None):
        """
        A collection of information about the state of the connection between service consumer and provider.
        :param pulumi.Input[str] actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param pulumi.Input[str] description: The reason for approval/rejection of the connection.
        :param pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']] status: Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        if actions_required is not None:
            pulumi.set(__self__, "actions_required", actions_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> Optional[pulumi.Input[str]]:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, "actions_required")

    @actions_required.setter
    def actions_required(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "actions_required", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The reason for approval/rejection of the connection.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]:
        """
        Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class RegistrationInfoArgs:
    def __init__(__self__, *,
                 expiration_time: Optional[pulumi.Input[str]] = None,
                 registration_token_operation: Optional[pulumi.Input[Union[str, 'RegistrationTokenOperation']]] = None,
                 token: Optional[pulumi.Input[str]] = None):
        """
        Represents a RegistrationInfo definition.
        :param pulumi.Input[str] expiration_time: Expiration time of registration token.
        :param pulumi.Input[Union[str, 'RegistrationTokenOperation']] registration_token_operation: The type of resetting the token.
        :param pulumi.Input[str] token: The registration token base64 encoded string.
        """
        if expiration_time is not None:
            pulumi.set(__self__, "expiration_time", expiration_time)
        if registration_token_operation is not None:
            pulumi.set(__self__, "registration_token_operation", registration_token_operation)
        if token is not None:
            pulumi.set(__self__, "token", token)

    @property
    @pulumi.getter(name="expirationTime")
    def expiration_time(self) -> Optional[pulumi.Input[str]]:
        """
        Expiration time of registration token.
        """
        return pulumi.get(self, "expiration_time")

    @expiration_time.setter
    def expiration_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expiration_time", value)

    @property
    @pulumi.getter(name="registrationTokenOperation")
    def registration_token_operation(self) -> Optional[pulumi.Input[Union[str, 'RegistrationTokenOperation']]]:
        """
        The type of resetting the token.
        """
        return pulumi.get(self, "registration_token_operation")

    @registration_token_operation.setter
    def registration_token_operation(self, value: Optional[pulumi.Input[Union[str, 'RegistrationTokenOperation']]]):
        pulumi.set(self, "registration_token_operation", value)

    @property
    @pulumi.getter
    def token(self) -> Optional[pulumi.Input[str]]:
        """
        The registration token base64 encoded string.
        """
        return pulumi.get(self, "token")

    @token.setter
    def token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token", value)


@pulumi.input_type
class ResourceModelWithAllowedPropertySetIdentityArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input['ResourceIdentityType']] = None):
        """
        :param pulumi.Input['ResourceIdentityType'] type: The identity type.
        """
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input['ResourceIdentityType']]:
        """
        The identity type.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input['ResourceIdentityType']]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class ResourceModelWithAllowedPropertySetPlanArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 product: pulumi.Input[str],
                 publisher: pulumi.Input[str],
                 promotion_code: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: A user defined name of the 3rd Party Artifact that is being procured.
        :param pulumi.Input[str] product: The 3rd Party artifact that is being procured. E.g. NewRelic. Product maps to the OfferID specified for the artifact at the time of Data Market onboarding. 
        :param pulumi.Input[str] publisher: The publisher of the 3rd Party Artifact that is being bought. E.g. NewRelic
        :param pulumi.Input[str] promotion_code: A publisher provided promotion code as provisioned in Data Market for the said product/artifact.
        :param pulumi.Input[str] version: The version of the desired product/artifact.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "product", product)
        pulumi.set(__self__, "publisher", publisher)
        if promotion_code is not None:
            pulumi.set(__self__, "promotion_code", promotion_code)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        A user defined name of the 3rd Party Artifact that is being procured.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def product(self) -> pulumi.Input[str]:
        """
        The 3rd Party artifact that is being procured. E.g. NewRelic. Product maps to the OfferID specified for the artifact at the time of Data Market onboarding. 
        """
        return pulumi.get(self, "product")

    @product.setter
    def product(self, value: pulumi.Input[str]):
        pulumi.set(self, "product", value)

    @property
    @pulumi.getter
    def publisher(self) -> pulumi.Input[str]:
        """
        The publisher of the 3rd Party Artifact that is being bought. E.g. NewRelic
        """
        return pulumi.get(self, "publisher")

    @publisher.setter
    def publisher(self, value: pulumi.Input[str]):
        pulumi.set(self, "publisher", value)

    @property
    @pulumi.getter(name="promotionCode")
    def promotion_code(self) -> Optional[pulumi.Input[str]]:
        """
        A publisher provided promotion code as provisioned in Data Market for the said product/artifact.
        """
        return pulumi.get(self, "promotion_code")

    @promotion_code.setter
    def promotion_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "promotion_code", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of the desired product/artifact.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class ResourceModelWithAllowedPropertySetSkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 capacity: Optional[pulumi.Input[int]] = None,
                 family: Optional[pulumi.Input[str]] = None,
                 size: Optional[pulumi.Input[str]] = None,
                 tier: Optional[pulumi.Input['SkuTier']] = None):
        """
        :param pulumi.Input[str] name: The name of the SKU. Ex - P3. It is typically a letter+number code
        :param pulumi.Input[int] capacity: If the SKU supports scale out/in then the capacity integer should be included. If scale out/in is not possible for the resource this may be omitted.
        :param pulumi.Input[str] family: If the service has different generations of hardware, for the same SKU, then that can be captured here.
        :param pulumi.Input[str] size: The SKU size. When the name field is the combination of tier and some other value, this would be the standalone code. 
        :param pulumi.Input['SkuTier'] tier: This field is required to be implemented by the Resource Provider if the service has more than one tier, but is not required on a PUT.
        """
        pulumi.set(__self__, "name", name)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if family is not None:
            pulumi.set(__self__, "family", family)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the SKU. Ex - P3. It is typically a letter+number code
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[int]]:
        """
        If the SKU supports scale out/in then the capacity integer should be included. If scale out/in is not possible for the resource this may be omitted.
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "capacity", value)

    @property
    @pulumi.getter
    def family(self) -> Optional[pulumi.Input[str]]:
        """
        If the service has different generations of hardware, for the same SKU, then that can be captured here.
        """
        return pulumi.get(self, "family")

    @family.setter
    def family(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "family", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[str]]:
        """
        The SKU size. When the name field is the combination of tier and some other value, this would be the standalone code. 
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input['SkuTier']]:
        """
        This field is required to be implemented by the Resource Provider if the service has more than one tier, but is not required on a PUT.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input['SkuTier']]):
        pulumi.set(self, "tier", value)


@pulumi.input_type
class ScalingHostPoolReferenceArgs:
    def __init__(__self__, *,
                 host_pool_arm_path: Optional[pulumi.Input[str]] = None,
                 scaling_plan_enabled: Optional[pulumi.Input[bool]] = None):
        """
        Scaling plan reference to hostpool.
        :param pulumi.Input[str] host_pool_arm_path: Arm path of referenced hostpool.
        :param pulumi.Input[bool] scaling_plan_enabled: Is the scaling plan enabled for this hostpool.
        """
        if host_pool_arm_path is not None:
            pulumi.set(__self__, "host_pool_arm_path", host_pool_arm_path)
        if scaling_plan_enabled is not None:
            pulumi.set(__self__, "scaling_plan_enabled", scaling_plan_enabled)

    @property
    @pulumi.getter(name="hostPoolArmPath")
    def host_pool_arm_path(self) -> Optional[pulumi.Input[str]]:
        """
        Arm path of referenced hostpool.
        """
        return pulumi.get(self, "host_pool_arm_path")

    @host_pool_arm_path.setter
    def host_pool_arm_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_pool_arm_path", value)

    @property
    @pulumi.getter(name="scalingPlanEnabled")
    def scaling_plan_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the scaling plan enabled for this hostpool.
        """
        return pulumi.get(self, "scaling_plan_enabled")

    @scaling_plan_enabled.setter
    def scaling_plan_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "scaling_plan_enabled", value)


@pulumi.input_type
class ScalingScheduleArgs:
    def __init__(__self__, *,
                 days_of_week: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 off_peak_load_balancing_algorithm: Optional[pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']]] = None,
                 off_peak_start_time: Optional[pulumi.Input[str]] = None,
                 peak_load_balancing_algorithm: Optional[pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']]] = None,
                 peak_start_time: Optional[pulumi.Input[str]] = None,
                 ramp_down_capacity_threshold_pct: Optional[pulumi.Input[int]] = None,
                 ramp_down_force_logoff_users: Optional[pulumi.Input[bool]] = None,
                 ramp_down_load_balancing_algorithm: Optional[pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']]] = None,
                 ramp_down_minimum_hosts_pct: Optional[pulumi.Input[int]] = None,
                 ramp_down_notification_message: Optional[pulumi.Input[str]] = None,
                 ramp_down_start_time: Optional[pulumi.Input[str]] = None,
                 ramp_down_stop_hosts_when: Optional[pulumi.Input[Union[str, 'StopHostsWhen']]] = None,
                 ramp_down_wait_time_minutes: Optional[pulumi.Input[int]] = None,
                 ramp_up_capacity_threshold_pct: Optional[pulumi.Input[int]] = None,
                 ramp_up_load_balancing_algorithm: Optional[pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']]] = None,
                 ramp_up_minimum_hosts_pct: Optional[pulumi.Input[int]] = None,
                 ramp_up_start_time: Optional[pulumi.Input[str]] = None):
        """
        Scaling plan schedule.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] days_of_week: Set of days of the week on which this schedule is active.
        :param pulumi.Input[str] name: Name of the scaling schedule.
        :param pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']] off_peak_load_balancing_algorithm: Load balancing algorithm for off-peak period.
        :param pulumi.Input[str] off_peak_start_time: Starting time for off-peak period.
        :param pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']] peak_load_balancing_algorithm: Load balancing algorithm for peak period.
        :param pulumi.Input[str] peak_start_time: Starting time for peak period.
        :param pulumi.Input[int] ramp_down_capacity_threshold_pct: Capacity threshold for ramp down period.
        :param pulumi.Input[bool] ramp_down_force_logoff_users: Should users be logged off forcefully from hosts.
        :param pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']] ramp_down_load_balancing_algorithm: Load balancing algorithm for ramp down period.
        :param pulumi.Input[int] ramp_down_minimum_hosts_pct: Minimum host percentage for ramp down period.
        :param pulumi.Input[str] ramp_down_notification_message: Notification message for users during ramp down period.
        :param pulumi.Input[str] ramp_down_start_time: Starting time for ramp down period.
        :param pulumi.Input[Union[str, 'StopHostsWhen']] ramp_down_stop_hosts_when: Specifies when to stop hosts during ramp down period.
        :param pulumi.Input[int] ramp_down_wait_time_minutes: Number of minutes to wait to stop hosts during ramp down period.
        :param pulumi.Input[int] ramp_up_capacity_threshold_pct: Capacity threshold for ramp up period.
        :param pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']] ramp_up_load_balancing_algorithm: Load balancing algorithm for ramp up period.
        :param pulumi.Input[int] ramp_up_minimum_hosts_pct: Minimum host percentage for ramp up period.
        :param pulumi.Input[str] ramp_up_start_time: Starting time for ramp up period.
        """
        if days_of_week is not None:
            pulumi.set(__self__, "days_of_week", days_of_week)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if off_peak_load_balancing_algorithm is not None:
            pulumi.set(__self__, "off_peak_load_balancing_algorithm", off_peak_load_balancing_algorithm)
        if off_peak_start_time is not None:
            pulumi.set(__self__, "off_peak_start_time", off_peak_start_time)
        if peak_load_balancing_algorithm is not None:
            pulumi.set(__self__, "peak_load_balancing_algorithm", peak_load_balancing_algorithm)
        if peak_start_time is not None:
            pulumi.set(__self__, "peak_start_time", peak_start_time)
        if ramp_down_capacity_threshold_pct is not None:
            pulumi.set(__self__, "ramp_down_capacity_threshold_pct", ramp_down_capacity_threshold_pct)
        if ramp_down_force_logoff_users is not None:
            pulumi.set(__self__, "ramp_down_force_logoff_users", ramp_down_force_logoff_users)
        if ramp_down_load_balancing_algorithm is not None:
            pulumi.set(__self__, "ramp_down_load_balancing_algorithm", ramp_down_load_balancing_algorithm)
        if ramp_down_minimum_hosts_pct is not None:
            pulumi.set(__self__, "ramp_down_minimum_hosts_pct", ramp_down_minimum_hosts_pct)
        if ramp_down_notification_message is not None:
            pulumi.set(__self__, "ramp_down_notification_message", ramp_down_notification_message)
        if ramp_down_start_time is not None:
            pulumi.set(__self__, "ramp_down_start_time", ramp_down_start_time)
        if ramp_down_stop_hosts_when is not None:
            pulumi.set(__self__, "ramp_down_stop_hosts_when", ramp_down_stop_hosts_when)
        if ramp_down_wait_time_minutes is not None:
            pulumi.set(__self__, "ramp_down_wait_time_minutes", ramp_down_wait_time_minutes)
        if ramp_up_capacity_threshold_pct is not None:
            pulumi.set(__self__, "ramp_up_capacity_threshold_pct", ramp_up_capacity_threshold_pct)
        if ramp_up_load_balancing_algorithm is not None:
            pulumi.set(__self__, "ramp_up_load_balancing_algorithm", ramp_up_load_balancing_algorithm)
        if ramp_up_minimum_hosts_pct is not None:
            pulumi.set(__self__, "ramp_up_minimum_hosts_pct", ramp_up_minimum_hosts_pct)
        if ramp_up_start_time is not None:
            pulumi.set(__self__, "ramp_up_start_time", ramp_up_start_time)

    @property
    @pulumi.getter(name="daysOfWeek")
    def days_of_week(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Set of days of the week on which this schedule is active.
        """
        return pulumi.get(self, "days_of_week")

    @days_of_week.setter
    def days_of_week(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "days_of_week", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the scaling schedule.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="offPeakLoadBalancingAlgorithm")
    def off_peak_load_balancing_algorithm(self) -> Optional[pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']]]:
        """
        Load balancing algorithm for off-peak period.
        """
        return pulumi.get(self, "off_peak_load_balancing_algorithm")

    @off_peak_load_balancing_algorithm.setter
    def off_peak_load_balancing_algorithm(self, value: Optional[pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']]]):
        pulumi.set(self, "off_peak_load_balancing_algorithm", value)

    @property
    @pulumi.getter(name="offPeakStartTime")
    def off_peak_start_time(self) -> Optional[pulumi.Input[str]]:
        """
        Starting time for off-peak period.
        """
        return pulumi.get(self, "off_peak_start_time")

    @off_peak_start_time.setter
    def off_peak_start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "off_peak_start_time", value)

    @property
    @pulumi.getter(name="peakLoadBalancingAlgorithm")
    def peak_load_balancing_algorithm(self) -> Optional[pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']]]:
        """
        Load balancing algorithm for peak period.
        """
        return pulumi.get(self, "peak_load_balancing_algorithm")

    @peak_load_balancing_algorithm.setter
    def peak_load_balancing_algorithm(self, value: Optional[pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']]]):
        pulumi.set(self, "peak_load_balancing_algorithm", value)

    @property
    @pulumi.getter(name="peakStartTime")
    def peak_start_time(self) -> Optional[pulumi.Input[str]]:
        """
        Starting time for peak period.
        """
        return pulumi.get(self, "peak_start_time")

    @peak_start_time.setter
    def peak_start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "peak_start_time", value)

    @property
    @pulumi.getter(name="rampDownCapacityThresholdPct")
    def ramp_down_capacity_threshold_pct(self) -> Optional[pulumi.Input[int]]:
        """
        Capacity threshold for ramp down period.
        """
        return pulumi.get(self, "ramp_down_capacity_threshold_pct")

    @ramp_down_capacity_threshold_pct.setter
    def ramp_down_capacity_threshold_pct(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ramp_down_capacity_threshold_pct", value)

    @property
    @pulumi.getter(name="rampDownForceLogoffUsers")
    def ramp_down_force_logoff_users(self) -> Optional[pulumi.Input[bool]]:
        """
        Should users be logged off forcefully from hosts.
        """
        return pulumi.get(self, "ramp_down_force_logoff_users")

    @ramp_down_force_logoff_users.setter
    def ramp_down_force_logoff_users(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ramp_down_force_logoff_users", value)

    @property
    @pulumi.getter(name="rampDownLoadBalancingAlgorithm")
    def ramp_down_load_balancing_algorithm(self) -> Optional[pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']]]:
        """
        Load balancing algorithm for ramp down period.
        """
        return pulumi.get(self, "ramp_down_load_balancing_algorithm")

    @ramp_down_load_balancing_algorithm.setter
    def ramp_down_load_balancing_algorithm(self, value: Optional[pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']]]):
        pulumi.set(self, "ramp_down_load_balancing_algorithm", value)

    @property
    @pulumi.getter(name="rampDownMinimumHostsPct")
    def ramp_down_minimum_hosts_pct(self) -> Optional[pulumi.Input[int]]:
        """
        Minimum host percentage for ramp down period.
        """
        return pulumi.get(self, "ramp_down_minimum_hosts_pct")

    @ramp_down_minimum_hosts_pct.setter
    def ramp_down_minimum_hosts_pct(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ramp_down_minimum_hosts_pct", value)

    @property
    @pulumi.getter(name="rampDownNotificationMessage")
    def ramp_down_notification_message(self) -> Optional[pulumi.Input[str]]:
        """
        Notification message for users during ramp down period.
        """
        return pulumi.get(self, "ramp_down_notification_message")

    @ramp_down_notification_message.setter
    def ramp_down_notification_message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ramp_down_notification_message", value)

    @property
    @pulumi.getter(name="rampDownStartTime")
    def ramp_down_start_time(self) -> Optional[pulumi.Input[str]]:
        """
        Starting time for ramp down period.
        """
        return pulumi.get(self, "ramp_down_start_time")

    @ramp_down_start_time.setter
    def ramp_down_start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ramp_down_start_time", value)

    @property
    @pulumi.getter(name="rampDownStopHostsWhen")
    def ramp_down_stop_hosts_when(self) -> Optional[pulumi.Input[Union[str, 'StopHostsWhen']]]:
        """
        Specifies when to stop hosts during ramp down period.
        """
        return pulumi.get(self, "ramp_down_stop_hosts_when")

    @ramp_down_stop_hosts_when.setter
    def ramp_down_stop_hosts_when(self, value: Optional[pulumi.Input[Union[str, 'StopHostsWhen']]]):
        pulumi.set(self, "ramp_down_stop_hosts_when", value)

    @property
    @pulumi.getter(name="rampDownWaitTimeMinutes")
    def ramp_down_wait_time_minutes(self) -> Optional[pulumi.Input[int]]:
        """
        Number of minutes to wait to stop hosts during ramp down period.
        """
        return pulumi.get(self, "ramp_down_wait_time_minutes")

    @ramp_down_wait_time_minutes.setter
    def ramp_down_wait_time_minutes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ramp_down_wait_time_minutes", value)

    @property
    @pulumi.getter(name="rampUpCapacityThresholdPct")
    def ramp_up_capacity_threshold_pct(self) -> Optional[pulumi.Input[int]]:
        """
        Capacity threshold for ramp up period.
        """
        return pulumi.get(self, "ramp_up_capacity_threshold_pct")

    @ramp_up_capacity_threshold_pct.setter
    def ramp_up_capacity_threshold_pct(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ramp_up_capacity_threshold_pct", value)

    @property
    @pulumi.getter(name="rampUpLoadBalancingAlgorithm")
    def ramp_up_load_balancing_algorithm(self) -> Optional[pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']]]:
        """
        Load balancing algorithm for ramp up period.
        """
        return pulumi.get(self, "ramp_up_load_balancing_algorithm")

    @ramp_up_load_balancing_algorithm.setter
    def ramp_up_load_balancing_algorithm(self, value: Optional[pulumi.Input[Union[str, 'SessionHostLoadBalancingAlgorithm']]]):
        pulumi.set(self, "ramp_up_load_balancing_algorithm", value)

    @property
    @pulumi.getter(name="rampUpMinimumHostsPct")
    def ramp_up_minimum_hosts_pct(self) -> Optional[pulumi.Input[int]]:
        """
        Minimum host percentage for ramp up period.
        """
        return pulumi.get(self, "ramp_up_minimum_hosts_pct")

    @ramp_up_minimum_hosts_pct.setter
    def ramp_up_minimum_hosts_pct(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ramp_up_minimum_hosts_pct", value)

    @property
    @pulumi.getter(name="rampUpStartTime")
    def ramp_up_start_time(self) -> Optional[pulumi.Input[str]]:
        """
        Starting time for ramp up period.
        """
        return pulumi.get(self, "ramp_up_start_time")

    @ramp_up_start_time.setter
    def ramp_up_start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ramp_up_start_time", value)


@pulumi.input_type
class TimeArgs:
    def __init__(__self__, *,
                 hour: pulumi.Input[int],
                 minute: pulumi.Input[int]):
        """
        The time for a scaling action to occur.
        :param pulumi.Input[int] hour: The hour.
        :param pulumi.Input[int] minute: The minute.
        """
        pulumi.set(__self__, "hour", hour)
        pulumi.set(__self__, "minute", minute)

    @property
    @pulumi.getter
    def hour(self) -> pulumi.Input[int]:
        """
        The hour.
        """
        return pulumi.get(self, "hour")

    @hour.setter
    def hour(self, value: pulumi.Input[int]):
        pulumi.set(self, "hour", value)

    @property
    @pulumi.getter
    def minute(self) -> pulumi.Input[int]:
        """
        The minute.
        """
        return pulumi.get(self, "minute")

    @minute.setter
    def minute(self, value: pulumi.Input[int]):
        pulumi.set(self, "minute", value)


