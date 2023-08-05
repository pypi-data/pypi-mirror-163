# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetEventSubscriptionFullUrlResult',
    'AwaitableGetEventSubscriptionFullUrlResult',
    'get_event_subscription_full_url',
    'get_event_subscription_full_url_output',
]

@pulumi.output_type
class GetEventSubscriptionFullUrlResult:
    """
    Full endpoint url of an event subscription
    """
    def __init__(__self__, endpoint_url=None):
        if endpoint_url and not isinstance(endpoint_url, str):
            raise TypeError("Expected argument 'endpoint_url' to be a str")
        pulumi.set(__self__, "endpoint_url", endpoint_url)

    @property
    @pulumi.getter(name="endpointUrl")
    def endpoint_url(self) -> Optional[str]:
        """
        The URL that represents the endpoint of the destination of an event subscription.
        """
        return pulumi.get(self, "endpoint_url")


class AwaitableGetEventSubscriptionFullUrlResult(GetEventSubscriptionFullUrlResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEventSubscriptionFullUrlResult(
            endpoint_url=self.endpoint_url)


def get_event_subscription_full_url(event_subscription_name: Optional[str] = None,
                                    scope: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEventSubscriptionFullUrlResult:
    """
    Full endpoint url of an event subscription
    API Version: 2020-06-01.


    :param str event_subscription_name: Name of the event subscription.
    :param str scope: The scope of the event subscription. The scope can be a subscription, or a resource group, or a top level resource belonging to a resource provider namespace, or an EventGrid topic. For example, use '/subscriptions/{subscriptionId}/' for a subscription, '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}' for a resource group, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}' for a resource, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}' for an EventGrid topic.
    """
    __args__ = dict()
    __args__['eventSubscriptionName'] = event_subscription_name
    __args__['scope'] = scope
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:eventgrid:getEventSubscriptionFullUrl', __args__, opts=opts, typ=GetEventSubscriptionFullUrlResult).value

    return AwaitableGetEventSubscriptionFullUrlResult(
        endpoint_url=__ret__.endpoint_url)


@_utilities.lift_output_func(get_event_subscription_full_url)
def get_event_subscription_full_url_output(event_subscription_name: Optional[pulumi.Input[str]] = None,
                                           scope: Optional[pulumi.Input[str]] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEventSubscriptionFullUrlResult]:
    """
    Full endpoint url of an event subscription
    API Version: 2020-06-01.


    :param str event_subscription_name: Name of the event subscription.
    :param str scope: The scope of the event subscription. The scope can be a subscription, or a resource group, or a top level resource belonging to a resource provider namespace, or an EventGrid topic. For example, use '/subscriptions/{subscriptionId}/' for a subscription, '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}' for a resource group, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}' for a resource, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}' for an EventGrid topic.
    """
    ...
