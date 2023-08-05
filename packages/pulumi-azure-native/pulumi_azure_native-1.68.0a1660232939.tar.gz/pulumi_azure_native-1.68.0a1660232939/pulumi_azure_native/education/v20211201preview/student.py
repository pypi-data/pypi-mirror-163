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

__all__ = ['StudentArgs', 'Student']

@pulumi.input_type
class StudentArgs:
    def __init__(__self__, *,
                 billing_account_name: pulumi.Input[str],
                 billing_profile_name: pulumi.Input[str],
                 budget: pulumi.Input['AmountArgs'],
                 email: pulumi.Input[str],
                 expiration_date: pulumi.Input[str],
                 first_name: pulumi.Input[str],
                 invoice_section_name: pulumi.Input[str],
                 last_name: pulumi.Input[str],
                 role: pulumi.Input[Union[str, 'StudentRole']],
                 student_alias: Optional[pulumi.Input[str]] = None,
                 subscription_alias: Optional[pulumi.Input[str]] = None,
                 subscription_invite_last_sent_date: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Student resource.
        :param pulumi.Input[str] billing_account_name: Billing account name.
        :param pulumi.Input[str] billing_profile_name: Billing profile name.
        :param pulumi.Input['AmountArgs'] budget: Student Budget
        :param pulumi.Input[str] email: Student Email
        :param pulumi.Input[str] expiration_date: Date this student is set to expire from the lab.
        :param pulumi.Input[str] first_name: First Name
        :param pulumi.Input[str] invoice_section_name: Invoice section name.
        :param pulumi.Input[str] last_name: Last Name
        :param pulumi.Input[Union[str, 'StudentRole']] role: Student Role
        :param pulumi.Input[str] student_alias: Student alias.
        :param pulumi.Input[str] subscription_alias: Subscription alias
        :param pulumi.Input[str] subscription_invite_last_sent_date: subscription invite last sent date
        """
        pulumi.set(__self__, "billing_account_name", billing_account_name)
        pulumi.set(__self__, "billing_profile_name", billing_profile_name)
        pulumi.set(__self__, "budget", budget)
        pulumi.set(__self__, "email", email)
        pulumi.set(__self__, "expiration_date", expiration_date)
        pulumi.set(__self__, "first_name", first_name)
        pulumi.set(__self__, "invoice_section_name", invoice_section_name)
        pulumi.set(__self__, "last_name", last_name)
        pulumi.set(__self__, "role", role)
        if student_alias is not None:
            pulumi.set(__self__, "student_alias", student_alias)
        if subscription_alias is not None:
            pulumi.set(__self__, "subscription_alias", subscription_alias)
        if subscription_invite_last_sent_date is not None:
            pulumi.set(__self__, "subscription_invite_last_sent_date", subscription_invite_last_sent_date)

    @property
    @pulumi.getter(name="billingAccountName")
    def billing_account_name(self) -> pulumi.Input[str]:
        """
        Billing account name.
        """
        return pulumi.get(self, "billing_account_name")

    @billing_account_name.setter
    def billing_account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "billing_account_name", value)

    @property
    @pulumi.getter(name="billingProfileName")
    def billing_profile_name(self) -> pulumi.Input[str]:
        """
        Billing profile name.
        """
        return pulumi.get(self, "billing_profile_name")

    @billing_profile_name.setter
    def billing_profile_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "billing_profile_name", value)

    @property
    @pulumi.getter
    def budget(self) -> pulumi.Input['AmountArgs']:
        """
        Student Budget
        """
        return pulumi.get(self, "budget")

    @budget.setter
    def budget(self, value: pulumi.Input['AmountArgs']):
        pulumi.set(self, "budget", value)

    @property
    @pulumi.getter
    def email(self) -> pulumi.Input[str]:
        """
        Student Email
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: pulumi.Input[str]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> pulumi.Input[str]:
        """
        Date this student is set to expire from the lab.
        """
        return pulumi.get(self, "expiration_date")

    @expiration_date.setter
    def expiration_date(self, value: pulumi.Input[str]):
        pulumi.set(self, "expiration_date", value)

    @property
    @pulumi.getter(name="firstName")
    def first_name(self) -> pulumi.Input[str]:
        """
        First Name
        """
        return pulumi.get(self, "first_name")

    @first_name.setter
    def first_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "first_name", value)

    @property
    @pulumi.getter(name="invoiceSectionName")
    def invoice_section_name(self) -> pulumi.Input[str]:
        """
        Invoice section name.
        """
        return pulumi.get(self, "invoice_section_name")

    @invoice_section_name.setter
    def invoice_section_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "invoice_section_name", value)

    @property
    @pulumi.getter(name="lastName")
    def last_name(self) -> pulumi.Input[str]:
        """
        Last Name
        """
        return pulumi.get(self, "last_name")

    @last_name.setter
    def last_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "last_name", value)

    @property
    @pulumi.getter
    def role(self) -> pulumi.Input[Union[str, 'StudentRole']]:
        """
        Student Role
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: pulumi.Input[Union[str, 'StudentRole']]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter(name="studentAlias")
    def student_alias(self) -> Optional[pulumi.Input[str]]:
        """
        Student alias.
        """
        return pulumi.get(self, "student_alias")

    @student_alias.setter
    def student_alias(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "student_alias", value)

    @property
    @pulumi.getter(name="subscriptionAlias")
    def subscription_alias(self) -> Optional[pulumi.Input[str]]:
        """
        Subscription alias
        """
        return pulumi.get(self, "subscription_alias")

    @subscription_alias.setter
    def subscription_alias(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subscription_alias", value)

    @property
    @pulumi.getter(name="subscriptionInviteLastSentDate")
    def subscription_invite_last_sent_date(self) -> Optional[pulumi.Input[str]]:
        """
        subscription invite last sent date
        """
        return pulumi.get(self, "subscription_invite_last_sent_date")

    @subscription_invite_last_sent_date.setter
    def subscription_invite_last_sent_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subscription_invite_last_sent_date", value)


class Student(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 billing_account_name: Optional[pulumi.Input[str]] = None,
                 billing_profile_name: Optional[pulumi.Input[str]] = None,
                 budget: Optional[pulumi.Input[pulumi.InputType['AmountArgs']]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 expiration_date: Optional[pulumi.Input[str]] = None,
                 first_name: Optional[pulumi.Input[str]] = None,
                 invoice_section_name: Optional[pulumi.Input[str]] = None,
                 last_name: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[Union[str, 'StudentRole']]] = None,
                 student_alias: Optional[pulumi.Input[str]] = None,
                 subscription_alias: Optional[pulumi.Input[str]] = None,
                 subscription_invite_last_sent_date: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Student details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] billing_account_name: Billing account name.
        :param pulumi.Input[str] billing_profile_name: Billing profile name.
        :param pulumi.Input[pulumi.InputType['AmountArgs']] budget: Student Budget
        :param pulumi.Input[str] email: Student Email
        :param pulumi.Input[str] expiration_date: Date this student is set to expire from the lab.
        :param pulumi.Input[str] first_name: First Name
        :param pulumi.Input[str] invoice_section_name: Invoice section name.
        :param pulumi.Input[str] last_name: Last Name
        :param pulumi.Input[Union[str, 'StudentRole']] role: Student Role
        :param pulumi.Input[str] student_alias: Student alias.
        :param pulumi.Input[str] subscription_alias: Subscription alias
        :param pulumi.Input[str] subscription_invite_last_sent_date: subscription invite last sent date
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StudentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Student details.

        :param str resource_name: The name of the resource.
        :param StudentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StudentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 billing_account_name: Optional[pulumi.Input[str]] = None,
                 billing_profile_name: Optional[pulumi.Input[str]] = None,
                 budget: Optional[pulumi.Input[pulumi.InputType['AmountArgs']]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 expiration_date: Optional[pulumi.Input[str]] = None,
                 first_name: Optional[pulumi.Input[str]] = None,
                 invoice_section_name: Optional[pulumi.Input[str]] = None,
                 last_name: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[Union[str, 'StudentRole']]] = None,
                 student_alias: Optional[pulumi.Input[str]] = None,
                 subscription_alias: Optional[pulumi.Input[str]] = None,
                 subscription_invite_last_sent_date: Optional[pulumi.Input[str]] = None,
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
            __props__ = StudentArgs.__new__(StudentArgs)

            if billing_account_name is None and not opts.urn:
                raise TypeError("Missing required property 'billing_account_name'")
            __props__.__dict__["billing_account_name"] = billing_account_name
            if billing_profile_name is None and not opts.urn:
                raise TypeError("Missing required property 'billing_profile_name'")
            __props__.__dict__["billing_profile_name"] = billing_profile_name
            if budget is None and not opts.urn:
                raise TypeError("Missing required property 'budget'")
            __props__.__dict__["budget"] = budget
            if email is None and not opts.urn:
                raise TypeError("Missing required property 'email'")
            __props__.__dict__["email"] = email
            if expiration_date is None and not opts.urn:
                raise TypeError("Missing required property 'expiration_date'")
            __props__.__dict__["expiration_date"] = expiration_date
            if first_name is None and not opts.urn:
                raise TypeError("Missing required property 'first_name'")
            __props__.__dict__["first_name"] = first_name
            if invoice_section_name is None and not opts.urn:
                raise TypeError("Missing required property 'invoice_section_name'")
            __props__.__dict__["invoice_section_name"] = invoice_section_name
            if last_name is None and not opts.urn:
                raise TypeError("Missing required property 'last_name'")
            __props__.__dict__["last_name"] = last_name
            if role is None and not opts.urn:
                raise TypeError("Missing required property 'role'")
            __props__.__dict__["role"] = role
            __props__.__dict__["student_alias"] = student_alias
            __props__.__dict__["subscription_alias"] = subscription_alias
            __props__.__dict__["subscription_invite_last_sent_date"] = subscription_invite_last_sent_date
            __props__.__dict__["effective_date"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["subscription_id"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:education:Student")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Student, __self__).__init__(
            'azure-native:education/v20211201preview:Student',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Student':
        """
        Get an existing Student resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = StudentArgs.__new__(StudentArgs)

        __props__.__dict__["budget"] = None
        __props__.__dict__["effective_date"] = None
        __props__.__dict__["email"] = None
        __props__.__dict__["expiration_date"] = None
        __props__.__dict__["first_name"] = None
        __props__.__dict__["last_name"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["role"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["subscription_alias"] = None
        __props__.__dict__["subscription_id"] = None
        __props__.__dict__["subscription_invite_last_sent_date"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return Student(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def budget(self) -> pulumi.Output['outputs.AmountResponse']:
        """
        Student Budget
        """
        return pulumi.get(self, "budget")

    @property
    @pulumi.getter(name="effectiveDate")
    def effective_date(self) -> pulumi.Output[str]:
        """
        Date student was added to the lab
        """
        return pulumi.get(self, "effective_date")

    @property
    @pulumi.getter
    def email(self) -> pulumi.Output[str]:
        """
        Student Email
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> pulumi.Output[str]:
        """
        Date this student is set to expire from the lab.
        """
        return pulumi.get(self, "expiration_date")

    @property
    @pulumi.getter(name="firstName")
    def first_name(self) -> pulumi.Output[str]:
        """
        First Name
        """
        return pulumi.get(self, "first_name")

    @property
    @pulumi.getter(name="lastName")
    def last_name(self) -> pulumi.Output[str]:
        """
        Last Name
        """
        return pulumi.get(self, "last_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        """
        Student Role
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Student Lab Status
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="subscriptionAlias")
    def subscription_alias(self) -> pulumi.Output[Optional[str]]:
        """
        Subscription alias
        """
        return pulumi.get(self, "subscription_alias")

    @property
    @pulumi.getter(name="subscriptionId")
    def subscription_id(self) -> pulumi.Output[str]:
        """
        Subscription Id
        """
        return pulumi.get(self, "subscription_id")

    @property
    @pulumi.getter(name="subscriptionInviteLastSentDate")
    def subscription_invite_last_sent_date(self) -> pulumi.Output[Optional[str]]:
        """
        subscription invite last sent date
        """
        return pulumi.get(self, "subscription_invite_last_sent_date")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

