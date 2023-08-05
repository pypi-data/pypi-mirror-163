# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = ['SecurityRuleInitArgs', 'SecurityRule']

@pulumi.input_type
class SecurityRuleInitArgs:
    def __init__(__self__, *,
                 access: pulumi.Input[Union[str, 'SecurityRuleAccess']],
                 destination_address_prefix: pulumi.Input[str],
                 direction: pulumi.Input[Union[str, 'SecurityRuleDirection']],
                 network_security_group_name: pulumi.Input[str],
                 protocol: pulumi.Input[Union[str, 'SecurityRuleProtocol']],
                 resource_group_name: pulumi.Input[str],
                 source_address_prefix: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 destination_port_range: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 security_rule_name: Optional[pulumi.Input[str]] = None,
                 source_port_range: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SecurityRule resource.
        :param pulumi.Input[Union[str, 'SecurityRuleAccess']] access: Gets or sets network traffic is allowed or denied. Possible values are 'Allow' and 'Deny'
        :param pulumi.Input[str] destination_address_prefix: Gets or sets destination address prefix. CIDR or source IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used. 
        :param pulumi.Input[Union[str, 'SecurityRuleDirection']] direction: Gets or sets the direction of the rule.InBound or Outbound. The direction specifies if rule will be evaluated on incoming or outgoing traffic.
        :param pulumi.Input[str] network_security_group_name: The name of the network security group.
        :param pulumi.Input[Union[str, 'SecurityRuleProtocol']] protocol: Gets or sets Network protocol this rule applies to. Can be Tcp, Udp or All(*).
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] source_address_prefix: Gets or sets source address prefix. CIDR or source IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used. If this is an ingress rule, specifies where network traffic originates from. 
        :param pulumi.Input[str] description: Gets or sets a description for this rule. Restricted to 140 chars.
        :param pulumi.Input[str] destination_port_range: Gets or sets Destination Port or Range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
        :param pulumi.Input[str] id: Resource Id
        :param pulumi.Input[str] name: Gets name of the resource that is unique within a resource group. This name can be used to access the resource
        :param pulumi.Input[int] priority: Gets or sets the priority of the rule. The value can be between 100 and 4096. The priority number must be unique for each rule in the collection. The lower the priority number, the higher the priority of the rule.
        :param pulumi.Input[str] provisioning_state: Gets or sets Provisioning state of the PublicIP resource Updating/Deleting/Failed
        :param pulumi.Input[str] security_rule_name: The name of the security rule.
        :param pulumi.Input[str] source_port_range: Gets or sets Source Port or Range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
        """
        pulumi.set(__self__, "access", access)
        pulumi.set(__self__, "destination_address_prefix", destination_address_prefix)
        pulumi.set(__self__, "direction", direction)
        pulumi.set(__self__, "network_security_group_name", network_security_group_name)
        pulumi.set(__self__, "protocol", protocol)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "source_address_prefix", source_address_prefix)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if destination_port_range is not None:
            pulumi.set(__self__, "destination_port_range", destination_port_range)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)
        if security_rule_name is not None:
            pulumi.set(__self__, "security_rule_name", security_rule_name)
        if source_port_range is not None:
            pulumi.set(__self__, "source_port_range", source_port_range)

    @property
    @pulumi.getter
    def access(self) -> pulumi.Input[Union[str, 'SecurityRuleAccess']]:
        """
        Gets or sets network traffic is allowed or denied. Possible values are 'Allow' and 'Deny'
        """
        return pulumi.get(self, "access")

    @access.setter
    def access(self, value: pulumi.Input[Union[str, 'SecurityRuleAccess']]):
        pulumi.set(self, "access", value)

    @property
    @pulumi.getter(name="destinationAddressPrefix")
    def destination_address_prefix(self) -> pulumi.Input[str]:
        """
        Gets or sets destination address prefix. CIDR or source IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used. 
        """
        return pulumi.get(self, "destination_address_prefix")

    @destination_address_prefix.setter
    def destination_address_prefix(self, value: pulumi.Input[str]):
        pulumi.set(self, "destination_address_prefix", value)

    @property
    @pulumi.getter
    def direction(self) -> pulumi.Input[Union[str, 'SecurityRuleDirection']]:
        """
        Gets or sets the direction of the rule.InBound or Outbound. The direction specifies if rule will be evaluated on incoming or outgoing traffic.
        """
        return pulumi.get(self, "direction")

    @direction.setter
    def direction(self, value: pulumi.Input[Union[str, 'SecurityRuleDirection']]):
        pulumi.set(self, "direction", value)

    @property
    @pulumi.getter(name="networkSecurityGroupName")
    def network_security_group_name(self) -> pulumi.Input[str]:
        """
        The name of the network security group.
        """
        return pulumi.get(self, "network_security_group_name")

    @network_security_group_name.setter
    def network_security_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "network_security_group_name", value)

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Input[Union[str, 'SecurityRuleProtocol']]:
        """
        Gets or sets Network protocol this rule applies to. Can be Tcp, Udp or All(*).
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: pulumi.Input[Union[str, 'SecurityRuleProtocol']]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="sourceAddressPrefix")
    def source_address_prefix(self) -> pulumi.Input[str]:
        """
        Gets or sets source address prefix. CIDR or source IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used. If this is an ingress rule, specifies where network traffic originates from. 
        """
        return pulumi.get(self, "source_address_prefix")

    @source_address_prefix.setter
    def source_address_prefix(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_address_prefix", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets a description for this rule. Restricted to 140 chars.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="destinationPortRange")
    def destination_port_range(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets Destination Port or Range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
        """
        return pulumi.get(self, "destination_port_range")

    @destination_port_range.setter
    def destination_port_range(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "destination_port_range", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Gets name of the resource that is unique within a resource group. This name can be used to access the resource
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[int]]:
        """
        Gets or sets the priority of the rule. The value can be between 100 and 4096. The priority number must be unique for each rule in the collection. The lower the priority number, the higher the priority of the rule.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets Provisioning state of the PublicIP resource Updating/Deleting/Failed
        """
        return pulumi.get(self, "provisioning_state")

    @provisioning_state.setter
    def provisioning_state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "provisioning_state", value)

    @property
    @pulumi.getter(name="securityRuleName")
    def security_rule_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the security rule.
        """
        return pulumi.get(self, "security_rule_name")

    @security_rule_name.setter
    def security_rule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "security_rule_name", value)

    @property
    @pulumi.getter(name="sourcePortRange")
    def source_port_range(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets Source Port or Range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
        """
        return pulumi.get(self, "source_port_range")

    @source_port_range.setter
    def source_port_range(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_port_range", value)


warnings.warn("""Version 2016-03-30 will be removed in v2 of the provider.""", DeprecationWarning)


class SecurityRule(pulumi.CustomResource):
    warnings.warn("""Version 2016-03-30 will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access: Optional[pulumi.Input[Union[str, 'SecurityRuleAccess']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 destination_address_prefix: Optional[pulumi.Input[str]] = None,
                 destination_port_range: Optional[pulumi.Input[str]] = None,
                 direction: Optional[pulumi.Input[Union[str, 'SecurityRuleDirection']]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_security_group_name: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 protocol: Optional[pulumi.Input[Union[str, 'SecurityRuleProtocol']]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 security_rule_name: Optional[pulumi.Input[str]] = None,
                 source_address_prefix: Optional[pulumi.Input[str]] = None,
                 source_port_range: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Network security rule

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'SecurityRuleAccess']] access: Gets or sets network traffic is allowed or denied. Possible values are 'Allow' and 'Deny'
        :param pulumi.Input[str] description: Gets or sets a description for this rule. Restricted to 140 chars.
        :param pulumi.Input[str] destination_address_prefix: Gets or sets destination address prefix. CIDR or source IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used. 
        :param pulumi.Input[str] destination_port_range: Gets or sets Destination Port or Range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
        :param pulumi.Input[Union[str, 'SecurityRuleDirection']] direction: Gets or sets the direction of the rule.InBound or Outbound. The direction specifies if rule will be evaluated on incoming or outgoing traffic.
        :param pulumi.Input[str] id: Resource Id
        :param pulumi.Input[str] name: Gets name of the resource that is unique within a resource group. This name can be used to access the resource
        :param pulumi.Input[str] network_security_group_name: The name of the network security group.
        :param pulumi.Input[int] priority: Gets or sets the priority of the rule. The value can be between 100 and 4096. The priority number must be unique for each rule in the collection. The lower the priority number, the higher the priority of the rule.
        :param pulumi.Input[Union[str, 'SecurityRuleProtocol']] protocol: Gets or sets Network protocol this rule applies to. Can be Tcp, Udp or All(*).
        :param pulumi.Input[str] provisioning_state: Gets or sets Provisioning state of the PublicIP resource Updating/Deleting/Failed
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] security_rule_name: The name of the security rule.
        :param pulumi.Input[str] source_address_prefix: Gets or sets source address prefix. CIDR or source IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used. If this is an ingress rule, specifies where network traffic originates from. 
        :param pulumi.Input[str] source_port_range: Gets or sets Source Port or Range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SecurityRuleInitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Network security rule

        :param str resource_name: The name of the resource.
        :param SecurityRuleInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SecurityRuleInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access: Optional[pulumi.Input[Union[str, 'SecurityRuleAccess']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 destination_address_prefix: Optional[pulumi.Input[str]] = None,
                 destination_port_range: Optional[pulumi.Input[str]] = None,
                 direction: Optional[pulumi.Input[Union[str, 'SecurityRuleDirection']]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_security_group_name: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 protocol: Optional[pulumi.Input[Union[str, 'SecurityRuleProtocol']]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 security_rule_name: Optional[pulumi.Input[str]] = None,
                 source_address_prefix: Optional[pulumi.Input[str]] = None,
                 source_port_range: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""SecurityRule is deprecated: Version 2016-03-30 will be removed in v2 of the provider.""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SecurityRuleInitArgs.__new__(SecurityRuleInitArgs)

            if access is None and not opts.urn:
                raise TypeError("Missing required property 'access'")
            __props__.__dict__["access"] = access
            __props__.__dict__["description"] = description
            if destination_address_prefix is None and not opts.urn:
                raise TypeError("Missing required property 'destination_address_prefix'")
            __props__.__dict__["destination_address_prefix"] = destination_address_prefix
            __props__.__dict__["destination_port_range"] = destination_port_range
            if direction is None and not opts.urn:
                raise TypeError("Missing required property 'direction'")
            __props__.__dict__["direction"] = direction
            __props__.__dict__["id"] = id
            __props__.__dict__["name"] = name
            if network_security_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'network_security_group_name'")
            __props__.__dict__["network_security_group_name"] = network_security_group_name
            __props__.__dict__["priority"] = priority
            if protocol is None and not opts.urn:
                raise TypeError("Missing required property 'protocol'")
            __props__.__dict__["protocol"] = protocol
            __props__.__dict__["provisioning_state"] = provisioning_state
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["security_rule_name"] = security_rule_name
            if source_address_prefix is None and not opts.urn:
                raise TypeError("Missing required property 'source_address_prefix'")
            __props__.__dict__["source_address_prefix"] = source_address_prefix
            __props__.__dict__["source_port_range"] = source_port_range
            __props__.__dict__["etag"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20150501preview:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20150615:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20160601:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20160901:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20161201:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20170301:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20170601:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20170801:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20170901:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20171001:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20171101:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20180101:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20180201:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20180401:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20180601:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20180701:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20180801:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20181001:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20181101:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20181201:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20190201:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20190401:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20190601:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20190701:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20190801:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20190901:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20191101:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20191201:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20200301:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20200401:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20200501:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20200601:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20200701:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20200801:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20201101:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20210201:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20210301:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20210501:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20210801:SecurityRule"), pulumi.Alias(type_="azure-native:network/v20220101:SecurityRule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SecurityRule, __self__).__init__(
            'azure-native:network/v20160330:SecurityRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SecurityRule':
        """
        Get an existing SecurityRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SecurityRuleInitArgs.__new__(SecurityRuleInitArgs)

        __props__.__dict__["access"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["destination_address_prefix"] = None
        __props__.__dict__["destination_port_range"] = None
        __props__.__dict__["direction"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["priority"] = None
        __props__.__dict__["protocol"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["source_address_prefix"] = None
        __props__.__dict__["source_port_range"] = None
        return SecurityRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def access(self) -> pulumi.Output[str]:
        """
        Gets or sets network traffic is allowed or denied. Possible values are 'Allow' and 'Deny'
        """
        return pulumi.get(self, "access")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets a description for this rule. Restricted to 140 chars.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="destinationAddressPrefix")
    def destination_address_prefix(self) -> pulumi.Output[str]:
        """
        Gets or sets destination address prefix. CIDR or source IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used. 
        """
        return pulumi.get(self, "destination_address_prefix")

    @property
    @pulumi.getter(name="destinationPortRange")
    def destination_port_range(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets Destination Port or Range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
        """
        return pulumi.get(self, "destination_port_range")

    @property
    @pulumi.getter
    def direction(self) -> pulumi.Output[str]:
        """
        Gets or sets the direction of the rule.InBound or Outbound. The direction specifies if rule will be evaluated on incoming or outgoing traffic.
        """
        return pulumi.get(self, "direction")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        A unique read-only string that changes whenever the resource is updated
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        Gets name of the resource that is unique within a resource group. This name can be used to access the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Output[Optional[int]]:
        """
        Gets or sets the priority of the rule. The value can be between 100 and 4096. The priority number must be unique for each rule in the collection. The lower the priority number, the higher the priority of the rule.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[str]:
        """
        Gets or sets Network protocol this rule applies to. Can be Tcp, Udp or All(*).
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets Provisioning state of the PublicIP resource Updating/Deleting/Failed
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="sourceAddressPrefix")
    def source_address_prefix(self) -> pulumi.Output[str]:
        """
        Gets or sets source address prefix. CIDR or source IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used. If this is an ingress rule, specifies where network traffic originates from. 
        """
        return pulumi.get(self, "source_address_prefix")

    @property
    @pulumi.getter(name="sourcePortRange")
    def source_port_range(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets Source Port or Range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
        """
        return pulumi.get(self, "source_port_range")

