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
    'ClusterJobResponse',
    'ClusterPropertiesResponse',
    'ClusterSkuResponse',
    'PrivateEndpointPropertiesResponse',
    'PrivateLinkConnectionStateResponse',
    'PrivateLinkServiceConnectionResponse',
]

@pulumi.output_type
class ClusterJobResponse(dict):
    """
    A streaming job.
    """
    def __init__(__self__, *,
                 id: str,
                 job_state: str,
                 streaming_units: int):
        """
        A streaming job.
        :param str id: Resource ID of the streaming job.
        :param str job_state: The current execution state of the streaming job.
        :param int streaming_units: The number of streaming units that are used by the streaming job.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "job_state", job_state)
        pulumi.set(__self__, "streaming_units", streaming_units)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID of the streaming job.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="jobState")
    def job_state(self) -> str:
        """
        The current execution state of the streaming job.
        """
        return pulumi.get(self, "job_state")

    @property
    @pulumi.getter(name="streamingUnits")
    def streaming_units(self) -> int:
        """
        The number of streaming units that are used by the streaming job.
        """
        return pulumi.get(self, "streaming_units")


@pulumi.output_type
class ClusterPropertiesResponse(dict):
    """
    The properties associated with a Stream Analytics cluster.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "capacityAllocated":
            suggest = "capacity_allocated"
        elif key == "capacityAssigned":
            suggest = "capacity_assigned"
        elif key == "clusterId":
            suggest = "cluster_id"
        elif key == "createdDate":
            suggest = "created_date"
        elif key == "provisioningState":
            suggest = "provisioning_state"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ClusterPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ClusterPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ClusterPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 capacity_allocated: int,
                 capacity_assigned: int,
                 cluster_id: str,
                 created_date: str,
                 provisioning_state: str):
        """
        The properties associated with a Stream Analytics cluster.
        :param int capacity_allocated: Represents the number of streaming units currently being used on the cluster.
        :param int capacity_assigned: Represents the sum of the SUs of all streaming jobs associated with the cluster. If all of the jobs were running, this would be the capacity allocated.
        :param str cluster_id: Unique identifier for the cluster.
        :param str created_date: The date this cluster was created.
        :param str provisioning_state: The status of the cluster provisioning. The three terminal states are: Succeeded, Failed and Canceled
        """
        pulumi.set(__self__, "capacity_allocated", capacity_allocated)
        pulumi.set(__self__, "capacity_assigned", capacity_assigned)
        pulumi.set(__self__, "cluster_id", cluster_id)
        pulumi.set(__self__, "created_date", created_date)
        pulumi.set(__self__, "provisioning_state", provisioning_state)

    @property
    @pulumi.getter(name="capacityAllocated")
    def capacity_allocated(self) -> int:
        """
        Represents the number of streaming units currently being used on the cluster.
        """
        return pulumi.get(self, "capacity_allocated")

    @property
    @pulumi.getter(name="capacityAssigned")
    def capacity_assigned(self) -> int:
        """
        Represents the sum of the SUs of all streaming jobs associated with the cluster. If all of the jobs were running, this would be the capacity allocated.
        """
        return pulumi.get(self, "capacity_assigned")

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> str:
        """
        Unique identifier for the cluster.
        """
        return pulumi.get(self, "cluster_id")

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> str:
        """
        The date this cluster was created.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The status of the cluster provisioning. The three terminal states are: Succeeded, Failed and Canceled
        """
        return pulumi.get(self, "provisioning_state")


@pulumi.output_type
class ClusterSkuResponse(dict):
    """
    The SKU of the cluster. This determines the size/capacity of the cluster. Required on PUT (CreateOrUpdate) requests.
    """
    def __init__(__self__, *,
                 capacity: Optional[int] = None,
                 name: Optional[str] = None):
        """
        The SKU of the cluster. This determines the size/capacity of the cluster. Required on PUT (CreateOrUpdate) requests.
        :param int capacity: Denotes the number of streaming units the cluster can support. Valid values for this property are multiples of 36 with a minimum value of 36 and maximum value of 216. Required on PUT (CreateOrUpdate) requests.
        :param str name: Specifies the SKU name of the cluster. Required on PUT (CreateOrUpdate) requests.
        """
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[int]:
        """
        Denotes the number of streaming units the cluster can support. Valid values for this property are multiples of 36 with a minimum value of 36 and maximum value of 216. Required on PUT (CreateOrUpdate) requests.
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Specifies the SKU name of the cluster. Required on PUT (CreateOrUpdate) requests.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class PrivateEndpointPropertiesResponse(dict):
    """
    The properties associated with a private endpoint.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdDate":
            suggest = "created_date"
        elif key == "manualPrivateLinkServiceConnections":
            suggest = "manual_private_link_service_connections"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateEndpointPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateEndpointPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PrivateEndpointPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_date: str,
                 manual_private_link_service_connections: Optional[Sequence['outputs.PrivateLinkServiceConnectionResponse']] = None):
        """
        The properties associated with a private endpoint.
        :param str created_date: The date when this private endpoint was created.
        :param Sequence['PrivateLinkServiceConnectionResponse'] manual_private_link_service_connections: A list of connections to the remote resource. Immutable after it is set.
        """
        pulumi.set(__self__, "created_date", created_date)
        if manual_private_link_service_connections is not None:
            pulumi.set(__self__, "manual_private_link_service_connections", manual_private_link_service_connections)

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> str:
        """
        The date when this private endpoint was created.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter(name="manualPrivateLinkServiceConnections")
    def manual_private_link_service_connections(self) -> Optional[Sequence['outputs.PrivateLinkServiceConnectionResponse']]:
        """
        A list of connections to the remote resource. Immutable after it is set.
        """
        return pulumi.get(self, "manual_private_link_service_connections")


@pulumi.output_type
class PrivateLinkConnectionStateResponse(dict):
    """
    A collection of read-only information about the state of the connection to the private remote resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "actionsRequired":
            suggest = "actions_required"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateLinkConnectionStateResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateLinkConnectionStateResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PrivateLinkConnectionStateResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 actions_required: str,
                 description: str,
                 status: str):
        """
        A collection of read-only information about the state of the connection to the private remote resource.
        :param str actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param str description: The reason for approval/rejection of the connection.
        :param str status: Indicates whether the connection has been Approved/Rejected/Removed by the owner of the remote resource/service.
        """
        pulumi.set(__self__, "actions_required", actions_required)
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> str:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, "actions_required")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The reason for approval/rejection of the connection.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Indicates whether the connection has been Approved/Rejected/Removed by the owner of the remote resource/service.
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class PrivateLinkServiceConnectionResponse(dict):
    """
    A grouping of information about the connection to the remote resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "requestMessage":
            suggest = "request_message"
        elif key == "groupIds":
            suggest = "group_ids"
        elif key == "privateLinkServiceConnectionState":
            suggest = "private_link_service_connection_state"
        elif key == "privateLinkServiceId":
            suggest = "private_link_service_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateLinkServiceConnectionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateLinkServiceConnectionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PrivateLinkServiceConnectionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 request_message: str,
                 group_ids: Optional[Sequence[str]] = None,
                 private_link_service_connection_state: Optional['outputs.PrivateLinkConnectionStateResponse'] = None,
                 private_link_service_id: Optional[str] = None):
        """
        A grouping of information about the connection to the remote resource.
        :param str request_message: A message passed to the owner of the remote resource with this connection request. Restricted to 140 chars.
        :param Sequence[str] group_ids: The ID(s) of the group(s) obtained from the remote resource that this private endpoint should connect to. Required on PUT (CreateOrUpdate) requests.
        :param 'PrivateLinkConnectionStateResponse' private_link_service_connection_state: A collection of read-only information about the state of the connection to the private remote resource.
        :param str private_link_service_id: The resource id of the private link service. Required on PUT (CreateOrUpdate) requests.
        """
        pulumi.set(__self__, "request_message", request_message)
        if group_ids is not None:
            pulumi.set(__self__, "group_ids", group_ids)
        if private_link_service_connection_state is not None:
            pulumi.set(__self__, "private_link_service_connection_state", private_link_service_connection_state)
        if private_link_service_id is not None:
            pulumi.set(__self__, "private_link_service_id", private_link_service_id)

    @property
    @pulumi.getter(name="requestMessage")
    def request_message(self) -> str:
        """
        A message passed to the owner of the remote resource with this connection request. Restricted to 140 chars.
        """
        return pulumi.get(self, "request_message")

    @property
    @pulumi.getter(name="groupIds")
    def group_ids(self) -> Optional[Sequence[str]]:
        """
        The ID(s) of the group(s) obtained from the remote resource that this private endpoint should connect to. Required on PUT (CreateOrUpdate) requests.
        """
        return pulumi.get(self, "group_ids")

    @property
    @pulumi.getter(name="privateLinkServiceConnectionState")
    def private_link_service_connection_state(self) -> Optional['outputs.PrivateLinkConnectionStateResponse']:
        """
        A collection of read-only information about the state of the connection to the private remote resource.
        """
        return pulumi.get(self, "private_link_service_connection_state")

    @property
    @pulumi.getter(name="privateLinkServiceId")
    def private_link_service_id(self) -> Optional[str]:
        """
        The resource id of the private link service. Required on PUT (CreateOrUpdate) requests.
        """
        return pulumi.get(self, "private_link_service_id")


