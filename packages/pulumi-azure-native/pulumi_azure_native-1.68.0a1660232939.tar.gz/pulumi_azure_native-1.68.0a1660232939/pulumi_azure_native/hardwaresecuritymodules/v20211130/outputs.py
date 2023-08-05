# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'ApiEntityReferenceResponse',
    'NetworkInterfaceResponse',
    'NetworkProfileResponse',
    'SkuResponse',
    'SystemDataResponse',
]

@pulumi.output_type
class ApiEntityReferenceResponse(dict):
    """
    The API entity reference.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        The API entity reference.
        :param str id: The ARM resource id in the form of /subscriptions/{SubscriptionId}/resourceGroups/{ResourceGroupName}/...
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ARM resource id in the form of /subscriptions/{SubscriptionId}/resourceGroups/{ResourceGroupName}/...
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class NetworkInterfaceResponse(dict):
    """
    The network interface definition.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "privateIpAddress":
            suggest = "private_ip_address"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in NetworkInterfaceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        NetworkInterfaceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        NetworkInterfaceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: str,
                 private_ip_address: Optional[str] = None):
        """
        The network interface definition.
        :param str id: The ARM resource id in the form of /subscriptions/{SubscriptionId}/resourceGroups/{ResourceGroupName}/...
        :param str private_ip_address: Private Ip address of the interface
        """
        pulumi.set(__self__, "id", id)
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ARM resource id in the form of /subscriptions/{SubscriptionId}/resourceGroups/{ResourceGroupName}/...
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> Optional[str]:
        """
        Private Ip address of the interface
        """
        return pulumi.get(self, "private_ip_address")


@pulumi.output_type
class NetworkProfileResponse(dict):
    """
    The network profile definition.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "networkInterfaces":
            suggest = "network_interfaces"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in NetworkProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        NetworkProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        NetworkProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 network_interfaces: Optional[Sequence['outputs.NetworkInterfaceResponse']] = None,
                 subnet: Optional['outputs.ApiEntityReferenceResponse'] = None):
        """
        The network profile definition.
        :param Sequence['NetworkInterfaceResponse'] network_interfaces: Specifies the list of resource Ids for the network interfaces associated with the dedicated HSM.
        :param 'ApiEntityReferenceResponse' subnet: Specifies the identifier of the subnet.
        """
        if network_interfaces is not None:
            pulumi.set(__self__, "network_interfaces", network_interfaces)
        if subnet is not None:
            pulumi.set(__self__, "subnet", subnet)

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Optional[Sequence['outputs.NetworkInterfaceResponse']]:
        """
        Specifies the list of resource Ids for the network interfaces associated with the dedicated HSM.
        """
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter
    def subnet(self) -> Optional['outputs.ApiEntityReferenceResponse']:
        """
        Specifies the identifier of the subnet.
        """
        return pulumi.get(self, "subnet")


@pulumi.output_type
class SkuResponse(dict):
    """
    SKU of the dedicated HSM
    """
    def __init__(__self__, *,
                 name: Optional[str] = None):
        """
        SKU of the dedicated HSM
        :param str name: SKU of the dedicated HSM
        """
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        SKU of the dedicated HSM
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of dedicated hsm resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdAt":
            suggest = "created_at"
        elif key == "createdBy":
            suggest = "created_by"
        elif key == "createdByType":
            suggest = "created_by_type"
        elif key == "lastModifiedAt":
            suggest = "last_modified_at"
        elif key == "lastModifiedBy":
            suggest = "last_modified_by"
        elif key == "lastModifiedByType":
            suggest = "last_modified_by_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SystemDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 created_by: Optional[str] = None,
                 created_by_type: Optional[str] = None,
                 last_modified_at: Optional[str] = None,
                 last_modified_by: Optional[str] = None,
                 last_modified_by_type: Optional[str] = None):
        """
        Metadata pertaining to creation and last modification of dedicated hsm resource.
        :param str created_at: The timestamp of dedicated hsm resource creation (UTC).
        :param str created_by: The identity that created dedicated hsm resource.
        :param str created_by_type: The type of identity that created dedicated hsm resource.
        :param str last_modified_at: The timestamp of dedicated hsm resource last modification (UTC).
        :param str last_modified_by: The identity that last modified dedicated hsm resource.
        :param str last_modified_by_type: The type of identity that last modified dedicated hsm resource.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if created_by_type is not None:
            pulumi.set(__self__, "created_by_type", created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of dedicated hsm resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created dedicated hsm resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created dedicated hsm resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of dedicated hsm resource last modification (UTC).
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified dedicated hsm resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified dedicated hsm resource.
        """
        return pulumi.get(self, "last_modified_by_type")


