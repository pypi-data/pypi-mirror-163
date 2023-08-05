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

__all__ = ['WebTestArgs', 'WebTest']

@pulumi.input_type
class WebTestArgs:
    def __init__(__self__, *,
                 locations: pulumi.Input[Sequence[pulumi.Input['WebTestGeolocationArgs']]],
                 resource_group_name: pulumi.Input[str],
                 synthetic_monitor_id: pulumi.Input[str],
                 web_test_kind: pulumi.Input['WebTestKind'],
                 configuration: Optional[pulumi.Input['WebTestPropertiesConfigurationArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 frequency: Optional[pulumi.Input[int]] = None,
                 kind: Optional[pulumi.Input['WebTestKind']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 retry_enabled: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeout: Optional[pulumi.Input[int]] = None,
                 web_test_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a WebTest resource.
        :param pulumi.Input[Sequence[pulumi.Input['WebTestGeolocationArgs']]] locations: A list of where to physically run the tests from to give global coverage for accessibility of your application.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] synthetic_monitor_id: Unique ID of this WebTest. This is typically the same value as the Name field.
        :param pulumi.Input['WebTestKind'] web_test_kind: The kind of web test this is, valid choices are ping and multistep.
        :param pulumi.Input['WebTestPropertiesConfigurationArgs'] configuration: An XML configuration specification for a WebTest.
        :param pulumi.Input[str] description: Purpose/user defined descriptive test for this WebTest.
        :param pulumi.Input[bool] enabled: Is the test actively being monitored.
        :param pulumi.Input[int] frequency: Interval in seconds between test runs for this WebTest. Default value is 300.
        :param pulumi.Input['WebTestKind'] kind: The kind of web test that this web test watches. Choices are ping and multistep.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[bool] retry_enabled: Allow for retries should this WebTest fail.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[int] timeout: Seconds until this WebTest will timeout and fail. Default value is 30.
        :param pulumi.Input[str] web_test_name: User defined name if this WebTest.
        """
        pulumi.set(__self__, "locations", locations)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "synthetic_monitor_id", synthetic_monitor_id)
        if web_test_kind is None:
            web_test_kind = 'ping'
        pulumi.set(__self__, "web_test_kind", web_test_kind)
        if configuration is not None:
            pulumi.set(__self__, "configuration", configuration)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if frequency is None:
            frequency = 300
        if frequency is not None:
            pulumi.set(__self__, "frequency", frequency)
        if kind is None:
            kind = 'ping'
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if retry_enabled is not None:
            pulumi.set(__self__, "retry_enabled", retry_enabled)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if timeout is None:
            timeout = 30
        if timeout is not None:
            pulumi.set(__self__, "timeout", timeout)
        if web_test_name is not None:
            pulumi.set(__self__, "web_test_name", web_test_name)

    @property
    @pulumi.getter
    def locations(self) -> pulumi.Input[Sequence[pulumi.Input['WebTestGeolocationArgs']]]:
        """
        A list of where to physically run the tests from to give global coverage for accessibility of your application.
        """
        return pulumi.get(self, "locations")

    @locations.setter
    def locations(self, value: pulumi.Input[Sequence[pulumi.Input['WebTestGeolocationArgs']]]):
        pulumi.set(self, "locations", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="syntheticMonitorId")
    def synthetic_monitor_id(self) -> pulumi.Input[str]:
        """
        Unique ID of this WebTest. This is typically the same value as the Name field.
        """
        return pulumi.get(self, "synthetic_monitor_id")

    @synthetic_monitor_id.setter
    def synthetic_monitor_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "synthetic_monitor_id", value)

    @property
    @pulumi.getter(name="webTestKind")
    def web_test_kind(self) -> pulumi.Input['WebTestKind']:
        """
        The kind of web test this is, valid choices are ping and multistep.
        """
        return pulumi.get(self, "web_test_kind")

    @web_test_kind.setter
    def web_test_kind(self, value: pulumi.Input['WebTestKind']):
        pulumi.set(self, "web_test_kind", value)

    @property
    @pulumi.getter
    def configuration(self) -> Optional[pulumi.Input['WebTestPropertiesConfigurationArgs']]:
        """
        An XML configuration specification for a WebTest.
        """
        return pulumi.get(self, "configuration")

    @configuration.setter
    def configuration(self, value: Optional[pulumi.Input['WebTestPropertiesConfigurationArgs']]):
        pulumi.set(self, "configuration", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Purpose/user defined descriptive test for this WebTest.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the test actively being monitored.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def frequency(self) -> Optional[pulumi.Input[int]]:
        """
        Interval in seconds between test runs for this WebTest. Default value is 300.
        """
        return pulumi.get(self, "frequency")

    @frequency.setter
    def frequency(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "frequency", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input['WebTestKind']]:
        """
        The kind of web test that this web test watches. Choices are ping and multistep.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input['WebTestKind']]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="retryEnabled")
    def retry_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Allow for retries should this WebTest fail.
        """
        return pulumi.get(self, "retry_enabled")

    @retry_enabled.setter
    def retry_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "retry_enabled", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def timeout(self) -> Optional[pulumi.Input[int]]:
        """
        Seconds until this WebTest will timeout and fail. Default value is 30.
        """
        return pulumi.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout", value)

    @property
    @pulumi.getter(name="webTestName")
    def web_test_name(self) -> Optional[pulumi.Input[str]]:
        """
        User defined name if this WebTest.
        """
        return pulumi.get(self, "web_test_name")

    @web_test_name.setter
    def web_test_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "web_test_name", value)


class WebTest(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration: Optional[pulumi.Input[pulumi.InputType['WebTestPropertiesConfigurationArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 frequency: Optional[pulumi.Input[int]] = None,
                 kind: Optional[pulumi.Input['WebTestKind']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 locations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WebTestGeolocationArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 retry_enabled: Optional[pulumi.Input[bool]] = None,
                 synthetic_monitor_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeout: Optional[pulumi.Input[int]] = None,
                 web_test_kind: Optional[pulumi.Input['WebTestKind']] = None,
                 web_test_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An Application Insights web test definition.
        API Version: 2015-05-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['WebTestPropertiesConfigurationArgs']] configuration: An XML configuration specification for a WebTest.
        :param pulumi.Input[str] description: Purpose/user defined descriptive test for this WebTest.
        :param pulumi.Input[bool] enabled: Is the test actively being monitored.
        :param pulumi.Input[int] frequency: Interval in seconds between test runs for this WebTest. Default value is 300.
        :param pulumi.Input['WebTestKind'] kind: The kind of web test that this web test watches. Choices are ping and multistep.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WebTestGeolocationArgs']]]] locations: A list of where to physically run the tests from to give global coverage for accessibility of your application.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[bool] retry_enabled: Allow for retries should this WebTest fail.
        :param pulumi.Input[str] synthetic_monitor_id: Unique ID of this WebTest. This is typically the same value as the Name field.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[int] timeout: Seconds until this WebTest will timeout and fail. Default value is 30.
        :param pulumi.Input['WebTestKind'] web_test_kind: The kind of web test this is, valid choices are ping and multistep.
        :param pulumi.Input[str] web_test_name: User defined name if this WebTest.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WebTestArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An Application Insights web test definition.
        API Version: 2015-05-01.

        :param str resource_name: The name of the resource.
        :param WebTestArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WebTestArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration: Optional[pulumi.Input[pulumi.InputType['WebTestPropertiesConfigurationArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 frequency: Optional[pulumi.Input[int]] = None,
                 kind: Optional[pulumi.Input['WebTestKind']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 locations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WebTestGeolocationArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 retry_enabled: Optional[pulumi.Input[bool]] = None,
                 synthetic_monitor_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeout: Optional[pulumi.Input[int]] = None,
                 web_test_kind: Optional[pulumi.Input['WebTestKind']] = None,
                 web_test_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = WebTestArgs.__new__(WebTestArgs)

            __props__.__dict__["configuration"] = configuration
            __props__.__dict__["description"] = description
            __props__.__dict__["enabled"] = enabled
            if frequency is None:
                frequency = 300
            __props__.__dict__["frequency"] = frequency
            if kind is None:
                kind = 'ping'
            __props__.__dict__["kind"] = kind
            __props__.__dict__["location"] = location
            if locations is None and not opts.urn:
                raise TypeError("Missing required property 'locations'")
            __props__.__dict__["locations"] = locations
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["retry_enabled"] = retry_enabled
            if synthetic_monitor_id is None and not opts.urn:
                raise TypeError("Missing required property 'synthetic_monitor_id'")
            __props__.__dict__["synthetic_monitor_id"] = synthetic_monitor_id
            __props__.__dict__["tags"] = tags
            if timeout is None:
                timeout = 30
            __props__.__dict__["timeout"] = timeout
            if web_test_kind is None:
                web_test_kind = 'ping'
            if web_test_kind is None and not opts.urn:
                raise TypeError("Missing required property 'web_test_kind'")
            __props__.__dict__["web_test_kind"] = web_test_kind
            __props__.__dict__["web_test_name"] = web_test_name
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:insights/v20150501:WebTest"), pulumi.Alias(type_="azure-native:insights/v20180501preview:WebTest"), pulumi.Alias(type_="azure-native:insights/v20201005preview:WebTest"), pulumi.Alias(type_="azure-native:insights/v20220615:WebTest")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebTest, __self__).__init__(
            'azure-native:insights:WebTest',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebTest':
        """
        Get an existing WebTest resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = WebTestArgs.__new__(WebTestArgs)

        __props__.__dict__["configuration"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["enabled"] = None
        __props__.__dict__["frequency"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["locations"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["retry_enabled"] = None
        __props__.__dict__["synthetic_monitor_id"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["timeout"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["web_test_kind"] = None
        __props__.__dict__["web_test_name"] = None
        return WebTest(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def configuration(self) -> pulumi.Output[Optional['outputs.WebTestPropertiesResponseConfiguration']]:
        """
        An XML configuration specification for a WebTest.
        """
        return pulumi.get(self, "configuration")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Purpose/user defined descriptive test for this WebTest.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Is the test actively being monitored.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def frequency(self) -> pulumi.Output[Optional[int]]:
        """
        Interval in seconds between test runs for this WebTest. Default value is 300.
        """
        return pulumi.get(self, "frequency")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        The kind of web test that this web test watches. Choices are ping and multistep.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def locations(self) -> pulumi.Output[Sequence['outputs.WebTestGeolocationResponse']]:
        """
        A list of where to physically run the tests from to give global coverage for accessibility of your application.
        """
        return pulumi.get(self, "locations")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Current state of this component, whether or not is has been provisioned within the resource group it is defined. Users cannot change this value but are able to read from it. Values will include Succeeded, Deploying, Canceled, and Failed.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="retryEnabled")
    def retry_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Allow for retries should this WebTest fail.
        """
        return pulumi.get(self, "retry_enabled")

    @property
    @pulumi.getter(name="syntheticMonitorId")
    def synthetic_monitor_id(self) -> pulumi.Output[str]:
        """
        Unique ID of this WebTest. This is typically the same value as the Name field.
        """
        return pulumi.get(self, "synthetic_monitor_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def timeout(self) -> pulumi.Output[Optional[int]]:
        """
        Seconds until this WebTest will timeout and fail. Default value is 30.
        """
        return pulumi.get(self, "timeout")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="webTestKind")
    def web_test_kind(self) -> pulumi.Output[str]:
        """
        The kind of web test this is, valid choices are ping and multistep.
        """
        return pulumi.get(self, "web_test_kind")

    @property
    @pulumi.getter(name="webTestName")
    def web_test_name(self) -> pulumi.Output[str]:
        """
        User defined name if this WebTest.
        """
        return pulumi.get(self, "web_test_name")

