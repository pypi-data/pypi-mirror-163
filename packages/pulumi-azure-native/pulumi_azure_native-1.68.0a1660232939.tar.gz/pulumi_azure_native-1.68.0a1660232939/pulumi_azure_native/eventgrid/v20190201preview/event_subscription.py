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
from ._inputs import *

__all__ = ['EventSubscriptionArgs', 'EventSubscription']

@pulumi.input_type
class EventSubscriptionArgs:
    def __init__(__self__, *,
                 scope: pulumi.Input[str],
                 dead_letter_destination: Optional[pulumi.Input['StorageBlobDeadLetterDestinationArgs']] = None,
                 destination: Optional[pulumi.Input[Union['EventHubEventSubscriptionDestinationArgs', 'HybridConnectionEventSubscriptionDestinationArgs', 'ServiceBusQueueEventSubscriptionDestinationArgs', 'StorageQueueEventSubscriptionDestinationArgs', 'WebHookEventSubscriptionDestinationArgs']]] = None,
                 event_delivery_schema: Optional[pulumi.Input[Union[str, 'EventDeliverySchema']]] = None,
                 event_subscription_name: Optional[pulumi.Input[str]] = None,
                 expiration_time_utc: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input['EventSubscriptionFilterArgs']] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 retry_policy: Optional[pulumi.Input['RetryPolicyArgs']] = None):
        """
        The set of arguments for constructing a EventSubscription resource.
        :param pulumi.Input[str] scope: The identifier of the resource to which the event subscription needs to be created or updated. The scope can be a subscription, or a resource group, or a top level resource belonging to a resource provider namespace, or an EventGrid topic. For example, use '/subscriptions/{subscriptionId}/' for a subscription, '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}' for a resource group, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}' for a resource, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}' for an EventGrid topic.
        :param pulumi.Input['StorageBlobDeadLetterDestinationArgs'] dead_letter_destination: The DeadLetter destination of the event subscription.
        :param pulumi.Input[Union['EventHubEventSubscriptionDestinationArgs', 'HybridConnectionEventSubscriptionDestinationArgs', 'ServiceBusQueueEventSubscriptionDestinationArgs', 'StorageQueueEventSubscriptionDestinationArgs', 'WebHookEventSubscriptionDestinationArgs']] destination: Information about the destination where events have to be delivered for the event subscription.
        :param pulumi.Input[Union[str, 'EventDeliverySchema']] event_delivery_schema: The event delivery schema for the event subscription.
        :param pulumi.Input[str] event_subscription_name: Name of the event subscription. Event subscription names must be between 3 and 64 characters in length and should use alphanumeric letters only.
        :param pulumi.Input[str] expiration_time_utc: Expiration time of the event subscription.
        :param pulumi.Input['EventSubscriptionFilterArgs'] filter: Information about the filter for the event subscription.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] labels: List of user defined labels.
        :param pulumi.Input['RetryPolicyArgs'] retry_policy: The retry policy for events. This can be used to configure maximum number of delivery attempts and time to live for events.
        """
        pulumi.set(__self__, "scope", scope)
        if dead_letter_destination is not None:
            pulumi.set(__self__, "dead_letter_destination", dead_letter_destination)
        if destination is not None:
            pulumi.set(__self__, "destination", destination)
        if event_delivery_schema is not None:
            pulumi.set(__self__, "event_delivery_schema", event_delivery_schema)
        if event_subscription_name is not None:
            pulumi.set(__self__, "event_subscription_name", event_subscription_name)
        if expiration_time_utc is not None:
            pulumi.set(__self__, "expiration_time_utc", expiration_time_utc)
        if filter is not None:
            pulumi.set(__self__, "filter", filter)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if retry_policy is not None:
            pulumi.set(__self__, "retry_policy", retry_policy)

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Input[str]:
        """
        The identifier of the resource to which the event subscription needs to be created or updated. The scope can be a subscription, or a resource group, or a top level resource belonging to a resource provider namespace, or an EventGrid topic. For example, use '/subscriptions/{subscriptionId}/' for a subscription, '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}' for a resource group, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}' for a resource, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}' for an EventGrid topic.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: pulumi.Input[str]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter(name="deadLetterDestination")
    def dead_letter_destination(self) -> Optional[pulumi.Input['StorageBlobDeadLetterDestinationArgs']]:
        """
        The DeadLetter destination of the event subscription.
        """
        return pulumi.get(self, "dead_letter_destination")

    @dead_letter_destination.setter
    def dead_letter_destination(self, value: Optional[pulumi.Input['StorageBlobDeadLetterDestinationArgs']]):
        pulumi.set(self, "dead_letter_destination", value)

    @property
    @pulumi.getter
    def destination(self) -> Optional[pulumi.Input[Union['EventHubEventSubscriptionDestinationArgs', 'HybridConnectionEventSubscriptionDestinationArgs', 'ServiceBusQueueEventSubscriptionDestinationArgs', 'StorageQueueEventSubscriptionDestinationArgs', 'WebHookEventSubscriptionDestinationArgs']]]:
        """
        Information about the destination where events have to be delivered for the event subscription.
        """
        return pulumi.get(self, "destination")

    @destination.setter
    def destination(self, value: Optional[pulumi.Input[Union['EventHubEventSubscriptionDestinationArgs', 'HybridConnectionEventSubscriptionDestinationArgs', 'ServiceBusQueueEventSubscriptionDestinationArgs', 'StorageQueueEventSubscriptionDestinationArgs', 'WebHookEventSubscriptionDestinationArgs']]]):
        pulumi.set(self, "destination", value)

    @property
    @pulumi.getter(name="eventDeliverySchema")
    def event_delivery_schema(self) -> Optional[pulumi.Input[Union[str, 'EventDeliverySchema']]]:
        """
        The event delivery schema for the event subscription.
        """
        return pulumi.get(self, "event_delivery_schema")

    @event_delivery_schema.setter
    def event_delivery_schema(self, value: Optional[pulumi.Input[Union[str, 'EventDeliverySchema']]]):
        pulumi.set(self, "event_delivery_schema", value)

    @property
    @pulumi.getter(name="eventSubscriptionName")
    def event_subscription_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the event subscription. Event subscription names must be between 3 and 64 characters in length and should use alphanumeric letters only.
        """
        return pulumi.get(self, "event_subscription_name")

    @event_subscription_name.setter
    def event_subscription_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "event_subscription_name", value)

    @property
    @pulumi.getter(name="expirationTimeUtc")
    def expiration_time_utc(self) -> Optional[pulumi.Input[str]]:
        """
        Expiration time of the event subscription.
        """
        return pulumi.get(self, "expiration_time_utc")

    @expiration_time_utc.setter
    def expiration_time_utc(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expiration_time_utc", value)

    @property
    @pulumi.getter
    def filter(self) -> Optional[pulumi.Input['EventSubscriptionFilterArgs']]:
        """
        Information about the filter for the event subscription.
        """
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: Optional[pulumi.Input['EventSubscriptionFilterArgs']]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of user defined labels.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter(name="retryPolicy")
    def retry_policy(self) -> Optional[pulumi.Input['RetryPolicyArgs']]:
        """
        The retry policy for events. This can be used to configure maximum number of delivery attempts and time to live for events.
        """
        return pulumi.get(self, "retry_policy")

    @retry_policy.setter
    def retry_policy(self, value: Optional[pulumi.Input['RetryPolicyArgs']]):
        pulumi.set(self, "retry_policy", value)


warnings.warn("""Version 2019-02-01-preview will be removed in v2 of the provider.""", DeprecationWarning)


class EventSubscription(pulumi.CustomResource):
    warnings.warn("""Version 2019-02-01-preview will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dead_letter_destination: Optional[pulumi.Input[pulumi.InputType['StorageBlobDeadLetterDestinationArgs']]] = None,
                 destination: Optional[pulumi.Input[Union[pulumi.InputType['EventHubEventSubscriptionDestinationArgs'], pulumi.InputType['HybridConnectionEventSubscriptionDestinationArgs'], pulumi.InputType['ServiceBusQueueEventSubscriptionDestinationArgs'], pulumi.InputType['StorageQueueEventSubscriptionDestinationArgs'], pulumi.InputType['WebHookEventSubscriptionDestinationArgs']]]] = None,
                 event_delivery_schema: Optional[pulumi.Input[Union[str, 'EventDeliverySchema']]] = None,
                 event_subscription_name: Optional[pulumi.Input[str]] = None,
                 expiration_time_utc: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input[pulumi.InputType['EventSubscriptionFilterArgs']]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 retry_policy: Optional[pulumi.Input[pulumi.InputType['RetryPolicyArgs']]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Event Subscription

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['StorageBlobDeadLetterDestinationArgs']] dead_letter_destination: The DeadLetter destination of the event subscription.
        :param pulumi.Input[Union[pulumi.InputType['EventHubEventSubscriptionDestinationArgs'], pulumi.InputType['HybridConnectionEventSubscriptionDestinationArgs'], pulumi.InputType['ServiceBusQueueEventSubscriptionDestinationArgs'], pulumi.InputType['StorageQueueEventSubscriptionDestinationArgs'], pulumi.InputType['WebHookEventSubscriptionDestinationArgs']]] destination: Information about the destination where events have to be delivered for the event subscription.
        :param pulumi.Input[Union[str, 'EventDeliverySchema']] event_delivery_schema: The event delivery schema for the event subscription.
        :param pulumi.Input[str] event_subscription_name: Name of the event subscription. Event subscription names must be between 3 and 64 characters in length and should use alphanumeric letters only.
        :param pulumi.Input[str] expiration_time_utc: Expiration time of the event subscription.
        :param pulumi.Input[pulumi.InputType['EventSubscriptionFilterArgs']] filter: Information about the filter for the event subscription.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] labels: List of user defined labels.
        :param pulumi.Input[pulumi.InputType['RetryPolicyArgs']] retry_policy: The retry policy for events. This can be used to configure maximum number of delivery attempts and time to live for events.
        :param pulumi.Input[str] scope: The identifier of the resource to which the event subscription needs to be created or updated. The scope can be a subscription, or a resource group, or a top level resource belonging to a resource provider namespace, or an EventGrid topic. For example, use '/subscriptions/{subscriptionId}/' for a subscription, '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}' for a resource group, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}' for a resource, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}' for an EventGrid topic.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EventSubscriptionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Event Subscription

        :param str resource_name: The name of the resource.
        :param EventSubscriptionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EventSubscriptionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dead_letter_destination: Optional[pulumi.Input[pulumi.InputType['StorageBlobDeadLetterDestinationArgs']]] = None,
                 destination: Optional[pulumi.Input[Union[pulumi.InputType['EventHubEventSubscriptionDestinationArgs'], pulumi.InputType['HybridConnectionEventSubscriptionDestinationArgs'], pulumi.InputType['ServiceBusQueueEventSubscriptionDestinationArgs'], pulumi.InputType['StorageQueueEventSubscriptionDestinationArgs'], pulumi.InputType['WebHookEventSubscriptionDestinationArgs']]]] = None,
                 event_delivery_schema: Optional[pulumi.Input[Union[str, 'EventDeliverySchema']]] = None,
                 event_subscription_name: Optional[pulumi.Input[str]] = None,
                 expiration_time_utc: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input[pulumi.InputType['EventSubscriptionFilterArgs']]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 retry_policy: Optional[pulumi.Input[pulumi.InputType['RetryPolicyArgs']]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""EventSubscription is deprecated: Version 2019-02-01-preview will be removed in v2 of the provider.""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EventSubscriptionArgs.__new__(EventSubscriptionArgs)

            __props__.__dict__["dead_letter_destination"] = dead_letter_destination
            __props__.__dict__["destination"] = destination
            __props__.__dict__["event_delivery_schema"] = event_delivery_schema
            __props__.__dict__["event_subscription_name"] = event_subscription_name
            __props__.__dict__["expiration_time_utc"] = expiration_time_utc
            __props__.__dict__["filter"] = filter
            __props__.__dict__["labels"] = labels
            __props__.__dict__["retry_policy"] = retry_policy
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__.__dict__["scope"] = scope
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["topic"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:eventgrid:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20170615preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20170915preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20180101:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20180501preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20180915preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20190101:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20190601:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20200101preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20200401preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20200601:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20201015preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20210601preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20211015preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20211201:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20220615:EventSubscription")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(EventSubscription, __self__).__init__(
            'azure-native:eventgrid/v20190201preview:EventSubscription',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'EventSubscription':
        """
        Get an existing EventSubscription resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = EventSubscriptionArgs.__new__(EventSubscriptionArgs)

        __props__.__dict__["dead_letter_destination"] = None
        __props__.__dict__["destination"] = None
        __props__.__dict__["event_delivery_schema"] = None
        __props__.__dict__["expiration_time_utc"] = None
        __props__.__dict__["filter"] = None
        __props__.__dict__["labels"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["retry_policy"] = None
        __props__.__dict__["topic"] = None
        __props__.__dict__["type"] = None
        return EventSubscription(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="deadLetterDestination")
    def dead_letter_destination(self) -> pulumi.Output[Optional['outputs.StorageBlobDeadLetterDestinationResponse']]:
        """
        The DeadLetter destination of the event subscription.
        """
        return pulumi.get(self, "dead_letter_destination")

    @property
    @pulumi.getter
    def destination(self) -> pulumi.Output[Optional[Any]]:
        """
        Information about the destination where events have to be delivered for the event subscription.
        """
        return pulumi.get(self, "destination")

    @property
    @pulumi.getter(name="eventDeliverySchema")
    def event_delivery_schema(self) -> pulumi.Output[Optional[str]]:
        """
        The event delivery schema for the event subscription.
        """
        return pulumi.get(self, "event_delivery_schema")

    @property
    @pulumi.getter(name="expirationTimeUtc")
    def expiration_time_utc(self) -> pulumi.Output[Optional[str]]:
        """
        Expiration time of the event subscription.
        """
        return pulumi.get(self, "expiration_time_utc")

    @property
    @pulumi.getter
    def filter(self) -> pulumi.Output[Optional['outputs.EventSubscriptionFilterResponse']]:
        """
        Information about the filter for the event subscription.
        """
        return pulumi.get(self, "filter")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of user defined labels.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the event subscription.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="retryPolicy")
    def retry_policy(self) -> pulumi.Output[Optional['outputs.RetryPolicyResponse']]:
        """
        The retry policy for events. This can be used to configure maximum number of delivery attempts and time to live for events.
        """
        return pulumi.get(self, "retry_policy")

    @property
    @pulumi.getter
    def topic(self) -> pulumi.Output[str]:
        """
        Name of the topic of the event subscription.
        """
        return pulumi.get(self, "topic")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the resource
        """
        return pulumi.get(self, "type")

