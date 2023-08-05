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
    'GetWorkspaceResult',
    'AwaitableGetWorkspaceResult',
    'get_workspace',
    'get_workspace_output',
]

@pulumi.output_type
class GetWorkspaceResult:
    """
    Information about workspace.
    """
    def __init__(__self__, authorizations=None, created_by=None, created_date_time=None, encryption=None, id=None, location=None, managed_resource_group_id=None, name=None, parameters=None, private_endpoint_connections=None, provisioning_state=None, public_network_access=None, required_nsg_rules=None, sku=None, storage_account_identity=None, system_data=None, tags=None, type=None, ui_definition_uri=None, updated_by=None, workspace_id=None, workspace_url=None):
        if authorizations and not isinstance(authorizations, list):
            raise TypeError("Expected argument 'authorizations' to be a list")
        pulumi.set(__self__, "authorizations", authorizations)
        if created_by and not isinstance(created_by, dict):
            raise TypeError("Expected argument 'created_by' to be a dict")
        pulumi.set(__self__, "created_by", created_by)
        if created_date_time and not isinstance(created_date_time, str):
            raise TypeError("Expected argument 'created_date_time' to be a str")
        pulumi.set(__self__, "created_date_time", created_date_time)
        if encryption and not isinstance(encryption, dict):
            raise TypeError("Expected argument 'encryption' to be a dict")
        pulumi.set(__self__, "encryption", encryption)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if managed_resource_group_id and not isinstance(managed_resource_group_id, str):
            raise TypeError("Expected argument 'managed_resource_group_id' to be a str")
        pulumi.set(__self__, "managed_resource_group_id", managed_resource_group_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if parameters and not isinstance(parameters, dict):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, "parameters", parameters)
        if private_endpoint_connections and not isinstance(private_endpoint_connections, list):
            raise TypeError("Expected argument 'private_endpoint_connections' to be a list")
        pulumi.set(__self__, "private_endpoint_connections", private_endpoint_connections)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if public_network_access and not isinstance(public_network_access, str):
            raise TypeError("Expected argument 'public_network_access' to be a str")
        pulumi.set(__self__, "public_network_access", public_network_access)
        if required_nsg_rules and not isinstance(required_nsg_rules, str):
            raise TypeError("Expected argument 'required_nsg_rules' to be a str")
        pulumi.set(__self__, "required_nsg_rules", required_nsg_rules)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if storage_account_identity and not isinstance(storage_account_identity, dict):
            raise TypeError("Expected argument 'storage_account_identity' to be a dict")
        pulumi.set(__self__, "storage_account_identity", storage_account_identity)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if ui_definition_uri and not isinstance(ui_definition_uri, str):
            raise TypeError("Expected argument 'ui_definition_uri' to be a str")
        pulumi.set(__self__, "ui_definition_uri", ui_definition_uri)
        if updated_by and not isinstance(updated_by, dict):
            raise TypeError("Expected argument 'updated_by' to be a dict")
        pulumi.set(__self__, "updated_by", updated_by)
        if workspace_id and not isinstance(workspace_id, str):
            raise TypeError("Expected argument 'workspace_id' to be a str")
        pulumi.set(__self__, "workspace_id", workspace_id)
        if workspace_url and not isinstance(workspace_url, str):
            raise TypeError("Expected argument 'workspace_url' to be a str")
        pulumi.set(__self__, "workspace_url", workspace_url)

    @property
    @pulumi.getter
    def authorizations(self) -> Optional[Sequence['outputs.WorkspaceProviderAuthorizationResponse']]:
        """
        The workspace provider authorizations.
        """
        return pulumi.get(self, "authorizations")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional['outputs.CreatedByResponse']:
        """
        Indicates the Object ID, PUID and Application ID of entity that created the workspace.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdDateTime")
    def created_date_time(self) -> str:
        """
        Specifies the date and time when the workspace is created.
        """
        return pulumi.get(self, "created_date_time")

    @property
    @pulumi.getter
    def encryption(self) -> Optional['outputs.WorkspacePropertiesResponseEncryption']:
        """
        Encryption properties for databricks workspace
        """
        return pulumi.get(self, "encryption")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedResourceGroupId")
    def managed_resource_group_id(self) -> str:
        """
        The managed resource group Id.
        """
        return pulumi.get(self, "managed_resource_group_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> Optional['outputs.WorkspaceCustomParametersResponse']:
        """
        The workspace's custom parameters.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> Sequence['outputs.PrivateEndpointConnectionResponse']:
        """
        Private endpoint connections created on the workspace
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The workspace provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[str]:
        """
        The network access type for accessing workspace. Set value to disabled to access workspace only via private link.
        """
        return pulumi.get(self, "public_network_access")

    @property
    @pulumi.getter(name="requiredNsgRules")
    def required_nsg_rules(self) -> Optional[str]:
        """
        Gets or sets a value indicating whether data plane (clusters) to control plane communication happen over private endpoint. Supported values are 'AllRules' and 'NoAzureDatabricksRules'. 'NoAzureServiceRules' value is for internal use only.
        """
        return pulumi.get(self, "required_nsg_rules")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.SkuResponse']:
        """
        The SKU of the resource.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="storageAccountIdentity")
    def storage_account_identity(self) -> Optional['outputs.ManagedIdentityConfigurationResponse']:
        """
        The details of Managed Identity of Storage Account
        """
        return pulumi.get(self, "storage_account_identity")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata relating to this resource
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. Ex- Microsoft.Compute/virtualMachines or Microsoft.Storage/storageAccounts.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="uiDefinitionUri")
    def ui_definition_uri(self) -> Optional[str]:
        """
        The blob URI where the UI definition file is located.
        """
        return pulumi.get(self, "ui_definition_uri")

    @property
    @pulumi.getter(name="updatedBy")
    def updated_by(self) -> Optional['outputs.CreatedByResponse']:
        """
        Indicates the Object ID, PUID and Application ID of entity that last updated the workspace.
        """
        return pulumi.get(self, "updated_by")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> str:
        """
        The unique identifier of the databricks workspace in databricks control plane.
        """
        return pulumi.get(self, "workspace_id")

    @property
    @pulumi.getter(name="workspaceUrl")
    def workspace_url(self) -> str:
        """
        The workspace URL which is of the format 'adb-{workspaceId}.{random}.azuredatabricks.net'
        """
        return pulumi.get(self, "workspace_url")


class AwaitableGetWorkspaceResult(GetWorkspaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkspaceResult(
            authorizations=self.authorizations,
            created_by=self.created_by,
            created_date_time=self.created_date_time,
            encryption=self.encryption,
            id=self.id,
            location=self.location,
            managed_resource_group_id=self.managed_resource_group_id,
            name=self.name,
            parameters=self.parameters,
            private_endpoint_connections=self.private_endpoint_connections,
            provisioning_state=self.provisioning_state,
            public_network_access=self.public_network_access,
            required_nsg_rules=self.required_nsg_rules,
            sku=self.sku,
            storage_account_identity=self.storage_account_identity,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type,
            ui_definition_uri=self.ui_definition_uri,
            updated_by=self.updated_by,
            workspace_id=self.workspace_id,
            workspace_url=self.workspace_url)


def get_workspace(resource_group_name: Optional[str] = None,
                  workspace_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkspaceResult:
    """
    Information about workspace.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:databricks/v20220401preview:getWorkspace', __args__, opts=opts, typ=GetWorkspaceResult).value

    return AwaitableGetWorkspaceResult(
        authorizations=__ret__.authorizations,
        created_by=__ret__.created_by,
        created_date_time=__ret__.created_date_time,
        encryption=__ret__.encryption,
        id=__ret__.id,
        location=__ret__.location,
        managed_resource_group_id=__ret__.managed_resource_group_id,
        name=__ret__.name,
        parameters=__ret__.parameters,
        private_endpoint_connections=__ret__.private_endpoint_connections,
        provisioning_state=__ret__.provisioning_state,
        public_network_access=__ret__.public_network_access,
        required_nsg_rules=__ret__.required_nsg_rules,
        sku=__ret__.sku,
        storage_account_identity=__ret__.storage_account_identity,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type,
        ui_definition_uri=__ret__.ui_definition_uri,
        updated_by=__ret__.updated_by,
        workspace_id=__ret__.workspace_id,
        workspace_url=__ret__.workspace_url)


@_utilities.lift_output_func(get_workspace)
def get_workspace_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                         workspace_name: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWorkspaceResult]:
    """
    Information about workspace.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    ...
