# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from typing import Any, Dict, Mapping, Optional
from datetime import datetime
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError

from ._internal import _KeyVaultClientBase
from ._models import (
    Certificate,
    CertificateBase,
    CertificatePolicy,
    DeletedCertificate,
    Issuer,
    IssuerBase,
    Contact,
    CertificateOperation,
)


class CertificateClient(_KeyVaultClientBase):
    """CertificateClient defines a high level interface for
    managing certificates in the specified vault.
    Example:
        .. literalinclude:: ../tests/test_examples_certificates.py
            :start-after: [START create_certificate_client]
            :end-before: [END create_certificate_client]
            :language: python
            :dedent: 4
            :caption: Creates a new instance of the Certificate client
    """
    # pylint:disable=protected-access

    def create_certificate(self, name, policy, enabled=None, not_before=None, expires=None, tags=None, **kwargs):
        # type: (str, CertificatePolicy, Optional[bool], Optional[datetime], Optional[datetime], Optional[Dict[str, str]], Mapping[str, Mapping[str, Any]]) -> CertificateOperation
        """Creates a new certificate.

        If this is the first version, the certificate resource is created. This
        operation requires the certificates/create permission.

        :param name: The name of the certificate.
        :type name: str
        :param policy: The management policy for the certificate.
        :type policy:
         ~azure.security.keyvault.v7_0.models.CertificatePolicy
        :param enabled: Determines whether the object is enabled.
        :type enabled: bool
        :param not_before: Not before date of the secret in UTC
        :type not_before: datetime.datetime
        :param expires: Expiry date of the secret  in UTC.
        :type expires: datetime.datetime
        :param tags: Application specific metadata in the form of key-value pairs.
        :type tags: dict(str, str)
        :returns: The created CertificateOperation
        :rtype: ~azure.security.keyvault.certificates._models.CertificateOperation
        """

        if enabled is not None or not_before is not None or expires is not None:
            attributes = self._client.models.CertificateAttributes(
                enabled=enabled, not_before=not_before, expires=expires
            )
        else:
            attributes = None

        bundle = self._client.create_certificate(
            vault_base_url=self.vault_url,
            certificate_name=name,
            certificate_policy=policy,
            certificate_attributes=attributes,
            tags=tags,
            **kwargs
        )

        return CertificateOperation._from_certificate_operation_bundle(certificate_operation_bundle=bundle)

    def get_certificate(self, name, version=None, **kwargs):
        # type: (str, Optional[str]) -> Certificate
        """Gets information about a certificate.

        Gets information about a specific certificate. This operation requires
        the certificates/get permission.

        :param name: The name of the certificate in the given
         vault.
        :type name: str
        :param version: The version of the certificate.
        :type version: str
        :returns: An instance of Certificate
        :rtype: ~azure.security.keyvault.certificates._models.Certificate
        """
        if version is None:
            version = ""

        bundle = self._client.get_certificate(
            vault_base_url=self.vault_url,
            certificate_name=name,
            certificate_version=version,
            **kwargs
        )
        return Certificate._from_certificate_bundle(certificate_bundle=bundle)

    def delete_certificate(self, name, **kwargs):
        # type: (str) -> DeletedCertificate
        """Deletes a certificate from the key vault.

        Deletes all versions of a certificate object along with its associated
        policy. Delete certificate cannot be used to remove individual versions
        of a certificate object. This operation requires the
        certificates/delete permission.

        :param name: The name of the certificate.
        :type name: str
        :returns: The deleted certificate
        :rtype: ~azure.security.keyvault.certificates._models.DeletedCertificate
        """
        bundle = self._client.delete_certificate(vault_base_url=self.vault_url, certificate_name=name, **kwargs)
        return DeletedCertificate._from_deleted_certificate_bundle(deleted_certificate_bundle=bundle)

    def get_deleted_certificate(self, name, **kwargs):
        # type: (str) -> DeletedCertificate
        """Retrieves information about the specified deleted certificate.

        Retrieves the deleted certificate information plus its attributes,
        such as retention interval, scheduled permanent deletion, and the
        current deletion recovery level. This operaiton requires the certificates/
        get permission.

        :param name: The name of the certificate.
        :type name: str
        :return: The deleted certificate
        :rtype: ~azure.security.keyvault.certificates._models.DeletedCertificate
        """
        bundle = self._client.get_deleted_certificate(
            vault_base_url=self.vault_url,
            certificate_nae=name,
            error_map={404: ResourceNotFoundError},
            **kwargs
        )
        return DeletedCertificate._from_deleted_certificate_bundle(deleted_certificate_bundle=bundle)

    def purge_deleted_certificate(self, name, **kwargs):
        # type: (str) -> None
        """Permanently deletes the specified deleted certificate.

        Performs an irreversible deletion of the specified certificate, without
        possibility for recovery. The operation is not available if the recovery
        level does not specified 'Purgeable'. This operation requires the
        certificate/purge permission.

        :param name: The name of the certificate
        :type name: str
        :return: None
        :rtype: None
        """
        self._client.purge_deleted_certificate(vault_base_url=self.vault_url, certificate_name=name, **kwargs)

    def recover_deleted_certificate(self, name, **kwargs):
        # type: (str, Mapping[str, Any]) -> Certificate
        """Recovers the deleted certificate back to its current version under
        /certificates.

        Performs hte reversal of the Delete operation. THe operation is applicable
        in vaults enabled for soft-delete, and must be issued during the retention
        interval (available in the deleted certificate's attributes). This operation
        requires the certificates/recover permission.

        :param name: The name of the deleted certificate
        :type name: str
        :return: The recovered certificate
        :rtype ~azure.security.keyvault.certificates._models.Certificate
        """
        bundle = self._client.recover_deleted_certificate(vault_base_url=self.vault_url, certificate_name=name, **kwargs)
        return Certificate._from_certificate_bundle(certificate_bundle=bundle)

    def import_certificate(
        self,
        name,
        base64_encoded_certificate,
        policy,
        password=None,
        enabled=None,
        not_before=None,
        expires=None,
        tags=None,
        **kwargs
    ):
        # type: (str, str, CertificatePolicy, Optional[str], Optional[bool],Optional[datetime], Optional[datetime], Optional[Dict[str, str]], Mapping[str, Any]) -> Certificate
        """Imports a certificate into the key vault.

        Imports an existing valid certificate, containing a private key, into
        Azure Key Vault. The certificate to be imported can be in either PFX or
        PEM format. If the certificate is in PEM format the PEM file must
        contain the key as well as x509 certificates. This operation requires
        the certificates/import permission.

        :param name: The name of the certificate.
        :type name: str
        :param base64_encoded_certificate: Base64 encoded representation of
         the certificate object to import. This certificate needs to contain
         the private key.
        :type base64_encoded_certificate: str
        :param policy: The management policy for the certificate.
        :type policy:
         ~azure.security.keyvault.v7_0.models.CertificatePolicy
        :param password: Password that protecting the certificate to import.
        :type password: str
        :param enabled: Determines whether the object is enabled.
        :type enabled: bool
        :param not_before: Not before date of the secret in UTC
        :type not_before: datetime.datetime
        :param expires: Expiry date of the secret  in UTC.
        :type expires: datetime.datetime
        :param tags: Application specific metadata in the form of key-value
         pairs.
        :type tags: dict[str, str]
        :returns: The imported Certificate
        :rtype: ~azure.security.keyvault.certificates._models.Certificate
        """
        if enabled is not None or not_before is not None or expires is not None:
            attributes = self._client.models.CertificateAttributes(
                enabled=enabled, not_before=not_before, expires=expires
            )
        else:
            attributes = None
        bundle = self._client.import_certificate(
            vault_base_url=self.vault_url,
            certificate_name=name,
            base64_encoded_certificate=base64_encoded_certificate,
            password=password,
            certificate_policy=policy,
            certificate_attributes=attributes,
            tags=tags,
            **kwargs
        )
        return Certificate._from_certificate_bundle(certificate_bundle=bundle)

    def get_policy(self, name, **kwargs):
        # type: (str) -> CertificatePolicy
        """Gets the policy for a certificate.

        Returns the specified certificate policy resources in the key
        vault. This operation requires the certificates/get permission.

        :param name: The name of the certificate in a given key vault.
        :type name: str
        :return: The certificate policy
        :rtype ~azure.security.keyvault.certificates._models.CertificatePolicy
        """
        bundle = self._client.get_certificate_policy(vault_base_url=self.vault_url, certificate_name=name, **kwargs)
        return CertificatePolicy._from_certificate_policy_bundle(certificate_policy_bundle=bundle)


    def update_policy(self, name, policy, **kwargs):
        # type: (str, CertificatePolicy) -> CertificatePolicy
        """Updates the policy for a certificate.

        Set specified members in the certificate policy. Leaves others as null.
        This operation requries the certificates/update permission.

        :param name: The name of the certificate in the given vault.
        :type name: str
        :param policy: The policy for the certificate.
        :type policy: ~azure.security.keyvault.certificates._models.CertificatePolicy
        :return: The certificate policy
        :rtype: ~azure.security.keyvault.certificates._models.CertificatePolicy
        """
        bundle = self._client.update_certificate_policy(
            vault_base_url=self.vault_url,
            certificate_name=name,
            certificate_policy=policy,
            **kwargs
        )
        return CertificatePolicy._from_certificate_policy_bundle(certificate_policy_bundle=bundle)


    def update_certificate(self, name, version=None, not_before=None, expires=None, enabled=None, tags=None, **kwargs):
        # type: (str, str, Optional[bool], Optional[Dict[str, str]]) -> Certificate
        """Updates the specified attributes associated with the given certificate.

        The UpdateCertificate operation applies the specified update on the
        given certificate; the only elements updated are the certificate's
        attributes. This operation requires the certificates/update permission.

        :param name: The name of the certificate in the given key
         vault.
        :type name: str
        :param version: The version of the certificate.
        :type version: str
        :param not_before: Not before date of the secret in UTC
        :type not_before: datetime.datetime
        :param expires: Expiry date of the secret  in UTC.
        :type expires: datetime.datetime
        :param enabled: Determines whether the object is enabled.
        :type enabled: bool
        :param tags: Application specific metadata in the form of key-value pairs.
        :type tags: dict(str, str)
        :returns: The updated Certificate
        :rtype: ~azure.security.keyvault.certificates._models.Certificate
        """
        if enabled is not None or not_before is not None or expires is not None:
            attributes = self._client.models.CertificateAttributes(
                enabled=enabled, not_before=not_before, expires=expires
            )
        else:
            attributes = None

        bundle = self._client.update_certificate(
            vault_base_url=self.vault_url,
            certificate_name=name,
            certificate_version=version or "",
            certificate_attributes=attributes,
            tags=tags,
            **kwargs
        )
        return Certificate._from_certificate_bundle(certificate_bundle=bundle)

    def backup_certificate(self, name, **kwargs):
        # type: (str) -> bytes
        """Backs up the specified certificate.

        Requests that a backup of the specified certificate be downloaded
        to the client. All versions of the certificate will be downloaded.
        This operation requires the certificates/backup permission.

        :param name: The name of the certificate.
        :type name: str
        :return: the backup blob containing the backed up certificate.
        :rtype: bytes
        """
        backup_result = self._client.backup_certificate(
            vault_base_url=self.vault_url,
            certificate_name=name,
            error_map={404: ResourceNotFoundError},
            **kwargs
        )
        return backup_result.value


    def restore_certificate(self, backup, **kwargs):
        # type: (bytes) -> Certificate
        """Restores a backed up certificate to a vault.

        Restores a backed up certificate, and all its versions, to a vault.
        this operation requires the certificates/restore permission.

        :param backup: The backup blob associated with a certificate bundle.
        :type backup bytes
        :return: The restored Certificate
        :rtype: ~azure.security.keyvault.certificates._models.Certificate
        """
        bundle = self._client.restore_certificate(
            vault_base_url=self.vault_url,
            certificate_bundle_backup=backup,
            error_map={409: ResourceExistsError},
            **kwargs
        )
        return Certificate._from_certificate_bundle(certificate_bundle=bundle)

    def list_deleted_certificates(self, include_pending=None, **kwargs):
        # type: (Optional[bool]) -> Generator[DeletedCertificate]
        """Lists the deleted certificates in the specified vault currently
        available for recovery.

        Retrieves the certificates in the current vault which are in a deleted
        state and ready for recovery or purging. This operation includes
        deletion-specific information. This operation requires the certificates/get/list
        permission. This operation can only be enabled on soft-delete enabled vaults.

        :param include_pending: Specifies whether to include certificates which are not
        completely provisioned.
        :type include_pending bool
        :return: An iterator like instance of DeletedCertificate
        :rtype:
         typing.Generator[~azure.security.keyvault.certificates._models.DeletedCertificate]
        """
        max_page_size = kwargs.get("max_page_size", None)
        pages = self._client.get_deleted_certificates(
            vault_base_url=self._vault_url,
            maxresults=max_page_size,
            include_pending=include_pending,
            **kwargs
        )
        return (DeletedCertificate._from_deleted_certificate_item(deleted_certificate_item=item) for item in pages)

    def list_certificates(self, include_pending=None, **kwargs):
        # type: (Optional[bool]) -> Generator[CertificateBase]
        """List certificates in the key vault.

        The GetCertificates operation returns the set of certificates resources
        in the key vault. This operation requires the
        certificates/list permission.

        :param include_pending: Specifies whether to include certificates
         which are not completely provisioned.
        :type include_pending: bool
        :returns: An iterator like instance of CertificateBase
        :rtype:
         typing.Generator[~azure.security.keyvault.certificates._models.CertificateBase]
        """
        max_page_size = kwargs.get("max_page_size", None)
        pages = self._client.get_certificates(
            vault_base_url=self._vault_url,
            maxresults=max_page_size,
            include_pending=include_pending,
            **kwargs
        )
        return (CertificateBase._from_certificate_item(certificate_item=item) for item in pages)

    def list_certificate_versions(self, name, **kwargs):
        # type: (str) -> Generator[CertificateBase]
        """List the versions of a certificate.

        The GetCertificateVersions operation returns the versions of a
        certificate in the key vault. This operation requires the
        certificates/list permission.

        :param name: The name of the certificate.
        :type name: str
        :returns: An iterator like instance of CertificateBase
        :rtype:
         typing.Generator[~azure.security.keyvault.certificates._models.CertificateBase]
        """
        max_page_size = kwargs.get("max_page_size", None)
        pages = self._client.get_certificate_versions(
            vault_base_url=self._vault_url,
            certificate_name=name,
            maxresults=max_page_size,
            **kwargs)
        return (CertificateBase._from_certificate_item(certificate_item=item) for item in pages)

    def create_contacts(self, contacts, **kwargs):
        # type: (Iterable[Contact]) -> Iterable[Contact]
        """Sets the certificate contacts for the key vault.

        Sets the certificate contacts for the key vault. This
        operation requires the certificates/managecontacts permission.

        :param contacts: The contact list for the vault certificates.
        :type contacts: list[~azure.keyvault.v7_0.models.Contact]
        :returns: The created list of contacts
        :rtype: list[~azure.security.keyvault.certificates._models.Contacts]
        """
        bundle = self._client.set_certificate_contacts(vault_base_url=self.vault_url, contact_list=contacts, **kwargs)
        return (Contact._from_certificate_contacts_item(contact_item=item) for item in bundle.contact_list)

    def list_contacts(self, **kwargs):
        # type: () -> Iterable[Contact]
        """Lists the certificate contacts for the key vault.

        Returns the set of certificate contact resources in the specified
        key vault. This operation requires the certificates/managecontacts
        permission.

        :return: The certificate contacts for the key vault.
        :rtype: ~azure.security.keyvault.certificates._models.Contacts
        """
        pages = self._client.get_certificate_contacts(vault_base_url=self._vault_url, **kwargs)
        return (Contact._from_certificate_contacts_item(contact_item=item) for item in pages.contact_list)

    def delete_contacts(self, **kwargs):
        # type: () -> Iterable[Contact]
        """Deletes the certificate contacts for the key vault.

        Deletes the certificate contacts for the key vault certificate.
        This operation requires the certificates/managecontacts permission.

        :return: Contacts
        :rtype: ~azure.security.certificates._models.Contacts
        """
        bundle = self._client.delete_certificate_contacts(vault_base_url=self.vault_url, **kwargs)
        return (Contact._from_certificate_contacts_item(contact_item=item) for item in bundle.contact_list)

    def get_certificate_operation(self, name, **kwargs):
        # type: (str) -> CertificateOperation
        """Gets the creation operation of a certificate.

        Gets the creation operation associated with a specified certificate.
        This operation requires the certificates/get permission.

        :param name: The name of the certificate.
        :type name: str
        :returns: The created CertificateOperation
        :rtype: ~azure.security.keyvault.v7_0.models.CertificateOperation
        """

        bundle = self._client.get_certificate_operation(vault_base_url=self.vault_url, certificate_name=name, **kwargs)
        return CertificateOperation._from_certificate_operation_bundle(certificate_operation_bundle=bundle)

    def delete_certificate_operation(self, name, **kwargs):
        # type: (str) -> CertificateOperation
        """Deletes the creation operation for a specific certificate.

        Deletes the creation operation for a specified certificate that is in
        the process of being created. The certificate is no longer created.
        This operation requires the certificates/update permission.

        :param name: The name of the certificate.
        :type name: str
        :return: The deleted CertificateOperation
        :rtype: ~azure.security.keyvault.certificates._models.CertificateOperation
        """
        bundle = self._client.delete_certificate_operation(vault_base_url=self.vault_url, certificate_name=name, **kwargs)
        return CertificateOperation._from_certificate_operation_bundle(certificate_operation_bundle=bundle)

    def cancel_certificate_operation(self, name, **kwargs):
        # type: (str) -> CertificateOperation
        """Updates a certificate operation.

        Updates a certificate creation operation that is already in progress.
        This operation requires the certificates/update permission.

        :param name: The name of the certificate.
        :type name: str
        :param cancellation_requested: Indicates if cancellation was requested
         on the certificate operation.
        :type cancellation_requested: bool
        :returns: The updated certificate operation
        :rtype: ~azure.security.keyvault.certificates._models.CertificateOperation
        """
        bundle = self._client.update_certificate_operation(
            vault_base_url=self.vault_url,
            certificate_name=name,
            cancellation_requested=True,
            **kwargs
        )
        return CertificateOperation._from_certificate_operation_bundle(certificate_operation_bundle=bundle)

    def merge_certificate(
        self, name, x509_certificates, enabled=True, not_before=None, expires=None, tags=None, **kwargs):
        # type: (str, list[bytearray], Optional[bool], Optional[datetime], Optional[datetime]Optional[Dict[str, str]]) -> Certificate
        """Merges a certificate or a certificate chain with a key pair existing on the server.

        Performs the merging of a certificate or certificate chain with a key pair currently
        available in the service. This operation requires the certificates/create permission.

        :param name: The name of the certificate
        :type name: str
        :param x509_certificates: The certificate or the certificate chain to merge.
        :type x509_certificates: list[bytearray]
        :param enabled: Determines whether the object is enabled.
        :type enabled: bool
        :param not_before: Not before date of the secret in UTC
        :type not_before: datetime.datetime
        :param expires: Expiry date of the secret  in UTC.
        :type expires: datetime.datetime
        :param tags: Application specific metadata in the form of key-value pairs.
        :type tags: dict[str, str]
        :return: The merged certificate operation
        :rtype: ~azure.security.keyvault.certificates._models.CertificateOperation
        """
        if enabled is not None or not_before is not None or expires is not None:
            attributes = self._client.models.CertificateAttributes(
                enabled=enabled, not_before=not_before, expires=expires
            )
        else:
            attributes = None
        bundle = self._client.merge_certificate(
            vault_base_url=self.vault_url,
            certificate_name=name,
            x509_certificates=x509_certificates,
            certificate_attributes=attributes,
            tags=tags,
            **kwargs
        )
        return CertificateOperation._from_certificate_operation_bundle(certificate_operation_bundle=bundle)


    def get_pending_certificate_signing_request(self, name, **kwargs):
        # type: (str) -> CertificateOperation
        """Gets the pending certificate signing request.

        Gets the pending certificate signing request for the specified certificate.
        This operation requires the certificates/get permission.

        :param name: The name of the certificate
        :type name: str
        :return: Certificate operation detailing the certificate signing request.
        :rtype: ~azure.security.keyvault.v7_0.models.CertificateOperation
        """
        bundle = self._client.get_certificate_operation(vault_base_url=self.vault_url, certificate_name=name, **kwargs)
        return CertificateOperation._from_certificate_operation_bundle(certificate_operation_bundle=bundle)

    def get_issuer(self, name, **kwargs):
        # type: (str) -> Issuer
        """Gets the specified certificate issuer.

        Returns the specified certificate issuer resources in the key vault.
        This operation requires the certificates/manageissuers/getissuers permission.

        :param name: The name of the issuer.
        :type name: str
        :return: The specified certificate issuer.
        :rtype: ~azure.security.keyvault.certificates._models.Issuer
        """
        issuer_bundle = self._client.get_certificate_issuer(vault_base_url=self.vault_url, issuer_name=name, **kwargs)
        return Issuer._from_issuer_bundle(issuer_bundle=issuer_bundle)

    def create_issuer(
        self,
        name,
        provider,
        account_id=None,
        password=None,
        organization_id=None,
        admin_details=[None],
        enabled=None,
        **kwargs
    ):
        # type: (str, str, Optional[str], Optional[str], Optional[str], Optional[List[AdministratorDetails]], Optional[bool], Mapping[str, Any]) -> Issuer
        """Sets the specified certificate issuer.

        The SetCertificateIssuer operation adds or updates the specified
        certificate issuer. This operation requires the certificates/setissuers
        permission.

        :param name: The name of the issuer.
        :type name: str
        :param provider: The issuer provider.
        :type provider: str
        :param account_id: The user name/account name/account id.
        :type account_id: str
        :param password: The password/secret/account key.
        :type password: str
        :param organization_id: Id of the organization.
        :type organization_id: str
        :param admin_details:
        :param enabled: Determines whether the object is enabled.
        :type enabled: bool
        :returns: The created Issuer
        :rtype: ~azure.security.keyvault.certificates._models.Issuer
        """
        if account_id or password:
            issuer_credentials = self._client.models.IssuerCredentials(account_id=account_id, password=password)
        else:
            issuer_credentials = None
        if admin_details[0]:
            admin_details_to_pass = []
            for admin_detail in admin_details:
                admin_details_to_pass.append(
                    self._client.models.AdministratorDetails(
                        first_name=admin_detail.first_name,
                        last_name=admin_detail.last_name,
                        email_address=admin_detail.email,
                        phone=admin_detail.phone
                    )
                )
        else:
            admin_details_to_pass = admin_details
        if organization_id or admin_details:
            organization_details = self._client.models.OrganizationDetails(id=organization_id, admin_details=admin_details_to_pass)
        else:
            organization_details = None
        if enabled is not None:
            issuer_attributes = self._client.models.IssuerAttributes(enabled=enabled)
        else:
            issuer_attributes = None
        issuer_bundle = self._client.set_certificate_issuer(
            vault_base_url=self.vault_url,
            issuer_name=name,
            provider=provider,
            credentials=issuer_credentials,
            organization_details=organization_details,
            attributes=issuer_attributes,
            **kwargs
        )
        return Issuer._from_issuer_bundle(issuer_bundle=issuer_bundle)

    def update_issuer(
        self,
        name,
        provider=None,
        account_id=None,
        password=None,
        organization_id=None,
        admin_details=[None],
        enabled=True,
        **kwargs
    ):
        # type: (str, Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[List[AdministratorDetails]], Optional[bool], Mapping[str, Any]) -> Issuer
        """Updates the specified certificate issuer.

        Performs an update on the specified certificate issuer entity.
        THis operation requires the certificates/setissuers permission.

        :param name: The name of the issuer.
        :type name: str
        :param provider: The issuer provider.
        :type provider: str
        :param account_id: The username / account name / account key.
        :type account_id: str
        :param password: The password / secret / account key.
        :type password: str
        :param organization_id: Id of the organization
        :type organization_id: str
        :param first_name: First name of the certificate issuer.
        :type first_name: str
        :param last_name: Last name of the certificate issuer.
        :type last_name: str
        :param email: Email address of the certificate issuer.
        :type email: str
        :param phone: Phone number of the certificate issuer.
        :type phone: str
        :param enabled: Determines whether the issuer is enabled.
        :type enabled: bool
        :return: The updated issuer
        :rtype: ~azure.security.keyvault.certificates._models.Issuer
        """
        if account_id or password:
            issuer_credentials = self._client.models.IssuerCredentials(account_id=account_id, password=password)
        else:
            issuer_credentials = None
        if admin_details[0]:
            admin_details_to_pass = []
            for admin_detail in admin_details:
                admin_details_to_pass.append(
                    self._client.models.AdministratorDetails(
                        first_name=admin_detail.first_name,
                        last_name=admin_detail.last_name,
                        email_address=admin_detail.email,
                        phone=admin_detail.phone
                    )
                )
        else:
            admin_details_to_pass = admin_details
        if organization_id or admin_details:
            organization_details = self._client.models.OrganizationDetails(id=organization_id, admin_details=admin_details_to_pass)
        else:
            organization_details = None
        if enabled is not None:
            issuer_attributes = self._client.models.IssuerAttributes(enabled=enabled)
        else:
            issuer_attributes = None
        issuer_bundle = self._client.update_certificate_issuer(
            vault_base_url=self.vault_url,
            issuer_name=name,
            provider=provider,
            credentials=issuer_credentials,
            organization_details=organization_details,
            attributes=issuer_attributes,
            **kwargs
        )
        return Issuer._from_issuer_bundle(issuer_bundle=issuer_bundle)

    def delete_issuer(self, name, **kwargs):
        # type: (str) -> Issuer
        """Deletes the specified certificate issuer.

        Permanently removes the specified certificate issuer from the vault.
        This operation requires the certificates/manageissuers/deleteissuers permission.

        :param name: The name of the issuer.
        :type name: str
        :return: Issuer
        :rtype: ~azure.security.keyvault.certificates._models.Issuer
        """
        issuer_bundle = self._client.delete_certificate_issuer(vault_base_url=self.vault_url, issuer_name=name, **kwargs)
        return Issuer._from_issuer_bundle(issuer_bundle=issuer_bundle)

    def list_issuers(self, **kwargs):
        # type: () -> Iterable[IssuerBase]
        """List certificate issuers for the key vault.

        Returns the set of certificate issuer resources in the key
        vault. This operation requires the certificates/manageissuers/getissuers
        permission.

        :return: An iterator like instance of Issuers
        :rtype: Iterable[~azure.security.keyvault.certificates._models.Issuer]
        """
        max_page_size = kwargs.get("max_page_size", None)
        paged_certificate_issuer_items = self._client.get_certificate_issuers(vault_base_url=self.vault_url, maxresults=max_page_size, **kwargs)
        return (IssuerBase._from_issuer_item(issuer_item=item) for item in paged_certificate_issuer_items)