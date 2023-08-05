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
    'AADAppArgs',
    'AdminCredentialsArgs',
    'BackupArgs',
    'HighAvailabilityArgs',
    'IdentityArgs',
    'MaintenanceWindowArgs',
    'MigrationResourceGroupArgs',
    'MigrationSecretParametersArgs',
    'NetworkArgs',
    'SkuArgs',
    'StorageArgs',
]

@pulumi.input_type
class AADAppArgs:
    def __init__(__self__, *,
                 aad_secret: pulumi.Input[str],
                 client_id: pulumi.Input[str],
                 tenant_id: pulumi.Input[str]):
        """
        Azure active directory application.
        """
        pulumi.set(__self__, "aad_secret", aad_secret)
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter(name="aadSecret")
    def aad_secret(self) -> pulumi.Input[str]:
        return pulumi.get(self, "aad_secret")

    @aad_secret.setter
    def aad_secret(self, value: pulumi.Input[str]):
        pulumi.set(self, "aad_secret", value)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "tenant_id", value)


@pulumi.input_type
class AdminCredentialsArgs:
    def __init__(__self__, *,
                 source_server_password: pulumi.Input[str],
                 target_server_password: pulumi.Input[str]):
        """
        Server admin credentials.
        """
        pulumi.set(__self__, "source_server_password", source_server_password)
        pulumi.set(__self__, "target_server_password", target_server_password)

    @property
    @pulumi.getter(name="sourceServerPassword")
    def source_server_password(self) -> pulumi.Input[str]:
        return pulumi.get(self, "source_server_password")

    @source_server_password.setter
    def source_server_password(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_server_password", value)

    @property
    @pulumi.getter(name="targetServerPassword")
    def target_server_password(self) -> pulumi.Input[str]:
        return pulumi.get(self, "target_server_password")

    @target_server_password.setter
    def target_server_password(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_server_password", value)


@pulumi.input_type
class BackupArgs:
    def __init__(__self__, *,
                 backup_retention_days: Optional[pulumi.Input[int]] = None,
                 geo_redundant_backup: Optional[pulumi.Input[Union[str, 'GeoRedundantBackupEnum']]] = None):
        """
        Backup properties of a server
        :param pulumi.Input[int] backup_retention_days: Backup retention days for the server.
        :param pulumi.Input[Union[str, 'GeoRedundantBackupEnum']] geo_redundant_backup: A value indicating whether Geo-Redundant backup is enabled on the server.
        """
        if backup_retention_days is not None:
            pulumi.set(__self__, "backup_retention_days", backup_retention_days)
        if geo_redundant_backup is not None:
            pulumi.set(__self__, "geo_redundant_backup", geo_redundant_backup)

    @property
    @pulumi.getter(name="backupRetentionDays")
    def backup_retention_days(self) -> Optional[pulumi.Input[int]]:
        """
        Backup retention days for the server.
        """
        return pulumi.get(self, "backup_retention_days")

    @backup_retention_days.setter
    def backup_retention_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "backup_retention_days", value)

    @property
    @pulumi.getter(name="geoRedundantBackup")
    def geo_redundant_backup(self) -> Optional[pulumi.Input[Union[str, 'GeoRedundantBackupEnum']]]:
        """
        A value indicating whether Geo-Redundant backup is enabled on the server.
        """
        return pulumi.get(self, "geo_redundant_backup")

    @geo_redundant_backup.setter
    def geo_redundant_backup(self, value: Optional[pulumi.Input[Union[str, 'GeoRedundantBackupEnum']]]):
        pulumi.set(self, "geo_redundant_backup", value)


@pulumi.input_type
class HighAvailabilityArgs:
    def __init__(__self__, *,
                 mode: Optional[pulumi.Input[Union[str, 'HighAvailabilityMode']]] = None,
                 standby_availability_zone: Optional[pulumi.Input[str]] = None):
        """
        High availability properties of a server
        :param pulumi.Input[Union[str, 'HighAvailabilityMode']] mode: The HA mode for the server.
        :param pulumi.Input[str] standby_availability_zone: availability zone information of the standby.
        """
        if mode is not None:
            pulumi.set(__self__, "mode", mode)
        if standby_availability_zone is not None:
            pulumi.set(__self__, "standby_availability_zone", standby_availability_zone)

    @property
    @pulumi.getter
    def mode(self) -> Optional[pulumi.Input[Union[str, 'HighAvailabilityMode']]]:
        """
        The HA mode for the server.
        """
        return pulumi.get(self, "mode")

    @mode.setter
    def mode(self, value: Optional[pulumi.Input[Union[str, 'HighAvailabilityMode']]]):
        pulumi.set(self, "mode", value)

    @property
    @pulumi.getter(name="standbyAvailabilityZone")
    def standby_availability_zone(self) -> Optional[pulumi.Input[str]]:
        """
        availability zone information of the standby.
        """
        return pulumi.get(self, "standby_availability_zone")

    @standby_availability_zone.setter
    def standby_availability_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "standby_availability_zone", value)


@pulumi.input_type
class IdentityArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input['ResourceIdentityType']] = None):
        """
        Identity for the resource.
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
class MaintenanceWindowArgs:
    def __init__(__self__, *,
                 custom_window: Optional[pulumi.Input[str]] = None,
                 day_of_week: Optional[pulumi.Input[int]] = None,
                 start_hour: Optional[pulumi.Input[int]] = None,
                 start_minute: Optional[pulumi.Input[int]] = None):
        """
        Maintenance window properties of a server.
        :param pulumi.Input[str] custom_window: indicates whether custom window is enabled or disabled
        :param pulumi.Input[int] day_of_week: day of week for maintenance window
        :param pulumi.Input[int] start_hour: start hour for maintenance window
        :param pulumi.Input[int] start_minute: start minute for maintenance window
        """
        if custom_window is not None:
            pulumi.set(__self__, "custom_window", custom_window)
        if day_of_week is not None:
            pulumi.set(__self__, "day_of_week", day_of_week)
        if start_hour is not None:
            pulumi.set(__self__, "start_hour", start_hour)
        if start_minute is not None:
            pulumi.set(__self__, "start_minute", start_minute)

    @property
    @pulumi.getter(name="customWindow")
    def custom_window(self) -> Optional[pulumi.Input[str]]:
        """
        indicates whether custom window is enabled or disabled
        """
        return pulumi.get(self, "custom_window")

    @custom_window.setter
    def custom_window(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_window", value)

    @property
    @pulumi.getter(name="dayOfWeek")
    def day_of_week(self) -> Optional[pulumi.Input[int]]:
        """
        day of week for maintenance window
        """
        return pulumi.get(self, "day_of_week")

    @day_of_week.setter
    def day_of_week(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "day_of_week", value)

    @property
    @pulumi.getter(name="startHour")
    def start_hour(self) -> Optional[pulumi.Input[int]]:
        """
        start hour for maintenance window
        """
        return pulumi.get(self, "start_hour")

    @start_hour.setter
    def start_hour(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "start_hour", value)

    @property
    @pulumi.getter(name="startMinute")
    def start_minute(self) -> Optional[pulumi.Input[int]]:
        """
        start minute for maintenance window
        """
        return pulumi.get(self, "start_minute")

    @start_minute.setter
    def start_minute(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "start_minute", value)


@pulumi.input_type
class MigrationResourceGroupArgs:
    def __init__(__self__, *,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 subnet_resource_id: Optional[pulumi.Input[str]] = None):
        """
        Migration resource group.
        """
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)
        if subnet_resource_id is not None:
            pulumi.set(__self__, "subnet_resource_id", subnet_resource_id)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id", value)

    @property
    @pulumi.getter(name="subnetResourceId")
    def subnet_resource_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "subnet_resource_id")

    @subnet_resource_id.setter
    def subnet_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_resource_id", value)


@pulumi.input_type
class MigrationSecretParametersArgs:
    def __init__(__self__, *,
                 aad_app: pulumi.Input['AADAppArgs'],
                 admin_credentials: pulumi.Input['AdminCredentialsArgs']):
        """
        Migration secret parameters.
        :param pulumi.Input['AADAppArgs'] aad_app: Azure active directory application.
        :param pulumi.Input['AdminCredentialsArgs'] admin_credentials: Server admin credentials.
        """
        pulumi.set(__self__, "aad_app", aad_app)
        pulumi.set(__self__, "admin_credentials", admin_credentials)

    @property
    @pulumi.getter(name="aadApp")
    def aad_app(self) -> pulumi.Input['AADAppArgs']:
        """
        Azure active directory application.
        """
        return pulumi.get(self, "aad_app")

    @aad_app.setter
    def aad_app(self, value: pulumi.Input['AADAppArgs']):
        pulumi.set(self, "aad_app", value)

    @property
    @pulumi.getter(name="adminCredentials")
    def admin_credentials(self) -> pulumi.Input['AdminCredentialsArgs']:
        """
        Server admin credentials.
        """
        return pulumi.get(self, "admin_credentials")

    @admin_credentials.setter
    def admin_credentials(self, value: pulumi.Input['AdminCredentialsArgs']):
        pulumi.set(self, "admin_credentials", value)


@pulumi.input_type
class NetworkArgs:
    def __init__(__self__, *,
                 delegated_subnet_resource_id: Optional[pulumi.Input[str]] = None,
                 private_dns_zone_arm_resource_id: Optional[pulumi.Input[str]] = None):
        """
        Network properties of a server
        :param pulumi.Input[str] delegated_subnet_resource_id: delegated subnet arm resource id.
        :param pulumi.Input[str] private_dns_zone_arm_resource_id: private dns zone arm resource id.
        """
        if delegated_subnet_resource_id is not None:
            pulumi.set(__self__, "delegated_subnet_resource_id", delegated_subnet_resource_id)
        if private_dns_zone_arm_resource_id is not None:
            pulumi.set(__self__, "private_dns_zone_arm_resource_id", private_dns_zone_arm_resource_id)

    @property
    @pulumi.getter(name="delegatedSubnetResourceId")
    def delegated_subnet_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        delegated subnet arm resource id.
        """
        return pulumi.get(self, "delegated_subnet_resource_id")

    @delegated_subnet_resource_id.setter
    def delegated_subnet_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delegated_subnet_resource_id", value)

    @property
    @pulumi.getter(name="privateDnsZoneArmResourceId")
    def private_dns_zone_arm_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        private dns zone arm resource id.
        """
        return pulumi.get(self, "private_dns_zone_arm_resource_id")

    @private_dns_zone_arm_resource_id.setter
    def private_dns_zone_arm_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_dns_zone_arm_resource_id", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 tier: pulumi.Input[Union[str, 'SkuTier']]):
        """
        Sku information related properties of a server.
        :param pulumi.Input[str] name: The name of the sku, typically, tier + family + cores, e.g. Standard_D4s_v3.
        :param pulumi.Input[Union[str, 'SkuTier']] tier: The tier of the particular SKU, e.g. Burstable.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the sku, typically, tier + family + cores, e.g. Standard_D4s_v3.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tier(self) -> pulumi.Input[Union[str, 'SkuTier']]:
        """
        The tier of the particular SKU, e.g. Burstable.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: pulumi.Input[Union[str, 'SkuTier']]):
        pulumi.set(self, "tier", value)


@pulumi.input_type
class StorageArgs:
    def __init__(__self__, *,
                 storage_size_gb: Optional[pulumi.Input[int]] = None):
        """
        Storage properties of a server
        :param pulumi.Input[int] storage_size_gb: Max storage allowed for a server.
        """
        if storage_size_gb is not None:
            pulumi.set(__self__, "storage_size_gb", storage_size_gb)

    @property
    @pulumi.getter(name="storageSizeGB")
    def storage_size_gb(self) -> Optional[pulumi.Input[int]]:
        """
        Max storage allowed for a server.
        """
        return pulumi.get(self, "storage_size_gb")

    @storage_size_gb.setter
    def storage_size_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "storage_size_gb", value)


