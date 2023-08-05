# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetOuContainerResult',
    'AwaitableGetOuContainerResult',
    'get_ou_container',
    'get_ou_container_output',
]

@pulumi.output_type
class GetOuContainerResult:
    """
    Resource for OuContainer.
    """
    def __init__(__self__, accounts=None, container_id=None, deployment_id=None, distinguished_name=None, domain_name=None, etag=None, id=None, location=None, name=None, provisioning_state=None, service_status=None, system_data=None, tags=None, tenant_id=None, type=None):
        if accounts and not isinstance(accounts, list):
            raise TypeError("Expected argument 'accounts' to be a list")
        pulumi.set(__self__, "accounts", accounts)
        if container_id and not isinstance(container_id, str):
            raise TypeError("Expected argument 'container_id' to be a str")
        pulumi.set(__self__, "container_id", container_id)
        if deployment_id and not isinstance(deployment_id, str):
            raise TypeError("Expected argument 'deployment_id' to be a str")
        pulumi.set(__self__, "deployment_id", deployment_id)
        if distinguished_name and not isinstance(distinguished_name, str):
            raise TypeError("Expected argument 'distinguished_name' to be a str")
        pulumi.set(__self__, "distinguished_name", distinguished_name)
        if domain_name and not isinstance(domain_name, str):
            raise TypeError("Expected argument 'domain_name' to be a str")
        pulumi.set(__self__, "domain_name", domain_name)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if service_status and not isinstance(service_status, str):
            raise TypeError("Expected argument 'service_status' to be a str")
        pulumi.set(__self__, "service_status", service_status)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if tenant_id and not isinstance(tenant_id, str):
            raise TypeError("Expected argument 'tenant_id' to be a str")
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def accounts(self) -> Optional[Sequence['outputs.ContainerAccountResponse']]:
        """
        The list of container accounts
        """
        return pulumi.get(self, "accounts")

    @property
    @pulumi.getter(name="containerId")
    def container_id(self) -> str:
        """
        The OuContainer name
        """
        return pulumi.get(self, "container_id")

    @property
    @pulumi.getter(name="deploymentId")
    def deployment_id(self) -> str:
        """
        The Deployment id
        """
        return pulumi.get(self, "deployment_id")

    @property
    @pulumi.getter(name="distinguishedName")
    def distinguished_name(self) -> str:
        """
        Distinguished Name of OuContainer instance
        """
        return pulumi.get(self, "distinguished_name")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> str:
        """
        The domain name of Domain Services.
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Resource etag
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The current deployment or provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="serviceStatus")
    def service_status(self) -> str:
        """
        Status of OuContainer instance
        """
        return pulumi.get(self, "service_status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        Azure Active Directory tenant id
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetOuContainerResult(GetOuContainerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOuContainerResult(
            accounts=self.accounts,
            container_id=self.container_id,
            deployment_id=self.deployment_id,
            distinguished_name=self.distinguished_name,
            domain_name=self.domain_name,
            etag=self.etag,
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            service_status=self.service_status,
            system_data=self.system_data,
            tags=self.tags,
            tenant_id=self.tenant_id,
            type=self.type)


def get_ou_container(domain_service_name: Optional[str] = None,
                     ou_container_name: Optional[str] = None,
                     resource_group_name: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOuContainerResult:
    """
    Resource for OuContainer.
    API Version: 2021-03-01.


    :param str domain_service_name: The name of the domain service.
    :param str ou_container_name: The name of the OuContainer.
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    __args__ = dict()
    __args__['domainServiceName'] = domain_service_name
    __args__['ouContainerName'] = ou_container_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:aad:getOuContainer', __args__, opts=opts, typ=GetOuContainerResult).value

    return AwaitableGetOuContainerResult(
        accounts=__ret__.accounts,
        container_id=__ret__.container_id,
        deployment_id=__ret__.deployment_id,
        distinguished_name=__ret__.distinguished_name,
        domain_name=__ret__.domain_name,
        etag=__ret__.etag,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        service_status=__ret__.service_status,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        tenant_id=__ret__.tenant_id,
        type=__ret__.type)


@_utilities.lift_output_func(get_ou_container)
def get_ou_container_output(domain_service_name: Optional[pulumi.Input[str]] = None,
                            ou_container_name: Optional[pulumi.Input[str]] = None,
                            resource_group_name: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOuContainerResult]:
    """
    Resource for OuContainer.
    API Version: 2021-03-01.


    :param str domain_service_name: The name of the domain service.
    :param str ou_container_name: The name of the OuContainer.
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    ...
