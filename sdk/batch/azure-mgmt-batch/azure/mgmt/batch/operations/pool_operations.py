# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

import uuid
from msrest.pipeline import ClientRawResponse
from msrestazure.azure_exceptions import CloudError
from msrest.exceptions import DeserializationError
from msrestazure.azure_operation import AzureOperationPoller

from .. import models


class PoolOperations(object):
    """PoolOperations operations.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    :ivar api_version: The API version to be used with the HTTP request. Constant value: "2018-12-01".
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):

        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self.api_version = "2018-12-01"

        self.config = config

    def list_by_batch_account(
            self, resource_group_name, account_name, maxresults=None, select=None, filter=None, custom_headers=None, raw=False, **operation_config):
        """Lists all of the pools in the specified account.

        :param resource_group_name: The name of the resource group that
         contains the Batch account.
        :type resource_group_name: str
        :param account_name: The name of the Batch account.
        :type account_name: str
        :param maxresults: The maximum number of items to return in the
         response.
        :type maxresults: int
        :param select: Comma separated list of properties that should be
         returned. e.g. "properties/provisioningState". Only top level
         properties under properties/ are valid for selection.
        :type select: str
        :param filter: OData filter expression. Valid properties for filtering
         are:
         name
         properties/allocationState
         properties/allocationStateTransitionTime
         properties/creationTime
         properties/provisioningState
         properties/provisioningStateTransitionTime
         properties/lastModified
         properties/vmSize
         properties/interNodeCommunication
         properties/scaleSettings/autoScale
         properties/scaleSettings/fixedScale
        :type filter: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: An iterator like instance of Pool
        :rtype:
         ~azure.mgmt.batch.models.PoolPaged[~azure.mgmt.batch.models.Pool]
        :raises: :class:`CloudError<msrestazure.azure_exceptions.CloudError>`
        """
        def internal_paging(next_link=None, raw=False):

            if not next_link:
                # Construct URL
                url = self.list_by_batch_account.metadata['url']
                path_format_arguments = {
                    'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
                    'accountName': self._serialize.url("account_name", account_name, 'str', max_length=24, min_length=3, pattern=r'^[-\w\._]+$'),
                    'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')
                }
                url = self._client.format_url(url, **path_format_arguments)

                # Construct parameters
                query_parameters = {}
                if maxresults is not None:
                    query_parameters['maxresults'] = self._serialize.query("maxresults", maxresults, 'int')
                if select is not None:
                    query_parameters['$select'] = self._serialize.query("select", select, 'str')
                if filter is not None:
                    query_parameters['$filter'] = self._serialize.query("filter", filter, 'str')
                query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

            else:
                url = next_link
                query_parameters = {}

            # Construct headers
            header_parameters = {}
            header_parameters['Content-Type'] = 'application/json; charset=utf-8'
            if self.config.generate_client_request_id:
                header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
            if custom_headers:
                header_parameters.update(custom_headers)
            if self.config.accept_language is not None:
                header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

            # Construct and send request
            request = self._client.get(url, query_parameters)
            response = self._client.send(
                request, header_parameters, stream=False, **operation_config)

            if response.status_code not in [200]:
                exp = CloudError(response)
                exp.request_id = response.headers.get('x-ms-request-id')
                raise exp

            return response

        # Deserialize response
        deserialized = models.PoolPaged(internal_paging, self._deserialize.dependencies)

        if raw:
            header_dict = {}
            client_raw_response = models.PoolPaged(internal_paging, self._deserialize.dependencies, header_dict)
            return client_raw_response

        return deserialized
    list_by_batch_account.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/pools'}


    def _create_initial(
            self, resource_group_name, account_name, pool_name, parameters, if_match=None, if_none_match=None, custom_headers=None, raw=False, **operation_config):
        # Construct URL
        url = self.create.metadata['url']
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'accountName': self._serialize.url("account_name", account_name, 'str', max_length=24, min_length=3, pattern=r'^[-\w\._]+$'),
            'poolName': self._serialize.url("pool_name", pool_name, 'str', max_length=64, min_length=1, pattern=r'^[a-zA-Z0-9_-]+$'),
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if if_match is not None:
            header_parameters['If-Match'] = self._serialize.header("if_match", if_match, 'str')
        if if_none_match is not None:
            header_parameters['If-None-Match'] = self._serialize.header("if_none_match", if_none_match, 'str')
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct body
        body_content = self._serialize.body(parameters, 'Pool')

        # Construct and send request
        request = self._client.put(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            exp = CloudError(response)
            exp.request_id = response.headers.get('x-ms-request-id')
            raise exp

        deserialized = None
        header_dict = {}

        if response.status_code == 200:
            deserialized = self._deserialize('Pool', response)
            header_dict = {
                'ETag': 'str',
            }

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            try:
                client_raw_response.add_headers(header_dict)
            except DeserializationError:
                pass # Deserialization of Headers here can fail
            return client_raw_response

        return deserialized

    def create(
            self, resource_group_name, account_name, pool_name, parameters, if_match=None, if_none_match=None, custom_headers=None, raw=False, **operation_config):
        """Creates a new pool inside the specified account.

        :param resource_group_name: The name of the resource group that
         contains the Batch account.
        :type resource_group_name: str
        :param account_name: The name of the Batch account.
        :type account_name: str
        :param pool_name: The pool name. This must be unique within the
         account.
        :type pool_name: str
        :param parameters: Additional parameters for pool creation.
        :type parameters: ~azure.mgmt.batch.models.Pool
        :param if_match: The entity state (ETag) version of the pool to
         update. A value of "*" can be used to apply the operation only if the
         pool already exists. If omitted, this operation will always be
         applied.
        :type if_match: str
        :param if_none_match: Set to '*' to allow a new pool to be created,
         but to prevent updating an existing pool. Other values will be
         ignored.
        :type if_none_match: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :return: An instance of AzureOperationPoller that returns Pool or
         ClientRawResponse if raw=true
        :rtype:
         ~msrestazure.azure_operation.AzureOperationPoller[~azure.mgmt.batch.models.Pool]
         or ~msrest.pipeline.ClientRawResponse
        :raises: :class:`CloudError<msrestazure.azure_exceptions.CloudError>`
        """
        raw_result = self._create_initial(
            resource_group_name=resource_group_name,
            account_name=account_name,
            pool_name=pool_name,
            parameters=parameters,
            if_match=if_match,
            if_none_match=if_none_match,
            custom_headers=custom_headers,
            raw=True,
            **operation_config
        )
        if raw:
            return raw_result

        # Construct and send request
        def long_running_send():
            return raw_result.response

        def get_long_running_status(status_link, headers=None):

            request = self._client.get(status_link)
            if headers:
                request.headers.update(headers)
            header_parameters = {}
            header_parameters['x-ms-client-request-id'] = raw_result.response.request.headers['x-ms-client-request-id']
            return self._client.send(
                request, header_parameters, stream=False, **operation_config)

        def get_long_running_output(response):

            if response.status_code not in [200]:
                exp = CloudError(response)
                exp.request_id = response.headers.get('x-ms-request-id')
                raise exp

            header_dict = {
                'ETag': 'str',
            }
            deserialized = self._deserialize('Pool', response)

            if raw:
                client_raw_response = ClientRawResponse(deserialized, response)
                client_raw_response.add_headers(header_dict)
                return client_raw_response

            return deserialized

        long_running_operation_timeout = operation_config.get(
            'long_running_operation_timeout',
            self.config.long_running_operation_timeout)
        return AzureOperationPoller(
            long_running_send, get_long_running_output,
            get_long_running_status, long_running_operation_timeout)
    create.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/pools/{poolName}'}

    def update(
            self, resource_group_name, account_name, pool_name, parameters, if_match=None, custom_headers=None, raw=False, **operation_config):
        """Updates the properties of an existing pool.

        :param resource_group_name: The name of the resource group that
         contains the Batch account.
        :type resource_group_name: str
        :param account_name: The name of the Batch account.
        :type account_name: str
        :param pool_name: The pool name. This must be unique within the
         account.
        :type pool_name: str
        :param parameters: Pool properties that should be updated. Properties
         that are supplied will be updated, any property not supplied will be
         unchanged.
        :type parameters: ~azure.mgmt.batch.models.Pool
        :param if_match: The entity state (ETag) version of the pool to
         update. This value can be omitted or set to "*" to apply the operation
         unconditionally.
        :type if_match: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: Pool or ClientRawResponse if raw=true
        :rtype: ~azure.mgmt.batch.models.Pool or
         ~msrest.pipeline.ClientRawResponse
        :raises: :class:`CloudError<msrestazure.azure_exceptions.CloudError>`
        """
        # Construct URL
        url = self.update.metadata['url']
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'accountName': self._serialize.url("account_name", account_name, 'str', max_length=24, min_length=3, pattern=r'^[-\w\._]+$'),
            'poolName': self._serialize.url("pool_name", pool_name, 'str', max_length=64, min_length=1, pattern=r'^[a-zA-Z0-9_-]+$'),
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if if_match is not None:
            header_parameters['If-Match'] = self._serialize.header("if_match", if_match, 'str')
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct body
        body_content = self._serialize.body(parameters, 'Pool')

        # Construct and send request
        request = self._client.patch(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            exp = CloudError(response)
            exp.request_id = response.headers.get('x-ms-request-id')
            raise exp

        deserialized = None
        header_dict = {}

        if response.status_code == 200:
            deserialized = self._deserialize('Pool', response)
            header_dict = {
                'ETag': 'str',
            }

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            client_raw_response.add_headers(header_dict)
            return client_raw_response

        return deserialized
    update.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/pools/{poolName}'}


    def _delete_initial(
            self, resource_group_name, account_name, pool_name, custom_headers=None, raw=False, **operation_config):
        # Construct URL
        url = self.delete.metadata['url']
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'accountName': self._serialize.url("account_name", account_name, 'str', max_length=24, min_length=3, pattern=r'^[-\w\._]+$'),
            'poolName': self._serialize.url("pool_name", pool_name, 'str', max_length=64, min_length=1, pattern=r'^[a-zA-Z0-9_-]+$'),
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct and send request
        request = self._client.delete(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200, 202, 204]:
            exp = CloudError(response)
            exp.request_id = response.headers.get('x-ms-request-id')
            raise exp

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            header_dict = {
                'Location': 'str',
                'Retry-After': 'int',
            }
            client_raw_response.add_headers(header_dict)
            return client_raw_response

    def delete(
            self, resource_group_name, account_name, pool_name, custom_headers=None, raw=False, **operation_config):
        """Deletes the specified pool.

        :param resource_group_name: The name of the resource group that
         contains the Batch account.
        :type resource_group_name: str
        :param account_name: The name of the Batch account.
        :type account_name: str
        :param pool_name: The pool name. This must be unique within the
         account.
        :type pool_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :return: An instance of AzureOperationPoller that returns None or
         ClientRawResponse if raw=true
        :rtype: ~msrestazure.azure_operation.AzureOperationPoller[None] or
         ~msrest.pipeline.ClientRawResponse
        :raises: :class:`CloudError<msrestazure.azure_exceptions.CloudError>`
        """
        raw_result = self._delete_initial(
            resource_group_name=resource_group_name,
            account_name=account_name,
            pool_name=pool_name,
            custom_headers=custom_headers,
            raw=True,
            **operation_config
        )
        if raw:
            return raw_result

        # Construct and send request
        def long_running_send():
            return raw_result.response

        def get_long_running_status(status_link, headers=None):

            request = self._client.get(status_link)
            if headers:
                request.headers.update(headers)
            header_parameters = {}
            header_parameters['x-ms-client-request-id'] = raw_result.response.request.headers['x-ms-client-request-id']
            return self._client.send(
                request, header_parameters, stream=False, **operation_config)

        def get_long_running_output(response):

            if response.status_code not in [200, 202, 204]:
                exp = CloudError(response)
                exp.request_id = response.headers.get('x-ms-request-id')
                raise exp

            if raw:
                client_raw_response = ClientRawResponse(None, response)
                client_raw_response.add_headers({
                    'Location': 'str',
                    'Retry-After': 'int',
                })
                return client_raw_response

        long_running_operation_timeout = operation_config.get(
            'long_running_operation_timeout',
            self.config.long_running_operation_timeout)
        return AzureOperationPoller(
            long_running_send, get_long_running_output,
            get_long_running_status, long_running_operation_timeout)
    delete.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/pools/{poolName}'}

    def get(
            self, resource_group_name, account_name, pool_name, custom_headers=None, raw=False, **operation_config):
        """Gets information about the specified pool.

        :param resource_group_name: The name of the resource group that
         contains the Batch account.
        :type resource_group_name: str
        :param account_name: The name of the Batch account.
        :type account_name: str
        :param pool_name: The pool name. This must be unique within the
         account.
        :type pool_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: Pool or ClientRawResponse if raw=true
        :rtype: ~azure.mgmt.batch.models.Pool or
         ~msrest.pipeline.ClientRawResponse
        :raises: :class:`CloudError<msrestazure.azure_exceptions.CloudError>`
        """
        # Construct URL
        url = self.get.metadata['url']
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'accountName': self._serialize.url("account_name", account_name, 'str', max_length=24, min_length=3, pattern=r'^[-\w\._]+$'),
            'poolName': self._serialize.url("pool_name", pool_name, 'str', max_length=64, min_length=1, pattern=r'^[a-zA-Z0-9_-]+$'),
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct and send request
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            exp = CloudError(response)
            exp.request_id = response.headers.get('x-ms-request-id')
            raise exp

        deserialized = None
        header_dict = {}

        if response.status_code == 200:
            deserialized = self._deserialize('Pool', response)
            header_dict = {
                'ETag': 'str',
            }

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            client_raw_response.add_headers(header_dict)
            return client_raw_response

        return deserialized
    get.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/pools/{poolName}'}

    def disable_auto_scale(
            self, resource_group_name, account_name, pool_name, custom_headers=None, raw=False, **operation_config):
        """Disables automatic scaling for a pool.

        :param resource_group_name: The name of the resource group that
         contains the Batch account.
        :type resource_group_name: str
        :param account_name: The name of the Batch account.
        :type account_name: str
        :param pool_name: The pool name. This must be unique within the
         account.
        :type pool_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: Pool or ClientRawResponse if raw=true
        :rtype: ~azure.mgmt.batch.models.Pool or
         ~msrest.pipeline.ClientRawResponse
        :raises: :class:`CloudError<msrestazure.azure_exceptions.CloudError>`
        """
        # Construct URL
        url = self.disable_auto_scale.metadata['url']
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'accountName': self._serialize.url("account_name", account_name, 'str', max_length=24, min_length=3, pattern=r'^[-\w\._]+$'),
            'poolName': self._serialize.url("pool_name", pool_name, 'str', max_length=64, min_length=1, pattern=r'^[a-zA-Z0-9_-]+$'),
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            exp = CloudError(response)
            exp.request_id = response.headers.get('x-ms-request-id')
            raise exp

        deserialized = None
        header_dict = {}

        if response.status_code == 200:
            deserialized = self._deserialize('Pool', response)
            header_dict = {
                'ETag': 'str',
            }

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            client_raw_response.add_headers(header_dict)
            return client_raw_response

        return deserialized
    disable_auto_scale.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/pools/{poolName}/disableAutoScale'}

    def stop_resize(
            self, resource_group_name, account_name, pool_name, custom_headers=None, raw=False, **operation_config):
        """Stops an ongoing resize operation on the pool.

        This does not restore the pool to its previous state before the resize
        operation: it only stops any further changes being made, and the pool
        maintains its current state. After stopping, the pool stabilizes at the
        number of nodes it was at when the stop operation was done. During the
        stop operation, the pool allocation state changes first to stopping and
        then to steady. A resize operation need not be an explicit resize pool
        request; this API can also be used to halt the initial sizing of the
        pool when it is created.

        :param resource_group_name: The name of the resource group that
         contains the Batch account.
        :type resource_group_name: str
        :param account_name: The name of the Batch account.
        :type account_name: str
        :param pool_name: The pool name. This must be unique within the
         account.
        :type pool_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: Pool or ClientRawResponse if raw=true
        :rtype: ~azure.mgmt.batch.models.Pool or
         ~msrest.pipeline.ClientRawResponse
        :raises: :class:`CloudError<msrestazure.azure_exceptions.CloudError>`
        """
        # Construct URL
        url = self.stop_resize.metadata['url']
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'accountName': self._serialize.url("account_name", account_name, 'str', max_length=24, min_length=3, pattern=r'^[-\w\._]+$'),
            'poolName': self._serialize.url("pool_name", pool_name, 'str', max_length=64, min_length=1, pattern=r'^[a-zA-Z0-9_-]+$'),
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            exp = CloudError(response)
            exp.request_id = response.headers.get('x-ms-request-id')
            raise exp

        deserialized = None
        header_dict = {}

        if response.status_code == 200:
            deserialized = self._deserialize('Pool', response)
            header_dict = {
                'ETag': 'str',
            }

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            client_raw_response.add_headers(header_dict)
            return client_raw_response

        return deserialized
    stop_resize.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/pools/{poolName}/stopResize'}