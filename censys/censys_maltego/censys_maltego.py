import ipaddress
import logging
import re
import socket

from censys.certificates import CensysCertificates
from censys.ipv4 import CensysIPv4

from maltego_trx.maltego import MaltegoTransform


class Censys:

    def __init__(self, api_id, api_secret, **kwargs):

        logging.basicConfig(filename='censys_maltego_transform.log', level=logging.DEBUG)
        self.max_pages = kwargs.get('max_pages', 1)
        self.start_page = kwargs.get('start_pages', 1)

        self.connection = {
            'ipv4': CensysIPv4(api_id=api_id, api_secret=api_secret),
            'certificates': CensysCertificates(api_id=api_id, api_secret=api_secret)
        }

        self.fields = {
            'certificate': [
                'parsed.names',
                'metadata.added_at',
                'metadata.seen_in_scan',
                'metadata.source',
                'metadata.updated_at',
                'tags',
                'parsed.fingerprint_sha1',
                'parsed.fingerprint_sha256',
                'parsed.serial_number',
                'parsed.subject.common_name',
                'parsed.validity.start',
                'parsed.validity.end',
                'parsed.issuer.organization',
                'parsed.issuer_dn',
                'parsed.extensions.basic_constraints.is_ca'
            ],
            'ipv4': [
                '443.https.heartbleed.heartbleed_vulnerable',
                '443.https.tls.certificate.parsed.extensions.basic_constraints.is_ca',
                '443.https.tls.certificate.parsed.extensions.subject_alt_name.dns_names',
                '443.https.tls.certificate.parsed.fingerprint_sha256',
                '443.https.tls.certificate.parsed.issuer.common_name',
                '443.https.tls.certificate.parsed.issuer.country',
                '443.https.tls.certificate.parsed.issuer.organization',
                '443.https.tls.certificate.parsed.issuer_dn',
                '443.https.tls.certificate.parsed.names',
                '443.https.tls.certificate.parsed.serial_number',
                '443.https.tls.certificate.parsed.signature.self_signed',
                '443.https.tls.certificate.parsed.subject.common_name',
                '443.https.tls.certificate.parsed.subject_dn',
                '443.https.tls.certificate.parsed.validity.end',
                '443.https.tls.certificate.parsed.validity.start',
                '443.https.tls.cipher_suite.name',
                '443.https.tls.signature.valid',
                '443.https.tls.validation.browser_trusted',
                '443.https.tls.version',
                'ip'
            ],
            'ports': [
                'ip',
                'ports',
                'protocols',
                'tags'
            ],
            'banners': [
                '22.ssh.v2.banner.raw',
                '143.imap.starttls.banner',
                '21.ftp.banner.banner',
                '23.telnet.banner.banner',
                '2323.telnet.banner.banner',
                '25.smtp.starttls.banner',
                '5900.vnc.banner.desktop_name',
                '5901.vnc.banner.desktop_name',
                '5902.vnc.banner.desktop_name',
                '5903.vnc.banner.desktop_name',
                '631.ipp.banner.attr_printer_uris',
                '3389.rdp.banner.metadata.description',
                '7547.cwmp.get.headers.www_authenticate'
            ],
            'domain': [
                '443.https.heartbleed.heartbleed_vulnerable',
                '443.https.tls.certificate.parsed.extensions.basic_constraints.is_ca',
                '443.https.tls.certificate.parsed.extensions.subject_alt_name.dns_names',
                '443.https.tls.certificate.parsed.fingerprint_sha256',
                '443.https.tls.certificate.parsed.issuer.common_name',
                '443.https.tls.certificate.parsed.issuer.country',
                '443.https.tls.certificate.parsed.issuer.organization',
                '443.https.tls.certificate.parsed.issuer_dn',
                '443.https.tls.certificate.parsed.names',
                '443.https.tls.certificate.parsed.serial_number',
                '443.https.tls.certificate.parsed.signature.self_signed',
                '443.https.tls.certificate.parsed.subject.common_name',
                '443.https.tls.certificate.parsed.subject_dn',
                '443.https.tls.certificate.parsed.validity.end',
                '443.https.tls.certificate.parsed.validity.start',
                '443.https.tls.cipher_suite.name',
                '443.https.tls.signature.valid',
                '443.https.tls.validation.browser_trusted',
                '443.https.tls.version',
                'ip'
            ]
        }

        if api_id and api_secret:
            self.api_id = api_id
            self.api_secret = api_secret
            self.mt = MaltegoTransform()
        else:
            self.mt.addException(
                "Please provide valid credentials as either a script parameter or environmental variable"
            )

    def _process_object_properties(self, properties):

        processed_properties = {}

        for prop in properties.split('#'):
            # This splits the string into separate values
            for values in prop:
                field_name, field_value = values.split('=')
                processed_properties[field_name] = field_value

        return processed_properties

    def _finalize(self):
        print(self.mt.returnOutput())

    def _validate_ip(self, query_parameter):

        try:
            ipaddress.ip_address(query_parameter)

            return True
        except ValueError as e:
            logging.warning("Value is not an IPv4 address. Trying type netblock.")
            logging.warning("{}".format(e))
        except Exception as e:
            return False

        try:
            ipaddress.ip_network(query_parameter, strict=True)
            return True
        except ValueError as e:
            logging.warning('Value is not an IPv4 network.')
            logging.warning("{}".format(e))
        except Exception as e:
            return False

        return False

    def _dns_to_ip_addr(self, dns):

        try:
            addr = socket.gethostbyname_ex(dns)
            return self._validate_ip(addr)
        except Exception as e:
            return False

    def _process_search(self, results, **kwargs):
        """
        Processes an IPv4 search to return results that people care about. I guess.
        :param results:
        :param kwargs:
        :return:
        """

        display_field = kwargs.get('display_field', None)

        for result in results['results']:

            entity_list = []

            if isinstance(result[display_field], list):

                for df in result[display_field]:
                    entity_list.append(
                        self.mt.addEntity(
                            'maltego.{}'.format(kwargs.get('object_type', 'Website')),
                            '{}'.format(df)
                        )
                    )
            else:
                entity_list.append(
                    self.mt.addEntity(
                        'maltego.{}'.format(kwargs.get('object_type', 'Website')),
                        '{}'.format(result[display_field])
                    )
                )

            for k in result.keys():
                for e in entity_list:
                    e.addProperty(
                        fieldName='property.{}'.format(k).replace('=', '__'),
                        displayName='{}'.format(k),
                        matchingRule='loose',
                        value='{}'.format(result[k]).replace('=', '_equals_')
                    )

    def search_hash_to_ipv4_address(self, *args, **kwargs):
        """
        This method takes a hash (md5, sha1, sha256) and returns a list of and IPv4 addresses with a certificate
        matching that hash.
        :param args:
        :param kwargs:
        :return:
        """
        q = "443.https.tls.certificate.parsed.fingerprint_{}: {}".format(
            re.escape(kwargs.get('hash_type', 'sha256')), re.escape(kwargs.get('hash_value', 'None'))
        )
        results_page = kwargs.get('start_page', self.start_page)
        max_pages = kwargs.get('max_pages', self.max_pages)

        while True:
            results = self.connection['ipv4'].paged_search(q, fields=self.fields['ipv4'], page=results_page)
            self._process_search(results, object_type='IPv4Address', display_field='ip', **kwargs)

            if results['metadata']['page'] >= results['metadata']['pages'] or results['metadata']['page'] >= max_pages:
                break
            else:
                results_page += 1

        return self._finalize()

    def search_domain_to_ipv4(self, *args, **kwargs):
        """
        This method searches the IPv4 data set for the domain and returns any ips with a cert referencing that domain
        :param args:
        :param kwargs:
        :return:
        """
        q = "443.https.tls.certificate.parsed.names: {}".format(re.escape(kwargs.get('domain_name', 'example.com')))
        results_page = kwargs.get('start_page', self.start_page)
        max_pages = kwargs.get('max_pages', self.max_pages)

        while True:
            results = self.connection['ipv4'].paged_search(q, fields=self.fields['ipv4'], page=results_page)

            self._process_search(results, object_type='IPv4Address', display_field='ip', **kwargs)

            if results['metadata']['page'] >= results['metadata']['pages'] or results['metadata']['page'] >= max_pages:
                break
            else:
                results_page += 1

        return self._finalize()

    def search_ipv4_to_domains(self, *args, **kwargs):
        """
        Searches for ipv4 addresses and returns domains that are found in the associated certificate.
        """

        q = "ip: {} AND 443.https.tls.certificate.parsed.fingerprint_sha256: *".format(
            re.escape(kwargs.get('ip_address', '127.0.0.1'))
        )

        results_page = kwargs.get('start_page', self.start_page)
        max_pages = kwargs.get('max_pages', self.max_pages)

        while True:
            results = self.connection['ipv4'].paged_search(q, fields=self.fields['ipv4'], page=results_page)

            self._process_search(
                results,
                object_type='Website',
                display_field='443.https.tls.certificate.parsed.names',
                **kwargs
            )

            if results['metadata']['page'] >= results['metadata']['pages'] or results['metadata']['page'] >= max_pages:
                break
            else:
                results_page += 1

        return self._finalize()

    def search_ipv4_to_hash(self, *args, **kwargs):

        # TOOD: Were you drunk when you did this?

        """
        Searches for ipv4 addresses matching IP and returns a list of certificate hashes
        """

        q = "ip: {} AND 443.https.tls.certificate.parsed.fingerprint_sha256: *".format(
            re.escape(kwargs.get('ip_address', '127.0.0.1'))
        )

        results_page = kwargs.get('start_page', self.start_page)
        max_pages = kwargs.get('max_pages', self.max_pages)

        while True:
            results = self.connection['ipv4'].paged_search(q, fields=self.fields['ipv4'], page=results_page)

            self._process_search(
                results,
                object_type='Hash',
                display_field='443.https.tls.certificate.parsed.fingerprint_sha256',
                **kwargs
            )

            if results['metadata']['page'] >= results['metadata']['pages'] or results['metadata']['page'] >= max_pages:
                break
            else:
                results_page += 1

        return self._finalize()

    def search_issuer_cn_to_certificate_hash(self, *args, **kwargs):
        q = "parsed.issuer.common_name: {}".format(
            re.escape(kwargs.get('issuer_cn', 'Let\'s Encrypt Authority'))
        )

        results_page = kwargs.get('start_page', self.start_page)
        max_pages = kwargs.get('max_pages', self.max_pages)

        while True:
            results = self.connection['certificates'].paged_search(q, fields=self.fields['certificate'], page=results_page)

            self._process_search(
                results,
                object_type='Hash',
                display_field='parsed.fingerprint_sha256',
                **kwargs
            )

            if results['metadata']['page'] >= results['metadata']['pages'] or results['metadata']['page'] >= max_pages:
                break
            else:
                results_page += 1

        return self._finalize()

    def search_subject_dn_to_certificate_hash(self, *args, **kwargs):
        q = "parsed.subject_dn: {}".format(
            re.escape(kwargs.get('subject_dn', 'Let\'s Encrypt Authority'))
        )

        results_page = kwargs.get('start_page', self.start_page)
        max_pages = kwargs.get('max_pages', self.max_pages)

        while True:
            results = self.connection['certificates'].paged_search(q, fields=self.fields['certificate'],
                                                                   page=results_page)
            self._process_search(
                results,
                object_type='Hash',
                display_field='parsed.fingerprint_sha256',
                **kwargs
            )

            if results['metadata']['page'] >= results['metadata']['pages'] or results['metadata']['page'] >= max_pages:
                break
            else:
                results_page += 1

        return self._finalize()

    def search_ipv4_to_ports(self, *args, **kwargs):
        q = "ip: {} AND ports: *".format(
            re.escape(kwargs.get('ip_address', '127.0.0.1'))
        )

        results_page = kwargs.get('start_page', self.start_page)
        max_pages = kwargs.get('max_pages', self.max_pages)

        while True:
            results = self.connection['ipv4'].paged_search(q, fields=self.fields['ports'], page=results_page)

            self._process_search(
                results,
                object_type='Port',
                display_field='ports',
                **kwargs
            )

            if results['metadata']['page'] >= results['metadata']['pages'] or results['metadata']['page'] >= max_pages:
                break
            else:
                results_page += 1

        return self._finalize()

    def search_http_body_to_ip(self, *args, **kwargs):
        # TODO: Fix
        q = "80.http.get.body: {}".format(
            re.escape(kwargs.get('body_text', '<script>'))
        )

        results_page = kwargs.get('start_page', self.start_page)
        max_pages = kwargs.get('max_pages', self.max_pages)

        while True:
            results = self.connection['ipv4'].paged_search(q, fields=self.fields['ipv4'], page=results_page)

            self._process_search(
                results,
                object_type='IPv4Address',
                display_field='ip',
                **kwargs
            )

            if results['metadata']['page'] >= results['metadata']['pages'] or results['metadata']['page'] >= max_pages:
                break
            else:
                results_page += 1

        return self._finalize()

    def search_https_body_to_ip(self, *args, **kwargs):
        # TODO: Fix
        q = "443.https.get.body: {}".format(
            re.escape(kwargs.get('body_text', '<script>')),
        )

        results_page = kwargs.get('start_page', self.start_page)
        max_pages = kwargs.get('max_pages', self.max_pages)

        while True:
            results = self.connection['ipv4'].paged_search(q, fields=self.fields['ipv4'], page=results_page)

            self._process_search(
                results,
                object_type='IPv4Address',
                display_field='ip',
                **kwargs
            )

            if results['metadata']['page'] >= results['metadata']['pages'] or results['metadata']['page'] >= max_pages:
                break
            else:
                results_page += 1

        return self._finalize()

    def search_https_body_hash_to_ip(self, **kwargs):
        # TODO: Fix
        q = "443.https.get.body_sha256: {}".format(
            re.escape(kwargs.get('body_text', 'xxxxxxxxxxxxxxxxx')),
        )

        results_page = kwargs.get('start_page', self.start_page)
        max_pages = kwargs.get('max_pages', self.max_pages)

        while True:
            results = self.connection['ipv4'].paged_search(q, fields=self.fields['ipv4'], page=results_page)

            self._process_search(
                results,
                object_type='IPv4Address',
                display_field='ip',
                **kwargs
            )

            if results['metadata']['page'] >= results['metadata']['pages'] or results['metadata']['page'] >= max_pages:
                break
            else:
                results_page += 1

        return self._finalize()
        pass

    def search_http_body_hash_to_ip(self, **kwargs):
        # TODO: Fix
        q = "80.http.get.body_sha256: {}".format(
            re.escape(kwargs.get('body_text', 'xxxxxxxxxxxxxxxxx')),
        )

        results_page = kwargs.get('start_page', self.start_page)
        max_pages = kwargs.get('max_pages', self.max_pages)

        while True:
            results = self.connection['ipv4'].paged_search(q, fields=self.fields['ipv4'], page=results_page)

            self._process_search(
                results,
                object_type='IPv4Address',
                display_field='ip',
                **kwargs
            )

            if results['metadata']['page'] >= results['metadata']['pages'] or results['metadata']['page'] >= max_pages:
                break
            else:
                results_page += 1

        return self._finalize()
