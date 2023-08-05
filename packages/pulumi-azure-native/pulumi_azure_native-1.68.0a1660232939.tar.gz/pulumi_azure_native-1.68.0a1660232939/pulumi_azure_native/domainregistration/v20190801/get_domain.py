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
    'GetDomainResult',
    'AwaitableGetDomainResult',
    'get_domain',
    'get_domain_output',
]

warnings.warn("""Version 2019-08-01 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetDomainResult:
    """
    Information about a domain.
    """
    def __init__(__self__, auth_code=None, auto_renew=None, created_time=None, dns_type=None, dns_zone_id=None, domain_not_renewable_reasons=None, expiration_time=None, id=None, kind=None, last_renewed_time=None, location=None, managed_host_names=None, name=None, name_servers=None, privacy=None, provisioning_state=None, ready_for_dns_record_management=None, registration_status=None, tags=None, target_dns_type=None, type=None):
        if auth_code and not isinstance(auth_code, str):
            raise TypeError("Expected argument 'auth_code' to be a str")
        pulumi.set(__self__, "auth_code", auth_code)
        if auto_renew and not isinstance(auto_renew, bool):
            raise TypeError("Expected argument 'auto_renew' to be a bool")
        pulumi.set(__self__, "auto_renew", auto_renew)
        if created_time and not isinstance(created_time, str):
            raise TypeError("Expected argument 'created_time' to be a str")
        pulumi.set(__self__, "created_time", created_time)
        if dns_type and not isinstance(dns_type, str):
            raise TypeError("Expected argument 'dns_type' to be a str")
        pulumi.set(__self__, "dns_type", dns_type)
        if dns_zone_id and not isinstance(dns_zone_id, str):
            raise TypeError("Expected argument 'dns_zone_id' to be a str")
        pulumi.set(__self__, "dns_zone_id", dns_zone_id)
        if domain_not_renewable_reasons and not isinstance(domain_not_renewable_reasons, list):
            raise TypeError("Expected argument 'domain_not_renewable_reasons' to be a list")
        pulumi.set(__self__, "domain_not_renewable_reasons", domain_not_renewable_reasons)
        if expiration_time and not isinstance(expiration_time, str):
            raise TypeError("Expected argument 'expiration_time' to be a str")
        pulumi.set(__self__, "expiration_time", expiration_time)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if last_renewed_time and not isinstance(last_renewed_time, str):
            raise TypeError("Expected argument 'last_renewed_time' to be a str")
        pulumi.set(__self__, "last_renewed_time", last_renewed_time)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if managed_host_names and not isinstance(managed_host_names, list):
            raise TypeError("Expected argument 'managed_host_names' to be a list")
        pulumi.set(__self__, "managed_host_names", managed_host_names)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if name_servers and not isinstance(name_servers, list):
            raise TypeError("Expected argument 'name_servers' to be a list")
        pulumi.set(__self__, "name_servers", name_servers)
        if privacy and not isinstance(privacy, bool):
            raise TypeError("Expected argument 'privacy' to be a bool")
        pulumi.set(__self__, "privacy", privacy)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if ready_for_dns_record_management and not isinstance(ready_for_dns_record_management, bool):
            raise TypeError("Expected argument 'ready_for_dns_record_management' to be a bool")
        pulumi.set(__self__, "ready_for_dns_record_management", ready_for_dns_record_management)
        if registration_status and not isinstance(registration_status, str):
            raise TypeError("Expected argument 'registration_status' to be a str")
        pulumi.set(__self__, "registration_status", registration_status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if target_dns_type and not isinstance(target_dns_type, str):
            raise TypeError("Expected argument 'target_dns_type' to be a str")
        pulumi.set(__self__, "target_dns_type", target_dns_type)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="authCode")
    def auth_code(self) -> Optional[str]:
        return pulumi.get(self, "auth_code")

    @property
    @pulumi.getter(name="autoRenew")
    def auto_renew(self) -> Optional[bool]:
        """
        <code>true</code> if the domain should be automatically renewed; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "auto_renew")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> str:
        """
        Domain creation timestamp.
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter(name="dnsType")
    def dns_type(self) -> Optional[str]:
        """
        Current DNS type
        """
        return pulumi.get(self, "dns_type")

    @property
    @pulumi.getter(name="dnsZoneId")
    def dns_zone_id(self) -> Optional[str]:
        """
        Azure DNS Zone to use
        """
        return pulumi.get(self, "dns_zone_id")

    @property
    @pulumi.getter(name="domainNotRenewableReasons")
    def domain_not_renewable_reasons(self) -> Sequence[str]:
        """
        Reasons why domain is not renewable.
        """
        return pulumi.get(self, "domain_not_renewable_reasons")

    @property
    @pulumi.getter(name="expirationTime")
    def expiration_time(self) -> str:
        """
        Domain expiration timestamp.
        """
        return pulumi.get(self, "expiration_time")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastRenewedTime")
    def last_renewed_time(self) -> str:
        """
        Timestamp when the domain was renewed last time.
        """
        return pulumi.get(self, "last_renewed_time")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedHostNames")
    def managed_host_names(self) -> Sequence['outputs.HostNameResponse']:
        """
        All hostnames derived from the domain and assigned to Azure resources.
        """
        return pulumi.get(self, "managed_host_names")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nameServers")
    def name_servers(self) -> Sequence[str]:
        """
        Name servers.
        """
        return pulumi.get(self, "name_servers")

    @property
    @pulumi.getter
    def privacy(self) -> Optional[bool]:
        """
        <code>true</code> if domain privacy is enabled for this domain; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "privacy")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Domain provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="readyForDnsRecordManagement")
    def ready_for_dns_record_management(self) -> bool:
        """
        <code>true</code> if Azure can assign this domain to App Service apps; otherwise, <code>false</code>. This value will be <code>true</code> if domain registration status is active and 
         it is hosted on name servers Azure has programmatic access to.
        """
        return pulumi.get(self, "ready_for_dns_record_management")

    @property
    @pulumi.getter(name="registrationStatus")
    def registration_status(self) -> str:
        """
        Domain registration status.
        """
        return pulumi.get(self, "registration_status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetDnsType")
    def target_dns_type(self) -> Optional[str]:
        """
        Target DNS type (would be used for migration)
        """
        return pulumi.get(self, "target_dns_type")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetDomainResult(GetDomainResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDomainResult(
            auth_code=self.auth_code,
            auto_renew=self.auto_renew,
            created_time=self.created_time,
            dns_type=self.dns_type,
            dns_zone_id=self.dns_zone_id,
            domain_not_renewable_reasons=self.domain_not_renewable_reasons,
            expiration_time=self.expiration_time,
            id=self.id,
            kind=self.kind,
            last_renewed_time=self.last_renewed_time,
            location=self.location,
            managed_host_names=self.managed_host_names,
            name=self.name,
            name_servers=self.name_servers,
            privacy=self.privacy,
            provisioning_state=self.provisioning_state,
            ready_for_dns_record_management=self.ready_for_dns_record_management,
            registration_status=self.registration_status,
            tags=self.tags,
            target_dns_type=self.target_dns_type,
            type=self.type)


def get_domain(domain_name: Optional[str] = None,
               resource_group_name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDomainResult:
    """
    Information about a domain.


    :param str domain_name: Name of the domain.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    pulumi.log.warn("""get_domain is deprecated: Version 2019-08-01 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['domainName'] = domain_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:domainregistration/v20190801:getDomain', __args__, opts=opts, typ=GetDomainResult).value

    return AwaitableGetDomainResult(
        auth_code=__ret__.auth_code,
        auto_renew=__ret__.auto_renew,
        created_time=__ret__.created_time,
        dns_type=__ret__.dns_type,
        dns_zone_id=__ret__.dns_zone_id,
        domain_not_renewable_reasons=__ret__.domain_not_renewable_reasons,
        expiration_time=__ret__.expiration_time,
        id=__ret__.id,
        kind=__ret__.kind,
        last_renewed_time=__ret__.last_renewed_time,
        location=__ret__.location,
        managed_host_names=__ret__.managed_host_names,
        name=__ret__.name,
        name_servers=__ret__.name_servers,
        privacy=__ret__.privacy,
        provisioning_state=__ret__.provisioning_state,
        ready_for_dns_record_management=__ret__.ready_for_dns_record_management,
        registration_status=__ret__.registration_status,
        tags=__ret__.tags,
        target_dns_type=__ret__.target_dns_type,
        type=__ret__.type)


@_utilities.lift_output_func(get_domain)
def get_domain_output(domain_name: Optional[pulumi.Input[str]] = None,
                      resource_group_name: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDomainResult]:
    """
    Information about a domain.


    :param str domain_name: Name of the domain.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    pulumi.log.warn("""get_domain is deprecated: Version 2019-08-01 will be removed in v2 of the provider.""")
    ...
