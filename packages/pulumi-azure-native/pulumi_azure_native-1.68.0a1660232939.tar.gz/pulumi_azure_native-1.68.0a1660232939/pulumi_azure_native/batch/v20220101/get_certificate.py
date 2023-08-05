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
    'GetCertificateResult',
    'AwaitableGetCertificateResult',
    'get_certificate',
    'get_certificate_output',
]

@pulumi.output_type
class GetCertificateResult:
    """
    Contains information about a certificate.
    """
    def __init__(__self__, delete_certificate_error=None, etag=None, format=None, id=None, name=None, previous_provisioning_state=None, previous_provisioning_state_transition_time=None, provisioning_state=None, provisioning_state_transition_time=None, public_data=None, thumbprint=None, thumbprint_algorithm=None, type=None):
        if delete_certificate_error and not isinstance(delete_certificate_error, dict):
            raise TypeError("Expected argument 'delete_certificate_error' to be a dict")
        pulumi.set(__self__, "delete_certificate_error", delete_certificate_error)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if format and not isinstance(format, str):
            raise TypeError("Expected argument 'format' to be a str")
        pulumi.set(__self__, "format", format)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if previous_provisioning_state and not isinstance(previous_provisioning_state, str):
            raise TypeError("Expected argument 'previous_provisioning_state' to be a str")
        pulumi.set(__self__, "previous_provisioning_state", previous_provisioning_state)
        if previous_provisioning_state_transition_time and not isinstance(previous_provisioning_state_transition_time, str):
            raise TypeError("Expected argument 'previous_provisioning_state_transition_time' to be a str")
        pulumi.set(__self__, "previous_provisioning_state_transition_time", previous_provisioning_state_transition_time)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if provisioning_state_transition_time and not isinstance(provisioning_state_transition_time, str):
            raise TypeError("Expected argument 'provisioning_state_transition_time' to be a str")
        pulumi.set(__self__, "provisioning_state_transition_time", provisioning_state_transition_time)
        if public_data and not isinstance(public_data, str):
            raise TypeError("Expected argument 'public_data' to be a str")
        pulumi.set(__self__, "public_data", public_data)
        if thumbprint and not isinstance(thumbprint, str):
            raise TypeError("Expected argument 'thumbprint' to be a str")
        pulumi.set(__self__, "thumbprint", thumbprint)
        if thumbprint_algorithm and not isinstance(thumbprint_algorithm, str):
            raise TypeError("Expected argument 'thumbprint_algorithm' to be a str")
        pulumi.set(__self__, "thumbprint_algorithm", thumbprint_algorithm)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="deleteCertificateError")
    def delete_certificate_error(self) -> 'outputs.DeleteCertificateErrorResponse':
        """
        This is only returned when the certificate provisioningState is 'Failed'.
        """
        return pulumi.get(self, "delete_certificate_error")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        The ETag of the resource, used for concurrency statements.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def format(self) -> Optional[str]:
        """
        The format of the certificate - either Pfx or Cer. If omitted, the default is Pfx.
        """
        return pulumi.get(self, "format")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="previousProvisioningState")
    def previous_provisioning_state(self) -> str:
        """
        The previous provisioned state of the resource
        """
        return pulumi.get(self, "previous_provisioning_state")

    @property
    @pulumi.getter(name="previousProvisioningStateTransitionTime")
    def previous_provisioning_state_transition_time(self) -> str:
        return pulumi.get(self, "previous_provisioning_state_transition_time")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="provisioningStateTransitionTime")
    def provisioning_state_transition_time(self) -> str:
        return pulumi.get(self, "provisioning_state_transition_time")

    @property
    @pulumi.getter(name="publicData")
    def public_data(self) -> str:
        """
        The public key of the certificate.
        """
        return pulumi.get(self, "public_data")

    @property
    @pulumi.getter
    def thumbprint(self) -> Optional[str]:
        """
        This must match the thumbprint from the name.
        """
        return pulumi.get(self, "thumbprint")

    @property
    @pulumi.getter(name="thumbprintAlgorithm")
    def thumbprint_algorithm(self) -> Optional[str]:
        """
        This must match the first portion of the certificate name. Currently required to be 'SHA1'.
        """
        return pulumi.get(self, "thumbprint_algorithm")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetCertificateResult(GetCertificateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCertificateResult(
            delete_certificate_error=self.delete_certificate_error,
            etag=self.etag,
            format=self.format,
            id=self.id,
            name=self.name,
            previous_provisioning_state=self.previous_provisioning_state,
            previous_provisioning_state_transition_time=self.previous_provisioning_state_transition_time,
            provisioning_state=self.provisioning_state,
            provisioning_state_transition_time=self.provisioning_state_transition_time,
            public_data=self.public_data,
            thumbprint=self.thumbprint,
            thumbprint_algorithm=self.thumbprint_algorithm,
            type=self.type)


def get_certificate(account_name: Optional[str] = None,
                    certificate_name: Optional[str] = None,
                    resource_group_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCertificateResult:
    """
    Contains information about a certificate.


    :param str account_name: The name of the Batch account.
    :param str certificate_name: The identifier for the certificate. This must be made up of algorithm and thumbprint separated by a dash, and must match the certificate data in the request. For example SHA1-a3d1c5.
    :param str resource_group_name: The name of the resource group that contains the Batch account.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['certificateName'] = certificate_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:batch/v20220101:getCertificate', __args__, opts=opts, typ=GetCertificateResult).value

    return AwaitableGetCertificateResult(
        delete_certificate_error=__ret__.delete_certificate_error,
        etag=__ret__.etag,
        format=__ret__.format,
        id=__ret__.id,
        name=__ret__.name,
        previous_provisioning_state=__ret__.previous_provisioning_state,
        previous_provisioning_state_transition_time=__ret__.previous_provisioning_state_transition_time,
        provisioning_state=__ret__.provisioning_state,
        provisioning_state_transition_time=__ret__.provisioning_state_transition_time,
        public_data=__ret__.public_data,
        thumbprint=__ret__.thumbprint,
        thumbprint_algorithm=__ret__.thumbprint_algorithm,
        type=__ret__.type)


@_utilities.lift_output_func(get_certificate)
def get_certificate_output(account_name: Optional[pulumi.Input[str]] = None,
                           certificate_name: Optional[pulumi.Input[str]] = None,
                           resource_group_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCertificateResult]:
    """
    Contains information about a certificate.


    :param str account_name: The name of the Batch account.
    :param str certificate_name: The identifier for the certificate. This must be made up of algorithm and thumbprint separated by a dash, and must match the certificate data in the request. For example SHA1-a3d1c5.
    :param str resource_group_name: The name of the resource group that contains the Batch account.
    """
    ...
