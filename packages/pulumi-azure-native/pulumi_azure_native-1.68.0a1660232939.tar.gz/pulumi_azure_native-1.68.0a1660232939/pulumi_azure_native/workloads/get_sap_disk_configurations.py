# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'GetSAPDiskConfigurationsResult',
    'AwaitableGetSAPDiskConfigurationsResult',
    'get_sap_disk_configurations',
    'get_sap_disk_configurations_output',
]

@pulumi.output_type
class GetSAPDiskConfigurationsResult:
    """
    The list of disk configuration for vmSku which are part of SAP deployment.
    """
    def __init__(__self__, disk_configurations=None):
        if disk_configurations and not isinstance(disk_configurations, list):
            raise TypeError("Expected argument 'disk_configurations' to be a list")
        pulumi.set(__self__, "disk_configurations", disk_configurations)

    @property
    @pulumi.getter(name="diskConfigurations")
    def disk_configurations(self) -> Optional[Sequence['outputs.SAPDiskConfigurationResponse']]:
        """
        Gets the list of Disk Configurations.
        """
        return pulumi.get(self, "disk_configurations")


class AwaitableGetSAPDiskConfigurationsResult(GetSAPDiskConfigurationsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSAPDiskConfigurationsResult(
            disk_configurations=self.disk_configurations)


def get_sap_disk_configurations(app_location: Optional[str] = None,
                                database_type: Optional[Union[str, 'SAPDatabaseType']] = None,
                                db_vm_sku: Optional[str] = None,
                                deployment_type: Optional[Union[str, 'SAPDeploymentType']] = None,
                                environment: Optional[Union[str, 'SAPEnvironmentType']] = None,
                                location: Optional[str] = None,
                                sap_product: Optional[Union[str, 'SAPProductType']] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSAPDiskConfigurationsResult:
    """
    The list of disk configuration for vmSku which are part of SAP deployment.
    API Version: 2021-12-01-preview.


    :param str app_location: The geo-location where the SAP resources will be created.
    :param Union[str, 'SAPDatabaseType'] database_type: The database type. Eg: HANA, DB2, etc
    :param str db_vm_sku: The VM SKU for database instance.
    :param Union[str, 'SAPDeploymentType'] deployment_type: The deployment type. Eg: SingleServer/ThreeTier
    :param Union[str, 'SAPEnvironmentType'] environment: Defines the environment type - Production/Non Production.
    :param str location: The name of Azure region.
    :param Union[str, 'SAPProductType'] sap_product: Defines the SAP Product type.
    """
    __args__ = dict()
    __args__['appLocation'] = app_location
    __args__['databaseType'] = database_type
    __args__['dbVmSku'] = db_vm_sku
    __args__['deploymentType'] = deployment_type
    __args__['environment'] = environment
    __args__['location'] = location
    __args__['sapProduct'] = sap_product
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:workloads:getSAPDiskConfigurations', __args__, opts=opts, typ=GetSAPDiskConfigurationsResult).value

    return AwaitableGetSAPDiskConfigurationsResult(
        disk_configurations=__ret__.disk_configurations)


@_utilities.lift_output_func(get_sap_disk_configurations)
def get_sap_disk_configurations_output(app_location: Optional[pulumi.Input[str]] = None,
                                       database_type: Optional[pulumi.Input[Union[str, 'SAPDatabaseType']]] = None,
                                       db_vm_sku: Optional[pulumi.Input[str]] = None,
                                       deployment_type: Optional[pulumi.Input[Union[str, 'SAPDeploymentType']]] = None,
                                       environment: Optional[pulumi.Input[Union[str, 'SAPEnvironmentType']]] = None,
                                       location: Optional[pulumi.Input[str]] = None,
                                       sap_product: Optional[pulumi.Input[Union[str, 'SAPProductType']]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSAPDiskConfigurationsResult]:
    """
    The list of disk configuration for vmSku which are part of SAP deployment.
    API Version: 2021-12-01-preview.


    :param str app_location: The geo-location where the SAP resources will be created.
    :param Union[str, 'SAPDatabaseType'] database_type: The database type. Eg: HANA, DB2, etc
    :param str db_vm_sku: The VM SKU for database instance.
    :param Union[str, 'SAPDeploymentType'] deployment_type: The deployment type. Eg: SingleServer/ThreeTier
    :param Union[str, 'SAPEnvironmentType'] environment: Defines the environment type - Production/Non Production.
    :param str location: The name of Azure region.
    :param Union[str, 'SAPProductType'] sap_product: Defines the SAP Product type.
    """
    ...
