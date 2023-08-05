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
from ._inputs import *

__all__ = ['ConnectorArgs', 'Connector']

@pulumi.input_type
class ConnectorArgs:
    def __init__(__self__, *,
                 authentication_details: Optional[pulumi.Input[Union['AwAssumeRoleAuthenticationDetailsPropertiesArgs', 'AwsCredsAuthenticationDetailsPropertiesArgs', 'GcpCredentialsDetailsPropertiesArgs']]] = None,
                 connector_name: Optional[pulumi.Input[str]] = None,
                 hybrid_compute_settings: Optional[pulumi.Input['HybridComputeSettingsPropertiesArgs']] = None):
        """
        The set of arguments for constructing a Connector resource.
        :param pulumi.Input[Union['AwAssumeRoleAuthenticationDetailsPropertiesArgs', 'AwsCredsAuthenticationDetailsPropertiesArgs', 'GcpCredentialsDetailsPropertiesArgs']] authentication_details: Settings for authentication management, these settings are relevant only for the cloud connector.
        :param pulumi.Input[str] connector_name: Name of the cloud account connector
        :param pulumi.Input['HybridComputeSettingsPropertiesArgs'] hybrid_compute_settings: Settings for hybrid compute management. These settings are relevant only for Arc autoProvision (Hybrid Compute).
        """
        if authentication_details is not None:
            pulumi.set(__self__, "authentication_details", authentication_details)
        if connector_name is not None:
            pulumi.set(__self__, "connector_name", connector_name)
        if hybrid_compute_settings is not None:
            pulumi.set(__self__, "hybrid_compute_settings", hybrid_compute_settings)

    @property
    @pulumi.getter(name="authenticationDetails")
    def authentication_details(self) -> Optional[pulumi.Input[Union['AwAssumeRoleAuthenticationDetailsPropertiesArgs', 'AwsCredsAuthenticationDetailsPropertiesArgs', 'GcpCredentialsDetailsPropertiesArgs']]]:
        """
        Settings for authentication management, these settings are relevant only for the cloud connector.
        """
        return pulumi.get(self, "authentication_details")

    @authentication_details.setter
    def authentication_details(self, value: Optional[pulumi.Input[Union['AwAssumeRoleAuthenticationDetailsPropertiesArgs', 'AwsCredsAuthenticationDetailsPropertiesArgs', 'GcpCredentialsDetailsPropertiesArgs']]]):
        pulumi.set(self, "authentication_details", value)

    @property
    @pulumi.getter(name="connectorName")
    def connector_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the cloud account connector
        """
        return pulumi.get(self, "connector_name")

    @connector_name.setter
    def connector_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connector_name", value)

    @property
    @pulumi.getter(name="hybridComputeSettings")
    def hybrid_compute_settings(self) -> Optional[pulumi.Input['HybridComputeSettingsPropertiesArgs']]:
        """
        Settings for hybrid compute management. These settings are relevant only for Arc autoProvision (Hybrid Compute).
        """
        return pulumi.get(self, "hybrid_compute_settings")

    @hybrid_compute_settings.setter
    def hybrid_compute_settings(self, value: Optional[pulumi.Input['HybridComputeSettingsPropertiesArgs']]):
        pulumi.set(self, "hybrid_compute_settings", value)


class Connector(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication_details: Optional[pulumi.Input[Union[pulumi.InputType['AwAssumeRoleAuthenticationDetailsPropertiesArgs'], pulumi.InputType['AwsCredsAuthenticationDetailsPropertiesArgs'], pulumi.InputType['GcpCredentialsDetailsPropertiesArgs']]]] = None,
                 connector_name: Optional[pulumi.Input[str]] = None,
                 hybrid_compute_settings: Optional[pulumi.Input[pulumi.InputType['HybridComputeSettingsPropertiesArgs']]] = None,
                 __props__=None):
        """
        The connector setting
        API Version: 2020-01-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[pulumi.InputType['AwAssumeRoleAuthenticationDetailsPropertiesArgs'], pulumi.InputType['AwsCredsAuthenticationDetailsPropertiesArgs'], pulumi.InputType['GcpCredentialsDetailsPropertiesArgs']]] authentication_details: Settings for authentication management, these settings are relevant only for the cloud connector.
        :param pulumi.Input[str] connector_name: Name of the cloud account connector
        :param pulumi.Input[pulumi.InputType['HybridComputeSettingsPropertiesArgs']] hybrid_compute_settings: Settings for hybrid compute management. These settings are relevant only for Arc autoProvision (Hybrid Compute).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ConnectorArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The connector setting
        API Version: 2020-01-01-preview.

        :param str resource_name: The name of the resource.
        :param ConnectorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConnectorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication_details: Optional[pulumi.Input[Union[pulumi.InputType['AwAssumeRoleAuthenticationDetailsPropertiesArgs'], pulumi.InputType['AwsCredsAuthenticationDetailsPropertiesArgs'], pulumi.InputType['GcpCredentialsDetailsPropertiesArgs']]]] = None,
                 connector_name: Optional[pulumi.Input[str]] = None,
                 hybrid_compute_settings: Optional[pulumi.Input[pulumi.InputType['HybridComputeSettingsPropertiesArgs']]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConnectorArgs.__new__(ConnectorArgs)

            __props__.__dict__["authentication_details"] = authentication_details
            __props__.__dict__["connector_name"] = connector_name
            __props__.__dict__["hybrid_compute_settings"] = hybrid_compute_settings
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:security/v20200101preview:Connector")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Connector, __self__).__init__(
            'azure-native:security:Connector',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Connector':
        """
        Get an existing Connector resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ConnectorArgs.__new__(ConnectorArgs)

        __props__.__dict__["authentication_details"] = None
        __props__.__dict__["hybrid_compute_settings"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["type"] = None
        return Connector(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="authenticationDetails")
    def authentication_details(self) -> pulumi.Output[Optional[Any]]:
        """
        Settings for authentication management, these settings are relevant only for the cloud connector.
        """
        return pulumi.get(self, "authentication_details")

    @property
    @pulumi.getter(name="hybridComputeSettings")
    def hybrid_compute_settings(self) -> pulumi.Output[Optional['outputs.HybridComputeSettingsPropertiesResponse']]:
        """
        Settings for hybrid compute management. These settings are relevant only for Arc autoProvision (Hybrid Compute).
        """
        return pulumi.get(self, "hybrid_compute_settings")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

