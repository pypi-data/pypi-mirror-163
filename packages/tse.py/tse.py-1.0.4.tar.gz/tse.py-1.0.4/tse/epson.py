"""
The module for the Epson backend.

In this module the TSE protocol for Epson devices and helpers are implemented.
"""
import socket
import json
from base64 import b64decode
from datetime import datetime
from hashlib import sha256
from base64 import b64encode
from xml.etree import ElementTree
from pathlib import Path
from typing import Optional, List
from tse import exceptions as tse_ex
from tse import (
        TSEInfo, TSEState, TSERole, TSETransaction, TSESignature,
        TransactionRangeType, TimeRangeType)


def _hash(challenge: str, secret: str) -> bytes:
    """
    Hash the challenge and secret composition.

    This function hashes the given data using the following formula:
    encodeBase64(sha256(challenge + secret))

    Args:
        challenge: The challenge returned by the TSE.
        secret: The shared secret.
    """
    composition = challenge+secret

    return b64encode(sha256(composition.encode()).digest())


class _TSEHost:
    """
    This class offers the possibility to communicate with an Epson TSE host.

    The ePOS Device XML interface is used for communication. Any device
    that provides this interface can be addressed (e.g. the Epson TSE
    server or Epson TSE printer).

    During the initialization of the instance, a socket connection to the
    TSE host is established. To send data to the TSE, the respective TSE must
    be opened and then closed again. If the TSE is used exclusively by only
    one user, then this can also remain open. Opening and closing before
    and after writing is only necessary if several users share a TSE.

    .. code:: python

        tse_host = _TSEHost(<hostname>)

        tse_host.tse_open(<tse_id>)
        tse_host.tse_send(<tse_id>, <data_dict>)
        tse_host.tse_close(<tse_id>)
    """

    def __init__(
            self, host: str, ssl: bool = False, timeout: int = 120) -> None:
        """
        Initialize the _TSEHost instance.

        This method establishes a TCP socket connection to host and sets
        the *client_id* and *protocol_version* properties.

        Args:
            host: The hostname or IP address of the host.
            ssl: If true, a SSL encrypted connection is used.
            timeout: The socket timeout in seconds.

        Raises:
            tse.exceptions.ConnectionError: If a unexpected error occurred.
            tse.exceptions.ConnectionTimeoutError: If socket timeout occurred.
            tse.exceptions.ConnectionHostnameError: If hostname format is not
                correct.
        """
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(timeout)

            if ssl:
                self._socket.connect((host, 8143))
            else:
                self._socket.connect((host, 8009))

            response = self._socket.recv(1024)

            root = ElementTree.fromstring(response.decode().rstrip('\x00'))
            client_id = root.find('*/client_id').text  # type: ignore
            protocol_version = root.find(
                    '*/protocol_version').text  # type: ignore
            self._client_id = client_id
            self._protocol_version = protocol_version

        except socket.gaierror:
            raise tse_ex.ConnectionHostnameError(
                f'The connection to the host "{host}" could not '
                'be established. The hostname has no valid format.')

        except socket.timeout:
            raise tse_ex.ConnectionTimeoutError(
                f'The connection to the host "{host}" could not'
                'be established. A timeout error occurs.')

        except Exception as ex:
            raise tse_ex.ConnectionError(
                f'The connection to the host "{host}" could not '
                f'be established ({str(ex)}).')

    def __del__(self) -> None:
        """
        Cleanup the TSEHost instance.

        This method closes the connection to the TSE host.
        """
        try:
            self._socket.close()

        except AttributeError:
            pass

    @property
    def client_id(self) -> Optional[str]:
        """
        Get client-ID returnd for the host after connection.

        Returns:
            The client-ID as string or None if client is not connected.
        """
        return self._client_id

    @property
    def protocol_version(self) -> Optional[str]:
        """
        Get protocol version returnd for the host after connection.

        Returns:
            The protocol version as string or None if client is not connected.
        """
        return self._protocol_version

    def _send(self, xml: str) -> str:
        r"""
        Send ePOS device XML data to the Host.

        The method minifies the passed XML data and expands the string
        with the character *\\x00*. The host expect this character at the
        end of the sent data.

        Args:
            xml: The XML data as string.

        Returns:
            The XML response from the host as string without
            *\\x00* at the end.

        Raises:
            tse.exceptions.ConnectionTimeoutError: If a socket timeout
                occurred.
            tse.exceptions.ConnectionError: If there is no connection to
                the host.

        """
        try:
            xml = xml+'\x00'
            xml = xml.replace('\n', '').replace(' ', '')
            self._socket.send(xml.encode())
            response = ''

            while True:
                response += self._socket.recv(1024).decode()

                if '\x00' in response:
                    break

            return response.rstrip('\x00')

        except socket.timeout:
            raise tse_ex.ConnectionTimeoutError(
                'The data could not be sent to the TSE host. '
                'Timeout error occurs.')

        except (OSError, AttributeError):
            raise tse_ex.ConnectionError(
                'There is no established host connection. '
                'Please connect again.')

    def tse_open(self, tse_id: str) -> None:
        """
        Open the TSE for operations.

        Args:
            tse_id: The ID of the TSE device.

        Raises:
            tse.exceptions.TSEInUseError: If the TSE is in use.
            tse.exceptions.TSEOpenError: If the TSE could not be opened.
            tse.exceptions.TSEError: If an unexpected TSE error occurred.
            tse.exceptions.ConnectionTimeoutError: If a socket timeout
                occurred.
            tse.exceptions.ConnectionError: If there is no connection to
                the host.
        """
        xml = '''
            <open_device>
                <device_id>{}</device_id>
                <data>
                    <type>type_storage</type>
                </data>
            </open_device>
            '''.format(tse_id)

        root = ElementTree.fromstring(self._send(xml))
        code = root.find('./code').text  # type: ignore

        match code:
            case 'DEVICE_IN_USE':
                raise tse_ex.TSEInUseError(
                    f'The TSE {tse_id} is in use.')
            case 'DEVICE_OPEN_ERROR' | 'DEVICE_NOT_FOUND':
                raise tse_ex.TSEOpenError(
                    'The TSE {tse_id} could not be opened.')
            case 'OK':
                pass
            case _:
                raise tse_ex.TSEError(
                    f'An unexpected TSE error occurred: {code}.')

    def tse_send(self, tse_id: str, data: dict, timeout: int = 3) -> dict:
        """
        Send data to the TSE JSON API.

        The data passed in the data dictionary is converted to the JSON
        format and sent to the TSE. The method returns the return value
        of the TSE.

        Args:
            tse_id: The ID of the TSE device.
            data: The data as dictionary.
            timeout: TSE operation timeout in seconds.

        Raises:
            tse.exceptions.TSEInUseError: If the TSE is in use.
            tse.exceptions.TSEOpenError: If the TSE is not open.
            tse.exceptions.TSETimeoutError: If TSE timeout error occurred.
            tse.exceptions.TSEError: If an unexpected TSE error occurred.
            tse.exceptions.ConnectionTimeoutError: If a socket timeout
                occurred.
            tse.exceptions.ConnectionError: If there is no connection to
                the host.
        """
        xml = '''
            <device_data>
                <device_id>{}</device_id>
                <data>
                    <type>operate</type>
                    <timeout>{}</timeout>
                    <requestdata>{}</requestdata>
                </data>
            </device_data>"
            '''.format(tse_id, timeout*1000, json.dumps(data))

        root_element = ElementTree.fromstring(self._send(xml))
        code_element = root_element.find('.//code')
        result_element = root_element.find('./data/resultdata')

        if isinstance(code_element, ElementTree.Element):
            code = code_element.text

            match code:
                case 'ERROR_TIMEOUT':
                    raise tse_ex.TSETimeoutError(
                        'A timeout error occurred while sending data to '
                        'the TSE')
                case 'ERROR_DEVICE_BUSY':
                    raise tse_ex.TSEInUseError(
                        'The TSE is in use.')
                case 'DEVICE_NOT_OPEN':
                    raise tse_ex.TSEOpenError(
                        'The TSE device is not open.')
                case 'SUCCESS':
                    if isinstance(result_element, ElementTree.Element) \
                            and isinstance(result_element.text, str):
                        return json.loads(result_element.text)
                case _:
                    raise tse_ex.TSEError(
                        f'Unexpected TSE error occures: {code}.')

        return {}

    def tse_close(self, tse_id: str) -> None:
        """
        Close the TSE device.

        Args:
            tse_id: The ID of the TSE device.

        Raises:
            tse.exceptions.TSEInUseError: If the TSE is in use.
            tse.exceptions.TSEOpenError: If the TSE in not open.
            tse.exceptions.TSEError: If an unexpected TSE error occurred.
            tse.exceptions.ConnectionTimeoutError: If a socket timeout
                occurred.
            tse.exceptions.ConnectionError: If there is no connection to
                the host.
        """
        xml = '''
            <close_device>
                <device_id>{}</device_id>
            </close_device>
            '''.format(tse_id)

        root = ElementTree.fromstring(self._send(xml))
        code = root.find('code').text  # type: ignore

        match code:
            case 'DEVICE_IN_USE':
                raise tse_ex.TSEInUseError(
                    'The TSE {tse_id} is in use.')
            case 'DEVICE_NOT_OPEN':
                raise tse_ex.TSEOpenError(
                    'The TSE {tse_id} is not open.')
            case 'OK':
                pass
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')


class TSE():
    """
    The TSE implementation for the Epson TSE.

    This class implements the TSEType protocol defined in the tse module.

    See: :class:`tse.TSEType` object.
    """

    def __init__(
            self,
            tse_id: str,
            host: str,
            secret: str = 'EPSONKEY',
            ssl: bool = False,
            timeout: int = 5
            ) -> None:
        """
        Initialize the TSE instance.

        During the initialization process, a connection to TSE host is
        established, which is used for communication afterwards.

        Args:
            tse_id: The ID of the TSE device.
            host: The hostname or IP address of the host.
            secret: The shared secret for authentication.
            ssl: If true, a SSL encrypted connection is used.
            timeout: Timeout for TSE operations in seconds.

        Raises:
            tse.exceptions.ConnectionError: If there is no connection to
                the host.
            tse.exceptions.ConnectionTimeoutError: If socket timeout occurred.
            tse.exceptions.ConnectionHostnameError: If hostname format is not
                correct.
        """
        self._tse_host = _TSEHost(host, ssl, timeout=120)
        self._tse_id = tse_id
        self._timeout = timeout
        self._secret = secret

    def _get_challenge(self, user_id: str) -> str:
        """
        Get challenge.

        The challenge is used to calculate the hash value required
        for user authentication.

        **Role: None**

        Args:
            user_id: The ID of the user for whom a challenge should
                be requested.

        Raises:
            tse.exceptions.TSEInUseError: If the TSE is in use.
            tse.exceptions.TSEOpenError: If the TSE is not open.
            tse.exceptions.TSETimeoutError: If TSE timeout error occurred.
            tse.exceptions.TSEError: If an unexpected TSE error occurred.
            tse.exceptions.ConnectionTimeoutError: If a socket timeout
                occurred.
            tse.exceptions.ConnectionError: If there is no connection to
                the host.
        """
        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'GetChallenge',
            'input': {
                'userId': user_id
            },
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=120)

        code = result['result']

        match code:
            case 'EXECUTION_OK':
                pass
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

        return result['output']['challenge']

    def info(self) -> TSEInfo:
        """See: :meth:`tse.TSEType.info`."""
        json_data = {
            'storage': {
                'type': 'COMMON',
                'vendor': ''
            },
            'function': 'GetStorageInfo',
            'input': {},
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout
        )

        code = result['result']

        match code:
            case 'EXECUTION_OK':
                pass
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

        tse_info = result['output']['tseInformation']
        state_data = tse_info['tseInitializationState']
        certificate_expiration_date = datetime.strptime(
            tse_info['certificateExpirationDate'], '%Y-%m-%dT%H:%M:%S%z'
        )
        needs_self_test = not tse_info['hasPassedSelfTest']
        api_version = str(tse_info['softwareVersion'])

        match state_data:
            case 'INITIALIZED':
                state = TSEState.INITIALIZED
            case 'UNINITIALIZED':
                state = TSEState.UNINITIALIZED
            case 'DECOMMISSIONED':
                state = TSEState.DECOMMISSIONED

        info = TSEInfo(
            public_key=tse_info['tsePublicKey'],
            model_name=tse_info['vendorType'],
            state=state,
            has_valid_time=tse_info['hasValidTime'],
            certificate_id=tse_info['tseDescription'],
            certificate_expiration_date=certificate_expiration_date,
            signature_algorithm=tse_info['signatureAlgorithm'],
            unique_id=tse_info['cdcId'],
            signature_counter=tse_info['createdSignatures'],
            remaining_signatures=tse_info['remainingSignatures'],
            max_signatures=tse_info['maxSignatures'],
            registered_users=tse_info['registeredClients'],
            max_registered_users=tse_info['maxRegisteredClients'],
            serial_number=tse_info['serialNumber'],
            max_started_transactions=tse_info['maxStartedTransactions'],
            tar_export_size=tse_info['tarExportSize'],
            needs_self_test=needs_self_test,
            api_version=api_version,
        )

        return info

    def open(self) -> None:
        """See: :meth:`tse.TSEType.open`."""
        self._tse_host.tse_open(self._tse_id)

    def close(self) -> None:
        """See: :meth:`tse.TSEType.close`."""
        self._tse_host.tse_close(self._tse_id)

    def initialize(
            self,
            puk: str,
            admin_pin: str,
            time_admin_pin: str
            ) -> None:
        """See: :meth:`tse.TSEType.initialize`."""
        if len(puk) != 6:
            raise ValueError('The PUK must contain exactly 6 characters.')
        elif len(admin_pin) != 5:
            raise ValueError(
                'The admin PIN must contain exactly 5 characters.')
        elif len(time_admin_pin) != 5:
            raise ValueError(
                'The time admin PIN must contain exactly 5 characters.')

        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'SetUp',
            'input': {
                'puk': puk,
                'adminPin': admin_pin,
                'timeAdminPin': time_admin_pin
            },
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=120)

        code = result['result']

        match code:
            case 'OTHER_ERROR_TSE_ALREADY_SET_UP':
                raise tse_ex.TSEAlreadyInitializedError(
                    f'The TSE {self._tse_id} was already initialized.')
            case 'TSE1_ERROR_CERTIFICATE_EXPIRED':
                raise tse_ex.TSECertificateExpiredError(
                    f'The certificate of the TSE {self._tse_id} is expired. '
                    'Either the validity of the certificate has expired or '
                    'the TSE was decommissioned.')
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST':
                raise tse_ex.TSENeedsSelfTestError(
                    f'The TSE {self._tse_id} needs a self test.')
            case 'EXECUTION_OK':
                return None
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

    def login_user(
            self,
            user_id: str,
            role: TSERole,
            pin: str,
            ) -> None:
        """See: :meth:`tse.TSEType.login_user`."""
        challenge = self._get_challenge(user_id)

        hash = _hash(challenge, self._secret)

        if role == TSERole.ADMIN:
            json_data = {
                'storage': {
                    'type': 'TSE',
                    'vendor': 'TSE1'
                },
                'function': 'AuthenticateUserForAdmin',
                'input': {
                    'userId': user_id,
                    'pin': pin,
                    'hash': hash.decode()
                },
                'compress': {
                    'required': False,
                    'type': ''
                }
            }
        else:
            json_data = {
                'storage': {
                    'type': 'TSE',
                    'vendor': 'TSE1'
                },
                'function': 'AuthenticateUserForTimeAdmin',
                'input': {
                    'clientId': user_id,
                    'pin': pin,
                    'hash': hash.decode()
                },
                'compress': {
                    'required': False,
                    'type': ''
                }
            }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=120)

        code = result['result']

        match code:
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_PUK_CHANGE':
                raise tse_ex.TSEPukStateError(
                    'The PUK change required. Maybe the TSE is '
                    'not initialized')
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_PIN_CHANGE':
                raise tse_ex.TSEPinStateError(
                    'The PIN change required. Maybe the TSE is '
                    'not initialized')
            case 'OTHER_ERROR_INVALID_ADMIN_USER_ID':
                raise tse_ex.TSELoginError(
                    'Only the "Administrator" user can be logged in '
                    'with TSERole.ADMIN role.')
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST':
                raise tse_ex.TSENeedsSelfTestError(
                    f'The TSE {self._tse_id} needs a self test.')
            case 'TSE1_ERROR_AUTHENTICATION_FAILED':
                remaining_retries = result['output']['remainingRetries']

                raise tse_ex.TSELoginError(
                        f'The user {user_id} could not login as {role} role '
                        f'(remaining retries: {remaining_retries}).')
            case 'TSE1_ERROR_AUTHENTICATION_PIN_BLOCKED':
                raise tse_ex.TSEPinBlockedError(
                    f'The PIN for {role} was blocked.')
            case 'OTHER_ERROR_HOST_AUTHENTICATION_FAILED':
                raise tse_ex.TSESecretError('Wrong authentication secret.')
            case 'EXECUTION_OK':
                return None
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

    def logout_user(
            self,
            user_id: str,
            role: TSERole,
            ) -> None:
        """See: :meth:`tse.TSEType.logout_user`."""
        if role == TSERole.ADMIN:
            if user_id != 'Administrator':
                raise tse_ex.TSELogoutError(
                    'Only the "Administrator" user can be logged in '
                    'with TSERole.ADMIN role.'
                )

            json_data = {
                'storage': {
                    'type': 'TSE',
                    'vendor': 'TSE1'
                },
                'function': 'LogOutForAdmin',
                'input': {
                },
                'compress': {
                    'required': False,
                    'type': ''
                }
            }
        else:
            json_data = {
                'storage': {
                    'type': 'TSE',
                    'vendor': 'TSE1'
                },
                'function': 'LogOutForTimeAdmin',
                'input': {
                    'clientId': user_id,
                },
                'compress': {
                    'required': False,
                    'type': ''
                }
            }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout)

        code = result['result']

        match code:
            case 'TSE1_ERROR_CERTIFICATE_EXPIRED':
                raise tse_ex.TSECertificateExpiredError(
                    f'The certificate of the TSE {self._tse_id} is expired. '
                    'Either the validity of the certificate has expired or '
                    'the TSE was decommissioned.')
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST':
                raise tse_ex.TSENeedsSelfTestError(
                    f'The TSE {self._tse_id} needs a self test.')
            case 'OTHER_ERROR_UNAUTHENTICATED_ADMIN_USER':
                raise tse_ex.TSELogoutError(
                    f'The user {user_id} not logged in with '
                    'TSERole.ADMIN role.')
            case 'TSE1_ERROR_AUTHENTICATION_USER_NOT_LOGGED_IN':
                raise tse_ex.TSELogoutError(
                    'The Given user is not authenticated. Maybe the TSE is '
                    'decommissioned.')
            case 'OTHER_ERROR_UNAUTHENTICATED_TIME_ADMIN_USER':
                raise tse_ex.TSELogoutError(
                    f'The user {user_id} not logged in with '
                    'TSERole.TIME_ADMIN role.')
            case 'EXECUTION_OK':
                return None
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

    def change_pin(self, role: TSERole, puk: str, new_pin: str) -> None:
        """See: :meth:`tse.TSEType.change_pin`."""
        if role == TSERole.ADMIN:
            function = 'UnblockUserForAdmin'
        elif role == TSERole.TIME_ADMIN:
            function = 'UnblockUserForTimeAdmin'

        challenge = self._get_challenge('Administrator')
        hash = _hash(challenge, self._secret)

        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'AuthenticateHost',
            'input': {
                'userId': 'Administrator',
                'hash': hash.decode(),
            },
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout)

        code = result['result']

        match code:
            case 'EXECUTION_OK':
                pass
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': function,
            'input': {
                'userId': 'Administrator',
                'puk': puk,
                'newPin': new_pin
            },
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=120)

        code = result['result']
        error: Optional[tse_ex.TSEError] = None

        match code:
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_PIN_CHANGE':
                error = tse_ex.TSEPinStateError(
                    'The PIN change required. Maybe the TSE is '
                    'not initialized')
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_PUK_CHANGE':
                error = tse_ex.TSEPukStateError(
                    'The PUK change required. Maybe the TSE is '
                    'not initialized')
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST':
                error = tse_ex.TSENeedsSelfTestError(
                    f'The TSE {self._tse_id} needs a self test.')
            case 'TSE1_ERROR_AUTHENTICATION_PIN_BLOCKED':
                error = tse_ex.TSEAuthenticationError(
                    'The PUK is blocked. You must replace the TSE.')
            case 'TSE1_ERROR_AUTHENTICATION_FAILED':
                error = tse_ex.TSEAuthenticationError(
                    'Wrong PUK given.')
            case 'TSE1_ERROR_CERTIFICATE_EXPIRED':
                error = tse_ex.TSECertificateExpiredError(
                    f'The certificate of the TSE {self._tse_id} is expired. '
                    'Either the validity of the certificate has expired or '
                    'the TSE was decommissioned.')
            case 'TSE1_ERROR_TSE_INVALID_PARAMETER':
                error = tse_ex.TSEPinError(
                    'The new PIN must be different from the old one.')
            case 'JSON_ERROR_INVALID_PARAMETER_RANGE':
                error = tse_ex.TSEPinError(
                    'The length of the PIN must be 5 characters.')
            case 'EXECUTION_OK':
                return None
            case _:
                error = tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'DeauthenticateHost',
            'input': {
                'userId': 'Administrator'
            },
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=120)

        code = result['result']

        match code:
            case 'EXECUTION_OK':
                pass
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

        if error:
            raise error

    def register_user(self, user_id: str) -> None:
        """See: :meth:`tse.TSEType.register_user`."""
        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'RegisterClient',
            'input': {
                'clientId': user_id,
            },
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout)

        code = result['result']

        match code:
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST':
                raise tse_ex.TSENeedsSelfTestError(
                    f'The TSE {self._tse_id} needs a self test.')
            case 'TSE1_ERROR_NOT_AUTHORIZED':
                raise tse_ex.TSEInternalError(
                    'The internal TSE error occures if the TSE is '
                    'decommissioned or if an internal error occures. '
                    'If the TSE is not decommissioned, the TSE host must'
                    'be restarted.')
            case 'OTHER_ERROR_UNAUTHENTICATED_ADMIN_USER':
                raise tse_ex.TSEUnauthenticatedUserError(
                    'No user logged in with TSERole.ADMIN role.')
            case 'JSON_ERROR_INVALID_PARAMETER_RANGE':
                raise ValueError(
                    'Maximum length of user ID is 30 characters.')
            case 'EXECUTION_OK':
                return None
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

    def deregister_user(self, user_id: str) -> None:
        """See: :meth:`tse.TSEType.deregister_user`."""
        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'DeregisterClient',
            'input': {
                'clientId': user_id,
            },
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout)

        code = result['result']

        match code:
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST':
                raise tse_ex.TSENeedsSelfTestError(
                    f'The TSE {self._tse_id} needs a self test.')
            case 'TSE1_ERROR_NOT_AUTHORIZED':
                raise tse_ex.TSEInternalError(
                    'The internal TSE error occures if the TSE is '
                    'decommissioned or if an internal error occures. '
                    'If the TSE is not decommissioned, the TSE host must'
                    'be restarted.')
            case 'TSE1_ERROR_CLIENT_NOT_REGISTERED':
                raise tse_ex.TSEClientNotExistError(
                    f'The user {user_id} does not exist.')
            case 'OTHER_ERROR_UNAUTHENTICATED_ADMIN_USER':
                raise tse_ex.TSEUnauthenticatedUserError(
                    'No user logged in with TSERole.ADMIN role.')
            case 'JSON_ERROR_INVALID_PARAMETER_RANGE':
                raise ValueError(
                    'Maximum length of user ID is 30 characters.')
            case 'EXECUTION_OK':
                return None
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {result}.')

    def user_list(self) -> List[str]:
        """See: :meth:`tse.TSEType.user_list`."""
        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'GetRegisteredClientList',
            'input': {},
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout)

        code = result['result']

        match code:
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST':
                raise tse_ex.TSENeedsSelfTestError(
                    f'The TSE {self._tse_id} needs a self test.')
            case 'TSE1_ERROR_NOT_AUTHORIZED':
                raise tse_ex.TSEInternalError(
                    'The internal TSE error occures if the TSE is '
                    'decommissioned or if an internal error occures. '
                    'If the TSE is not decommissioned, the TSE host must'
                    'be restarted.')
            case 'EXECUTION_OK':
                return result['output']['registeredClientIdList']
            case 'OTHER_ERROR_UNAUTHENTICATED_ADMIN_USER':
                raise tse_ex.TSEUnauthenticatedUserError(
                    'No user logged in with TSERole.ADMIN role.')
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

    def run_self_test(self) -> None:
        """See: :meth:`tse.TSEType.run_self_test`."""
        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'RunTSESelfTest',
            'input': {},
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=120)

        code = result['result']

        match code:
            # case 'TSE1_ERROR_CLIENT_NOT_REGISTERED':
            #     raise tse_ex.TSENotInitializedError(
            #         'The TSE is not initialized.')
            case 'EXECUTION_OK' | 'TSE1_ERROR_CLIENT_NOT_REGISTERED':
                return None
            case _:
                raise tse_ex.TSESelfTestError(
                    f'Unexpected TSE error occures: {code}.')

    def factory_reset(self) -> None:
        """
        Reset the TSE device.

        .. note::
            This method only works for development versions of the TSE device.

        You need to reboot the printer afterwards. In case of the TSE
        Server, please power cycle the TSE by removing and reinserting it.

        **Role: None**

        Raises:
            tse.exceptions.TSEInUseError: If the TSE is in use.
            tse.exceptions.TSEOpenError: If the TSE is not open.
            tse.exceptions.TSETimeoutError: If TSE timeout error occurred.
            tse.exceptions.TSEError: If an unexpected TSE error occurred.
            tse.exceptions.ConnectionTimeoutError: If a socket timeout
                occurred.
            tse.exceptions.ConnectionError: If there is no connection to
                the host.
        """
        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'FactoryReset',
            'input': {
            },
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout)

        code = result['result']

        match code:
            case 'EXECUTION_OK':
                return None
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

    def register_secret(self, secret: str) -> None:
        """See: :meth:`tse.TSEType.register_secret`."""
        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'RegisterSecretKey',
            'input': {
                'secretKey': secret
            },
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout)

        code = result['result']

        match code:
            case 'OTHER_ERROR_UNAUTHENTICATED_ADMIN_USER':
                raise tse_ex.TSEUnauthenticatedUserError(
                    'No user logged in with TSERole.ADMIN role.')
            case 'TSE1_ERROR_NOT_AUTHORIZED':
                raise tse_ex.TSEInternalError(
                    'A internal TSE error occurred. Normally, '
                    'the TSE host must be restarted.')
            case 'JSON_ERROR_INVALID_PARAMETER_RANGE':
                raise ValueError('The secret must have exactly 8 characters.')
            case 'EXECUTION_OK':
                self._secret = secret

                return None
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

    def update_time(self, user_id: str, time: datetime) -> None:
        """See: :meth:`tse.TSEType.update_time`."""
        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'UpdateTime',
            'input': {
                'userId': user_id,
                'newDateTime': time.isoformat(timespec='seconds') + 'Z',
                'useTimeSync': False
            },
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout)

        code = result['result']

        match code:
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST':
                raise tse_ex.TSENeedsSelfTestError(
                    f'The TSE {self._tse_id} needs a self test.')
            case 'TSE1_ERROR_CERTIFICATE_EXPIRED':
                raise tse_ex.TSECertificateExpiredError(
                    f'The certificate of the TSE {self._tse_id} is expired.')
            case 'TSE1_ERROR_NOT_AUTHORIZED':
                raise tse_ex.TSEInternalError(
                    'A internal TSE error occurred. Normally, '
                    'the TSE host must be restarted.')
            case 'OTHER_ERROR_UNAUTHENTICATED_TIME_ADMIN_USER':
                raise tse_ex.TSEUnauthenticatedUserError(
                    f'The user "{user_id}" is not logged in with '
                    'TSERole.TIME_ADMIN or TSERole.ADMIN role.')
            case 'EXECUTION_OK':
                return None
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

    def lock(self, state: bool) -> None:
        """See: :meth:`tse.TSEType.lock`."""
        if state:
            function = 'LockTSE'
        else:
            function = 'UnlockTSE'

        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': function,
            'input': {},
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout)

        code = result['result']

        match code:
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST':
                raise tse_ex.TSENeedsSelfTestError(
                    f'The TSE {self._tse_id} needs a self test.')
            case 'TSE1_ERROR_NOT_AUTHORIZED':
                raise tse_ex.TSEInternalError(
                    'The internal TSE error occures if the TSE is '
                    'decommissioned or if an internal error occures. '
                    'If the TSE is not decommissioned, the TSE host must'
                    'be restarted.')
            case 'OTHER_ERROR_UNAUTHENTICATED_ADMIN_USER':
                raise tse_ex.TSEUnauthenticatedUserError(
                    'No user logged in with TSERole.ADMIN role.')
            case 'EXECUTION_OK':
                return None
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

    def disable_secure_element(self) -> None:
        """See: :meth:`tse.TSEType.disable_secure_element`."""
        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'DisableSecureElement',
            'input': {},
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout)

        code = result['result']

        match code:
            case 'TSE1_ERROR_NOT_AUTHORIZED':
                raise tse_ex.TSEInternalError(
                    'A internal TSE error occurred. Normally, '
                    'the TSE host must be restarted.')
            case 'OTHER_ERROR_UNAUTHENTICATED_ADMIN_USER':
                raise tse_ex.TSEUnauthenticatedUserError(
                    'No user logged in with TSERole.ADMIN role.')
            case 'TSE1_ERROR_TSE_HAS_UNFINISHED_TRANSACTIONS':
                raise tse_ex.TSEUnfinishedTransactionError(
                    'There are still unfinished transactions.')
            case 'TSE1_ERROR_NO_TIME_SET':
                raise tse_ex.TSETimeNotSetError(
                    'The TSE time is not set.')
            case 'EXECUTION_OK':
                return None
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

    def start_transaction(
            self,
            user_id: str,
            data: str,
            type: str) -> TSETransaction:
        """See: :meth:`tse.TSEType.start_transaction`."""
        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'StartTransaction',
            'input': {
                'clientId': user_id,
                'processData': data,
                'processType': type,
                'additionalData': ''
            },
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout)

        code = result['result']

        match code:
            case 'OTHER_ERROR_UNAUTHENTICATED_TIME_ADMIN_USER':
                raise tse_ex.TSEUnauthenticatedUserError(
                    'No user logged in with TSERole.TIME_ADMIN role.')
            case 'TSE1_ERROR_CERTIFICATE_EXPIRED':
                raise tse_ex.TSECertificateExpiredError(
                    f'The certificate of the TSE {self._tse_id} is expired.')
            case 'TSE1_ERROR_NO_TIME_SET':
                raise tse_ex.TSETimeNotSetError(
                    'The TSE time is not set.')
            case 'EXECUTION_OK':
                output = result['output']

                signature = TSESignature(
                    time=datetime.strptime(
                        output['logTime'], '%Y-%m-%dT%H:%M:%S%z'),
                    value=output['signature'],
                    counter=output['signatureCounter'])

                transaction = TSETransaction(
                    number=output['transactionNumber'],
                    serial_number=output['serialNumber'],
                    start_signature=signature)

                return transaction
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

    def update_transaction(
            self,
            user_id: str,
            transaction: TSETransaction,
            data: str,
            type: str) -> None:
        """See: :meth:`tse.TSEType.update_transaction`."""
        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'UpdateTransaction',
            'input': {
                'clientId': user_id,
                'transactionNumber': transaction.number,
                'processData': data,
                'processType': type,
                'additionalData': ''
            },
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout)

        code = result['result']

        match code:
            case 'OTHER_ERROR_UNAUTHENTICATED_TIME_ADMIN_USER':
                raise tse_ex.TSEUnauthenticatedUserError(
                    'No user logged in with TSERole.TIME_ADMIN role.')
            case 'TSE1_ERROR_CERTIFICATE_EXPIRED':
                raise tse_ex.TSECertificateExpiredError(
                    f'The certificate of the TSE {self._tse_id} is expired.')
            case 'TSE1_ERROR_NO_TIME_SET':
                raise tse_ex.TSETimeNotSetError(
                    'The TSE time is not set.')
            case 'EXECUTION_OK':
                output = result['output']

                signature = TSESignature(
                    time=datetime.strptime(
                        output['logTime'], '%Y-%m-%dT%H:%M:%S%z'),
                    value=output['signature'],
                    counter=output['signatureCounter'])

                transaction.update_signature = signature
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

    def finish_transaction(
            self,
            user_id: str,
            transaction: TSETransaction,
            data: str,
            type: str) -> None:
        """See: :meth:`tse.TSEType.finish_transaction`."""
        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'FinishTransaction',
            'input': {
                'clientId': user_id,
                'transactionNumber': transaction.number,
                'processData': data,
                'processType': type,
                'additionalData': ''
            },
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout)

        code = result['result']

        match code:
            case 'OTHER_ERROR_UNAUTHENTICATED_TIME_ADMIN_USER':
                raise tse_ex.TSEUnauthenticatedUserError(
                    'No user logged in with TSERole.TIME_ADMIN role.')
            case 'TSE1_ERROR_CERTIFICATE_EXPIRED':
                raise tse_ex.TSECertificateExpiredError(
                    f'The certificate of the TSE {self._tse_id} is expired.')
            case 'TSE1_ERROR_NO_TIME_SET':
                raise tse_ex.TSETimeNotSetError(
                    'The TSE time is not set.')
            case 'EXECUTION_OK':
                output = result['output']

                signature = TSESignature(
                    time=datetime.strptime(
                        output['logTime'], '%Y-%m-%dT%H:%M:%S%z'),
                    value=output['signature'],
                    counter=output['signatureCounter'])

                transaction.finish_signature = signature
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

    def started_transaction_list(self, user_id: str) -> List[int]:
        """See: :meth:`tse.TSEType.started_transaction_list`."""
        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'GetStartedTransactionList',
            'input': {
                'clientId': user_id
            },
            'compress': {
                'required': False,
                'type': ''
            }
        }

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=self._timeout)

        code = result['result']

        match code:
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST' | \
                    'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST_PASSED':
                raise tse_ex.TSENeedsSelfTestError(
                    f'The TSE {self._tse_id} needs a self test.')
            case 'EXECUTION_OK':
                return result['output']['startedTransactionNumberList']
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures: {code}.')

    def export(
            self,
            filename: Path,
            user_id: str,
            transaction: TransactionRangeType = None,
            time: TimeRangeType = None,
            delete_data: bool = False) -> None:
        """See: :meth:`tse.TSEType.export`."""
        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'input': {},
            'compress': {
                'required': False,
                'type': ''
            }
        }

        if not user_id:
            raise tse_ex.TSENoUserError(
                    'The TSE user_id must not be an empty string.')

        if time and transaction:
            raise tse_ex.TSEArgumentError(
                'Export can be filtered by time or transaction only. Using '
                'both filters at the same time is not possible.')

        if transaction and not time:
            if isinstance(transaction, tuple):
                json_data['function'] =\
                    'ExportFilteredByTransactionNumberInterval'
                json_data['input'] = {
                    'clientId': user_id,
                    'startTransactionNumber': transaction[0],
                    'endTransactionNumber': transaction[1]
                }
            elif isinstance(transaction, int):
                json_data['function'] = 'ExportFilteredByTransactionNumber'
                json_data['input'] = {
                    'clientId': user_id,
                    'transactionNumber': transaction,
                }

            else:
                raise tse_ex.TSEArgumentTypeError(
                    'The transaction parameter must be an interger or '
                    'a tuple of integer.')

        if time and not transaction:
            if isinstance(time, tuple):
                json_data['function'] =\
                    'ExportFilteredByPeriodOfTime'
                json_data['input'] = {
                    'clientId': user_id,
                    'startDate': time[0].isoformat(timespec='seconds') + 'Z',
                    'endDate': time[1].isoformat(timespec='seconds') + 'Z'
                }

            else:
                raise tse_ex.TSEArgumentTypeError(
                    'The time parameter must be a tuple of datetime.')

        if not transaction and not time:
            json_data['function'] = 'ArchiveExport'

        result = self._tse_host.tse_send(
            self._tse_id, json_data, timeout=20)

        code = result['result']

        match code:
            case 'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST' | \
                    'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST_PASSED':
                raise tse_ex.TSENeedsSelfTestError(
                    f'The TSE {self._tse_id} needs a self test.')
            case 'TSE1_ERROR_CERTIFICATE_EXPIRED':
                raise tse_ex.TSECertificateExpiredError(
                    f'The certificate of the TSE {self._tse_id} is '
                    'expired.')
            case 'OTHER_ERROR_CURRENTLY_EXPORTING':
                raise tse_ex.TSEAlreadyExportingError(
                    'The TSE is already exporting. Please wait a little.')
            case 'OTHER_ERROR_UNAUTHENTICATED_ADMIN_USER':
                raise tse_ex.TSEUnauthenticatedUserError(
                    'No user logged in with TSERole.ADMIN role.')
            case 'OTHER_ERROR_NO_TIME_SET_BEFORE_EXPORT':
                raise tse_ex.TSETimeNotSetError(
                    'The time was not set before export.')
            case 'EXECUTION_OK':
                pass
            case _:
                raise tse_ex.TSEError(
                    f'Unexpected TSE error occures during the export: {code}.')

        json_data = {
            'storage': {
                'type': 'TSE',
                'vendor': 'TSE1'
            },
            'function': 'GetExportData',
            'input': {},
            'compress': {
                'required': False,
                'type': ''
            }
        }

        error: Optional[tse_ex.TSEError] = None
        data = b''

        while True:
            result = self._tse_host.tse_send(
                self._tse_id, json_data, timeout=self._timeout)

            code = result['result']

            match code:
                case 'TSE1_ERROR_CERTIFICATE_EXPIRED':
                    raise tse_ex.TSECertificateExpiredError(
                        f'The certificate of the TSE {self._tse_id} is '
                        'expired.')
                case 'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST' | \
                        'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST_PASSED':
                    error = tse_ex.TSENeedsSelfTestError(
                        f'The TSE {self._tse_id} needs a self test.')
                case 'TSE1_ERROR_EXPORT_NO_DATA_AVAILABLE':
                    error = tse_ex.TSENoDataToExportError(
                        'No data to exort available. Please edit the '
                        'export filter.')
                    break
                case 'EXECUTION_OK':
                    status = result['output']['exportStatus']

                    if status == 'EXPORT_INCOMPETE':
                        data += result['output']['exportData'].encode()

                    if status == 'EXPORT_COMPLETE':
                        data += result['output']['exportData'].encode()

                        break
                case _:
                    error = tse_ex.TSEError(
                        'Unexpected TSE error occures during loading '
                        f'the export data: {code}.')
                    break

        if not error:
            json_data = {
                'storage': {
                    'type': 'TSE',
                    'vendor': 'TSE1'
                },
                'function': 'FinalizeExport',
                'input': {
                    'deleteData': delete_data},
                'compress': {
                    'required': False,
                    'type': ''
                }
            }

            result = self._tse_host.tse_send(
                self._tse_id, json_data, timeout=self._timeout)

            code = result['result']

            match code:
                case 'TSE1_ERROR_CERTIFICATE_EXPIRED':
                    raise tse_ex.TSECertificateExpiredError(
                        f'The certificate of the TSE {self._tse_id} is '
                        'expired.')
                case 'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST' | \
                        'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST_PASSED':
                    raise tse_ex.TSENeedsSelfTestError(
                        f'The TSE {self._tse_id} needs a self test.')
                case 'EXECUTION_OK':
                    filename.write_bytes(b64decode(data))
                case _:
                    raise tse_ex.TSEError(
                        'Unexpected TSE error occures during the '
                        f'export finalization: {code}.')

        else:
            json_data = {
                'storage': {
                    'type': 'TSE',
                    'vendor': 'TSE1'
                },
                'function': 'CancelExport',
                'input': {},
                'compress': {
                    'required': False,
                    'type': ''
                }
            }

            result = self._tse_host.tse_send(
                self._tse_id, json_data, timeout=self._timeout)

            code = result['result']

            match code:
                case 'TSE1_ERROR_CERTIFICATE_EXPIRED':
                    raise tse_ex.TSECertificateExpiredError(
                        f'The certificate of the TSE {self._tse_id} is '
                        'expired.')
                case 'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST' | \
                        'TSE1_ERROR_WRONG_STATE_NEEDS_SELF_TEST_PASSED':
                    raise tse_ex.TSENeedsSelfTestError(
                        f'The TSE {self._tse_id} needs a self test.')
                case 'EXECUTION_OK':
                    return
                case _:
                    raise tse_ex.TSEError(
                        'Unexpected TSE error occures during export '
                        f'canceling: {code}.')
