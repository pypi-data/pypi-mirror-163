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
    'AccountResourceResponseProperties',
    'CorsRuleResponse',
    'EndpointAuthenticationResponse',
    'ModelingInputDataResponse',
    'ModelingResourceResponseProperties',
    'ServiceEndpointResourceResponseProperties',
    'SystemDataResponse',
]

@pulumi.output_type
class AccountResourceResponseProperties(dict):
    """
    Account resource properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "endpointAuthentications":
            suggest = "endpoint_authentications"
        elif key == "reportsConnectionString":
            suggest = "reports_connection_string"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccountResourceResponseProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccountResourceResponseProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccountResourceResponseProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 provisioning_state: str,
                 configuration: Optional[str] = None,
                 cors: Optional[Sequence['outputs.CorsRuleResponse']] = None,
                 endpoint_authentications: Optional[Sequence['outputs.EndpointAuthenticationResponse']] = None,
                 reports_connection_string: Optional[str] = None):
        """
        Account resource properties.
        :param str provisioning_state: The resource provisioning state.
        :param str configuration: Account configuration. This can only be set at RecommendationsService Account creation.
        :param Sequence['CorsRuleResponse'] cors: The list of CORS details.
        :param Sequence['EndpointAuthenticationResponse'] endpoint_authentications: The list of service endpoints authentication details.
        :param str reports_connection_string: Connection string to write Accounts reports to.
        """
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if configuration is not None:
            pulumi.set(__self__, "configuration", configuration)
        if cors is not None:
            pulumi.set(__self__, "cors", cors)
        if endpoint_authentications is not None:
            pulumi.set(__self__, "endpoint_authentications", endpoint_authentications)
        if reports_connection_string is not None:
            pulumi.set(__self__, "reports_connection_string", reports_connection_string)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The resource provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def configuration(self) -> Optional[str]:
        """
        Account configuration. This can only be set at RecommendationsService Account creation.
        """
        return pulumi.get(self, "configuration")

    @property
    @pulumi.getter
    def cors(self) -> Optional[Sequence['outputs.CorsRuleResponse']]:
        """
        The list of CORS details.
        """
        return pulumi.get(self, "cors")

    @property
    @pulumi.getter(name="endpointAuthentications")
    def endpoint_authentications(self) -> Optional[Sequence['outputs.EndpointAuthenticationResponse']]:
        """
        The list of service endpoints authentication details.
        """
        return pulumi.get(self, "endpoint_authentications")

    @property
    @pulumi.getter(name="reportsConnectionString")
    def reports_connection_string(self) -> Optional[str]:
        """
        Connection string to write Accounts reports to.
        """
        return pulumi.get(self, "reports_connection_string")


@pulumi.output_type
class CorsRuleResponse(dict):
    """
    CORS details.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "allowedOrigins":
            suggest = "allowed_origins"
        elif key == "allowedHeaders":
            suggest = "allowed_headers"
        elif key == "allowedMethods":
            suggest = "allowed_methods"
        elif key == "exposedHeaders":
            suggest = "exposed_headers"
        elif key == "maxAgeInSeconds":
            suggest = "max_age_in_seconds"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CorsRuleResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CorsRuleResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CorsRuleResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 allowed_origins: Sequence[str],
                 allowed_headers: Optional[Sequence[str]] = None,
                 allowed_methods: Optional[Sequence[str]] = None,
                 exposed_headers: Optional[Sequence[str]] = None,
                 max_age_in_seconds: Optional[int] = None):
        """
        CORS details.
        :param Sequence[str] allowed_origins: The origin domains that are permitted to make a request against the service via CORS.
        :param Sequence[str] allowed_headers: The request headers that the origin domain may specify on the CORS request.
        :param Sequence[str] allowed_methods: The methods (HTTP request verbs) that the origin domain may use for a CORS request.
        :param Sequence[str] exposed_headers: The response headers to expose to CORS clients.
        :param int max_age_in_seconds: The number of seconds that the client/browser should cache a preflight response.
        """
        pulumi.set(__self__, "allowed_origins", allowed_origins)
        if allowed_headers is not None:
            pulumi.set(__self__, "allowed_headers", allowed_headers)
        if allowed_methods is not None:
            pulumi.set(__self__, "allowed_methods", allowed_methods)
        if exposed_headers is not None:
            pulumi.set(__self__, "exposed_headers", exposed_headers)
        if max_age_in_seconds is not None:
            pulumi.set(__self__, "max_age_in_seconds", max_age_in_seconds)

    @property
    @pulumi.getter(name="allowedOrigins")
    def allowed_origins(self) -> Sequence[str]:
        """
        The origin domains that are permitted to make a request against the service via CORS.
        """
        return pulumi.get(self, "allowed_origins")

    @property
    @pulumi.getter(name="allowedHeaders")
    def allowed_headers(self) -> Optional[Sequence[str]]:
        """
        The request headers that the origin domain may specify on the CORS request.
        """
        return pulumi.get(self, "allowed_headers")

    @property
    @pulumi.getter(name="allowedMethods")
    def allowed_methods(self) -> Optional[Sequence[str]]:
        """
        The methods (HTTP request verbs) that the origin domain may use for a CORS request.
        """
        return pulumi.get(self, "allowed_methods")

    @property
    @pulumi.getter(name="exposedHeaders")
    def exposed_headers(self) -> Optional[Sequence[str]]:
        """
        The response headers to expose to CORS clients.
        """
        return pulumi.get(self, "exposed_headers")

    @property
    @pulumi.getter(name="maxAgeInSeconds")
    def max_age_in_seconds(self) -> Optional[int]:
        """
        The number of seconds that the client/browser should cache a preflight response.
        """
        return pulumi.get(self, "max_age_in_seconds")


@pulumi.output_type
class EndpointAuthenticationResponse(dict):
    """
    Service endpoints authentication details.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "aadTenantID":
            suggest = "aad_tenant_id"
        elif key == "principalID":
            suggest = "principal_id"
        elif key == "principalType":
            suggest = "principal_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointAuthenticationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointAuthenticationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointAuthenticationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 aad_tenant_id: Optional[str] = None,
                 principal_id: Optional[str] = None,
                 principal_type: Optional[str] = None):
        """
        Service endpoints authentication details.
        :param str aad_tenant_id: AAD tenant ID.
        :param str principal_id: AAD principal ID.
        :param str principal_type: AAD principal type.
        """
        if aad_tenant_id is not None:
            pulumi.set(__self__, "aad_tenant_id", aad_tenant_id)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if principal_type is not None:
            pulumi.set(__self__, "principal_type", principal_type)

    @property
    @pulumi.getter(name="aadTenantID")
    def aad_tenant_id(self) -> Optional[str]:
        """
        AAD tenant ID.
        """
        return pulumi.get(self, "aad_tenant_id")

    @property
    @pulumi.getter(name="principalID")
    def principal_id(self) -> Optional[str]:
        """
        AAD principal ID.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="principalType")
    def principal_type(self) -> Optional[str]:
        """
        AAD principal type.
        """
        return pulumi.get(self, "principal_type")


@pulumi.output_type
class ModelingInputDataResponse(dict):
    """
    The configuration to raw CDM data to be used as Modeling resource input.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "connectionString":
            suggest = "connection_string"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ModelingInputDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ModelingInputDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ModelingInputDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 connection_string: Optional[str] = None):
        """
        The configuration to raw CDM data to be used as Modeling resource input.
        :param str connection_string: Connection string to raw input data.
        """
        if connection_string is not None:
            pulumi.set(__self__, "connection_string", connection_string)

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> Optional[str]:
        """
        Connection string to raw input data.
        """
        return pulumi.get(self, "connection_string")


@pulumi.output_type
class ModelingResourceResponseProperties(dict):
    """
    Modeling resource properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "inputData":
            suggest = "input_data"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ModelingResourceResponseProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ModelingResourceResponseProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ModelingResourceResponseProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 provisioning_state: str,
                 features: Optional[str] = None,
                 frequency: Optional[str] = None,
                 input_data: Optional['outputs.ModelingInputDataResponse'] = None,
                 size: Optional[str] = None):
        """
        Modeling resource properties.
        :param str provisioning_state: The resource provisioning state.
        :param str features: Modeling features controls the set of supported scenarios\models being computed. This can only be set at Modeling creation.
        :param str frequency: Modeling frequency controls the modeling compute frequency.
        :param 'ModelingInputDataResponse' input_data: The configuration to raw CDM data to be used as Modeling resource input.
        :param str size: Modeling size controls the maximum supported input data size.
        """
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if features is not None:
            pulumi.set(__self__, "features", features)
        if frequency is not None:
            pulumi.set(__self__, "frequency", frequency)
        if input_data is not None:
            pulumi.set(__self__, "input_data", input_data)
        if size is not None:
            pulumi.set(__self__, "size", size)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The resource provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def features(self) -> Optional[str]:
        """
        Modeling features controls the set of supported scenarios\models being computed. This can only be set at Modeling creation.
        """
        return pulumi.get(self, "features")

    @property
    @pulumi.getter
    def frequency(self) -> Optional[str]:
        """
        Modeling frequency controls the modeling compute frequency.
        """
        return pulumi.get(self, "frequency")

    @property
    @pulumi.getter(name="inputData")
    def input_data(self) -> Optional['outputs.ModelingInputDataResponse']:
        """
        The configuration to raw CDM data to be used as Modeling resource input.
        """
        return pulumi.get(self, "input_data")

    @property
    @pulumi.getter
    def size(self) -> Optional[str]:
        """
        Modeling size controls the maximum supported input data size.
        """
        return pulumi.get(self, "size")


@pulumi.output_type
class ServiceEndpointResourceResponseProperties(dict):
    """
    ServiceEndpoint resource properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "pairedLocation":
            suggest = "paired_location"
        elif key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "preAllocatedCapacity":
            suggest = "pre_allocated_capacity"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServiceEndpointResourceResponseProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServiceEndpointResourceResponseProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ServiceEndpointResourceResponseProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 paired_location: str,
                 provisioning_state: str,
                 url: str,
                 pre_allocated_capacity: Optional[int] = None):
        """
        ServiceEndpoint resource properties.
        :param str paired_location: The paired location that will be used by this ServiceEndpoint.
        :param str provisioning_state: The resource provisioning state.
        :param str url: The URL where the ServiceEndpoint API is accessible at.
        :param int pre_allocated_capacity: ServiceEndpoint pre-allocated capacity controls the maximum requests-per-second allowed for that endpoint. Only applicable when Account configuration is Capacity.
        """
        pulumi.set(__self__, "paired_location", paired_location)
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        pulumi.set(__self__, "url", url)
        if pre_allocated_capacity is not None:
            pulumi.set(__self__, "pre_allocated_capacity", pre_allocated_capacity)

    @property
    @pulumi.getter(name="pairedLocation")
    def paired_location(self) -> str:
        """
        The paired location that will be used by this ServiceEndpoint.
        """
        return pulumi.get(self, "paired_location")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The resource provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def url(self) -> str:
        """
        The URL where the ServiceEndpoint API is accessible at.
        """
        return pulumi.get(self, "url")

    @property
    @pulumi.getter(name="preAllocatedCapacity")
    def pre_allocated_capacity(self) -> Optional[int]:
        """
        ServiceEndpoint pre-allocated capacity controls the maximum requests-per-second allowed for that endpoint. Only applicable when Account configuration is Capacity.
        """
        return pulumi.get(self, "pre_allocated_capacity")


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
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
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The timestamp of resource last modification (UTC)
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
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
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")


