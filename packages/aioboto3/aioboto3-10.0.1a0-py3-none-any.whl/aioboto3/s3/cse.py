import asyncio
import base64
import json
import inspect
import os
import re
import sys
import struct
from io import BytesIO
from typing import Dict, Union, IO, Optional, Any, Tuple

import aioboto3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC, CTR, ECB
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.backends.openssl.rsa import _RSAPrivateKey, _RSAPublicKey
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


RANGE_REGEX = re.compile(r'bytes=(?P<start>\d+)-(?P<end>\d+)*')
AES_BLOCK_SIZE = 128
AES_BLOCK_SIZE_BYTES = 16
JAVA_LONG_MAX_VALUE = 9223372036854775807


# Just so it looks like the object aiohttp returns
class DummyAIOFile(object):
    """So that response['Body'].read() presents the same way as a normal S3 get"""

    def __init__(self, data: bytes):
        self.file = BytesIO(data)

    async def read(self, n=-1):
        return self.file.read(n)

    async def readany(self):
        return self.file.read()

    async def readexactly(self, n):
        return self.file.read(n)

    async def readchunk(self):
        return self.file.read(), True


class DecryptError(Exception):
    pass


class CryptoContext(object):
    async def setup(self):
        """
        Coroutine to perform any setup
        """
        pass

    async def close(self):
        """
        Coroutine to perform any teardown
        """

    async def get_decryption_aes_key(self, key: bytes, material_description: Dict[str, Any]) -> bytes:
        """
        Get decryption key for a given S3 object

        :param key: Base64 decoded version of x-amz-key-v2
        :param material_description: JSON decoded x-amz-matdesc
        :return: Raw AES key bytes
        """
        raise NotImplementedError()

    async def get_encryption_aes_key(self) -> Tuple[bytes, Dict[str, str], str]:
        """
        Get encryption key to encrypt an S3 object

        :return: Raw AES key bytes, Stringified JSON x-amz-matdesc, Base64 encoded x-amz-key-v2
        """
        raise NotImplementedError()


class AsymmetricCryptoContext(CryptoContext):
    """
    Crypto context which uses public-private key cryptography.

    The public and private keys need to be loaded in by ``cryptography.hazmat.primitives.serialization.*``

    :param public_key: Public key object
    :param private_key: Private key object
    :param loop: Event loop
    """

    def __init__(self, public_key: Optional[_RSAPublicKey] = None,
                 private_key: Optional[_RSAPrivateKey] = None, loop: Optional[asyncio.AbstractEventLoop] = None):

        self.public_key = public_key
        self.private_key = private_key

        self._loop = loop
        if not loop:
            self._loop = asyncio.get_event_loop()

    async def get_decryption_aes_key(self, key: bytes, material_description: Dict[str, Any]) -> bytes:
        """
        Get decryption key for a given S3 object

        :param key: Base64 decoded version of x-amz-key
        :param material_description: JSON decoded x-amz-matdesc
        :return: Raw AES key bytes
        """
        if self.private_key is None:
            raise ValueError('Private key not provided during initialisation, cannot decrypt key encrypting key')

        plaintext = await self._loop.run_in_executor(None, lambda: (self.private_key.decrypt(key, padding.PKCS1v15())))

        return plaintext

    async def get_encryption_aes_key(self) -> Tuple[bytes, Dict[str, str], str]:
        """
        Get encryption key to encrypt an S3 object

        :return: Raw AES key bytes, Stringified JSON x-amz-matdesc, Base64 encoded x-amz-key
        """
        if self.public_key is None:
            raise ValueError('Public key not provided during initialisation, cannot encrypt key encrypting key')

        random_bytes = os.urandom(32)

        ciphertext = await self._loop.run_in_executor(
            None, lambda: (self.public_key.encrypt(random_bytes, padding.PKCS1v15())))

        return random_bytes, {}, base64.b64encode(ciphertext).decode()

    @staticmethod
    def from_der_public_key(data: bytes) -> _RSAPublicKey:
        """
        Convert public key in DER encoding to a Public key object

        :param data: public key bytes
        """

        return serialization.load_der_public_key(data, default_backend())

    @staticmethod
    def from_der_private_key(data: bytes, password: Optional[str] = None) -> _RSAPrivateKey:
        """
        Convert private key in DER encoding to a Private key object

        :param data: private key bytes
        :param password: password the private key is encrypted with
        """
        return serialization.load_der_private_key(data, password, default_backend())


class SymmetricCryptoContext(CryptoContext):
    """
    Crypto context which uses symmetric cryptography.

    The key field should be a valid AES key.

    :param key: Key bytes
    :param loop: Event loop
    """

    def __init__(self, key: bytes, loop: Optional[asyncio.AbstractEventLoop] = None):
        self.key = key
        self._backend = default_backend()
        self._cipher = Cipher(AES(self.key), ECB(), backend=self._backend)

        self._loop = loop
        if not loop:
            self._loop = asyncio.get_event_loop()

    async def get_decryption_aes_key(self, key: bytes, material_description: Dict[str, Any]) -> bytes:
        """
        Get decryption key for a given S3 object

        :param key: Base64 decoded version of x-amz-key
        :param material_description: JSON decoded x-amz-matdesc
        :return: Raw AES key bytes
        """

        # So it seems when java just calls Cipher.getInstance('AES') it'll default to AES/ECB/PKCS5Padding
        aesecb = self._cipher.decryptor()
        padded_result = await self._loop.run_in_executor(None, lambda: (aesecb.update(key) + aesecb.finalize()))

        unpadder = PKCS7(AES.block_size).unpadder()
        result = await self._loop.run_in_executor(None, lambda: (unpadder.update(padded_result) + unpadder.finalize()))

        return result

    async def get_encryption_aes_key(self) -> Tuple[bytes, Dict[str, str], str]:
        """
        Get encryption key to encrypt an S3 object

        :return: Raw AES key bytes, Stringified JSON x-amz-matdesc, Base64 encoded x-amz-key
        """

        random_bytes = os.urandom(32)

        padder = PKCS7(AES.block_size).padder()
        padded_result = await self._loop.run_in_executor(
            None, lambda: (padder.update(random_bytes) + padder.finalize()))

        aesecb = self._cipher.encryptor()
        encrypted_result = await self._loop.run_in_executor(
            None, lambda: (aesecb.update(padded_result) + aesecb.finalize()))

        return random_bytes, {}, base64.b64encode(encrypted_result).decode()


class KMSCryptoContext(CryptoContext):
    """
    Crypto context which uses symmetric cryptography.

    The key field should be a valid AES key.

    E.g. if you wanted to set the KMS region, add kms_client_args={'region_name': 'eu-west-1'}

    :param key: Key bytes
    :param kms_client_args: Will be expanded when getting a KMS client
    :param authenticated_encryption: Uses AES-GCM instead of AES-CBC (also allows range gets of files)
    :param loop: Event loop
    """

    def __init__(self, keyid: Optional[str] = None, kms_client_args: Optional[dict] = None,
                 authenticated_encryption: bool = True):
        self.kms_key = keyid
        self.authenticated_encryption = authenticated_encryption

        # Store the client instead of creating one every time, performance wins when doing many files
        self._kms_client = None
        self._kms_client_args = kms_client_args if kms_client_args else {}
        self._session = None

    async def setup(self):
        self._session = aioboto3.Session()
        self._kms_client = await self._session.client('kms', **self._kms_client_args).__aenter__()

    async def close(self):
        await self._kms_client.close()

    async def get_decryption_aes_key(self, key: bytes, material_description: Dict[str, Any]) -> bytes:
        kms_data = await self._kms_client.decrypt(
            CiphertextBlob=key,
            EncryptionContext=material_description
        )
        return kms_data['Plaintext']

    async def get_encryption_aes_key(self) -> Tuple[bytes, Dict[str, str], str]:
        if self.kms_key is None:
            raise ValueError('KMS Key not provided during initalisation, cannot decrypt key encrypting key')

        encryption_context = {'kms_cmk_id': self.kms_key}
        kms_resp = await self._kms_client.generate_data_key(
            KeyId=self.kms_key,
            EncryptionContext=encryption_context,
            KeySpec='AES_256'
        )

        return kms_resp['Plaintext'], encryption_context, base64.b64encode(kms_resp['CiphertextBlob']).decode()


class MockKMSCryptoContext(KMSCryptoContext):
    def __init__(self, aes_key: bytes, material_description: dict, encrypted_key: bytes,
                 authenticated_encryption: bool = True):
        super(MockKMSCryptoContext, self).__init__()
        self.aes_key = aes_key
        self.material_description = material_description
        self.encrypted_key = encrypted_key
        self.authenticated_encryption = authenticated_encryption

    async def setup(self):
        pass

    async def close(self):
        pass

    async def get_decryption_aes_key(self, key: bytes, material_description: Dict[str, Any]) -> bytes:
        return self.aes_key

    async def get_encryption_aes_key(self) -> Tuple[bytes, Dict[str, str], str]:
        return self.aes_key, self.material_description.copy(), base64.b64encode(self.encrypted_key).decode()


class S3CSE(object):
    """
    S3 Client-side encryption wrapper.

    To change S3 region add s3_client_args={'region_name': 'eu-west-1'}

    To use this object, either use it with ``async with S3CSE(...) as s3_cse:``
    Or run the setup() and close() coro's respectively

    :param crypto_context: Takes a cryto context object from above
    :param s3_client_args: Optional dict of S3 client args
    """

    def __init__(self, crypto_context: CryptoContext, s3_client_args: Optional[dict] = None):
        self._loop = None
        self._backend = default_backend()

        self._crypto_context = crypto_context
        self._session = None
        self._s3_client = None
        self._s3_client_args = s3_client_args if s3_client_args else {}

    async def setup(self):
        if sys.version_info < (3, 7):
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = asyncio.get_running_loop()

        self._session = aioboto3.Session()
        self._s3_client = await self._session.client('s3', **self._s3_client_args).__aenter__()
        await self._crypto_context.setup()

    async def close(self):
        await self._s3_client.close()
        await self._crypto_context.close()

    async def __aenter__(self):
        await self.setup()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    # noinspection PyPep8Naming
    async def get_object(self, Bucket: str, Key: str, **kwargs) -> dict:
        """
        S3 GetObject. Takes same args as Boto3 documentation

        Decrypts any CSE

        :param Bucket: S3 Bucket
        :param Key: S3 Key (filepath)
        :return: returns same response as a normal S3 get_object
        """
        if self._s3_client is None:
            await self.setup()

        # Ok so if we are doing a range get. We need to align the range start/end with AES block boundaries
        # 9223372036854775806 is 8EiB so I have no issue with hardcoding it.
        # We pass the actual start, desired start and desired end to the decrypt function so that it can
        # generate the correct IV's for starting decryption at that block and then chop off the start and end of the
        # AES block so it matches what the user is expecting.
        _range = kwargs.get('Range')
        actual_range_start = None
        desired_range_start = None
        desired_range_end = None
        if _range:
            range_match = RANGE_REGEX.match(_range)
            if not range_match:
                raise ValueError('Dont understand this range value {0}'.format(_range))

            desired_range_start = int(range_match.group(1))
            desired_range_end = range_match.group(2)
            if desired_range_end is None:
                desired_range_end = 9223372036854775806
            else:
                desired_range_end = int(desired_range_end)

            actual_range_start, actual_range_end = _get_adjusted_crypto_range(desired_range_start, desired_range_end)

            # Update range with actual start_end
            kwargs['Range'] = 'bytes={0}-{1}'.format(actual_range_start, actual_range_end)

        s3_response = await self._s3_client.get_object(Bucket=Bucket, Key=Key, **kwargs)
        metadata = s3_response['Metadata']
        whole_file_length = int(s3_response['ResponseMetadata']['HTTPHeaders']['content-length'])

        if 'x-amz-key' not in metadata and 'x-amz-key-v2' not in metadata:
            # No crypto
            return s3_response

        if 'x-amz-key' in metadata:
            # Crypto V1
            # Todo move the file obj into the decrypt to do streaming
            file_data = await s3_response['Body'].read()
            body = await self._decrypt_v1(file_data, metadata, actual_range_start)
        else:
            # Crypto V2
            # Todo move the file obj into the decrypt to do streaming
            file_data = await s3_response['Body'].read()
            body = await self._decrypt_v2(file_data, metadata, whole_file_length,
                                          actual_range_start, desired_range_start,
                                          desired_range_end)

        s3_response['Body'] = DummyAIOFile(body)

        return s3_response

    async def _decrypt_v1(self, file_data: bytes, metadata: Dict[str, str], range_start: Optional[int] = None) -> bytes:
        if range_start:
            raise DecryptError('Cant do range get when not using KMS encryption')

        decryption_key = base64.b64decode(metadata['x-amz-key'])
        material_description = json.loads(metadata['x-amz-matdesc'])

        aes_key = await self._crypto_context.get_decryption_aes_key(decryption_key, material_description)

        # x-amz-key - Contains base64 encrypted key
        # x-amz-iv - AES IVs
        # x-amz-matdesc - JSON Description of client-side master key (used as encryption context as is)
        # x-amz-unencrypted-content-length - Unencrypted content length

        iv = base64.b64decode(metadata['x-amz-iv'])

        # TODO look at doing AES as stream

        # AES/CBC/PKCS5Padding
        aescbc = Cipher(AES(aes_key), CBC(iv), backend=self._backend).decryptor()
        padded_result = await self._loop.run_in_executor(None, lambda: (aescbc.update(file_data) + aescbc.finalize()))

        unpadder = PKCS7(AES.block_size).unpadder()
        result = await self._loop.run_in_executor(None, lambda: (unpadder.update(padded_result) + unpadder.finalize()))

        return result

    async def _decrypt_v2(self, file_data: bytes, metadata: Dict[str, str], entire_file_length: int,
                          range_start: Optional[int] = None, desired_start: Optional[int] = None,
                          desired_end: Optional[int] = None) -> bytes:

        decryption_key = base64.b64decode(metadata['x-amz-key-v2'])
        material_description = json.loads(metadata['x-amz-matdesc'])

        aes_key = await self._crypto_context.get_decryption_aes_key(decryption_key, material_description)

        # x-amz-key-v2 - Contains base64 encrypted key
        # x-amz-iv - AES IVs
        # x-amz-matdesc - JSON Description of client-side master key (used as encryption context as is)
        # x-amz-unencrypted-content-length - Unencrypted content length
        # x-amz-wrap-alg - Key wrapping algo, either AESWrap, RSA/ECB/OAEPWithSHA-256AndMGF1Padding or KMS
        # x-amz-cek-alg - AES/GCM/NoPadding or AES/CBC/PKCS5Padding
        # x-amz-tag-len - AEAD Tag length in bits

        iv = base64.b64decode(metadata['x-amz-iv'])

        # TODO look at doing AES as stream
        if metadata.get('x-amz-cek-alg', 'AES/CBC/PKCS5Padding') == 'AES/GCM/NoPadding':
            # AES/GCM/NoPadding

            # So begin the nastyness
            if range_start is not None:
                # Generate IV's as if you were doing so for each block until we get to the one we need
                iv = _adjust_iv_for_range(iv, range_start)
                # IV is now 16 bytes not 12

                aesctr = Cipher(AES(aes_key), CTR(iv), backend=self._backend).decryptor()

                result = await self._loop.run_in_executor(None, lambda: (aesctr.update(file_data) + aesctr.finalize()))

                # Possible remove AEAD tag if our range covers the end
                aead_tag_len = int(metadata['x-amz-tag-len']) // 8
                max_offset = entire_file_length - aead_tag_len - 1
                desired_end = max_offset if desired_end > max_offset else desired_end

                # Chop file
                result = result[desired_start:desired_end]

            else:
                aesgcm = AESGCM(aes_key)

                try:
                    result = await self._loop.run_in_executor(None, lambda: aesgcm.decrypt(iv, file_data, None))
                except InvalidTag:
                    raise DecryptError('Failed to decrypt, AEAD tag is incorrect. Possible key or IV are incorrect')

        else:
            if range_start:
                raise DecryptError('Cannot decrypt AES-CBC file with range')

            # AES/CBC/PKCS5Padding
            aescbc = Cipher(AES(aes_key), CBC(iv), backend=self._backend).decryptor()
            padded_result = await self._loop.run_in_executor(
                None, lambda: (aescbc.update(file_data) + aescbc.finalize()))

            unpadder = PKCS7(AES.block_size).unpadder()
            result = await self._loop.run_in_executor(
                None, lambda: (unpadder.update(padded_result) + unpadder.finalize()))

        return result

    async def put_object(self, Body: Union[bytes, IO], Bucket: str, Key: str, Metadata: Dict = None, **kwargs):
        """
        PutObject. Takes same args as Boto3 documentation

        Encrypts files

        :param: Body: File data
        :param Bucket: S3 Bucket
        :param Key: S3 Key (filepath)
        """
        if self._s3_client is None:
            await self.setup()

        if hasattr(Body, 'read'):
            if inspect.iscoroutinefunction(Body.read):
                Body = await Body.read()
            else:
                Body = Body.read()

        # We do some different V2 stuff if using kms
        is_kms = isinstance(self._crypto_context, KMSCryptoContext)
        # noinspection PyUnresolvedReferences
        authenticated_crypto = is_kms and self._crypto_context.authenticated_encryption

        Metadata = Metadata if Metadata is not None else {}

        aes_key, matdesc_metadata, key_metadata = await self._crypto_context.get_encryption_aes_key()

        if is_kms and authenticated_crypto:
            Metadata['x-amz-cek-alg'] = 'AES/GCM/NoPadding'
            Metadata['x-amz-tag-len'] = str(AES_BLOCK_SIZE)
            iv = os.urandom(12)

            # 16byte 128bit authentication tag forced
            aesgcm = AESGCM(aes_key)

            result = await self._loop.run_in_executor(None, lambda: aesgcm.encrypt(iv, Body, None))

        else:
            if is_kms:  # V1 is always AES/CBC/PKCS5Padding
                Metadata['x-amz-cek-alg'] = 'AES/CBC/PKCS5Padding'

            iv = os.urandom(16)

            padder = PKCS7(AES.block_size).padder()
            padded_result = await self._loop.run_in_executor(None, lambda: (padder.update(Body) + padder.finalize()))

            aescbc = Cipher(AES(aes_key), CBC(iv), backend=self._backend).encryptor()
            result = await self._loop.run_in_executor(None, lambda: (aescbc.update(padded_result) + aescbc.finalize()))

        # For all V1 and V2
        Metadata['x-amz-unencrypted-content-length'] = str(len(Body))
        Metadata['x-amz-iv'] = base64.b64encode(iv).decode()
        Metadata['x-amz-matdesc'] = json.dumps(matdesc_metadata)

        if is_kms:
            Metadata['x-amz-wrap-alg'] = 'kms'
            Metadata['x-amz-key-v2'] = key_metadata
        else:
            Metadata['x-amz-key'] = key_metadata

        await self._s3_client.put_object(
            Bucket=Bucket,
            Key=Key,
            Body=result,
            Metadata=Metadata,
            **kwargs
        )


def _adjust_iv_for_range(iv: bytes, byte_offset: int) -> bytes:
    if len(iv) != 12:
        raise RuntimeError('IV must be 12 bytes long for AES-GCM/CTR')

    block_size = AES_BLOCK_SIZE
    block_offset = byte_offset // block_size
    if block_offset * block_size != byte_offset:
        raise RuntimeError('Range size invalid. Should never hit this as range should be adjusted by now')

    j0 = _compute_j0(iv)
    return _increment_blocks(j0, block_offset)


def _get_adjusted_crypto_range(start: int, end: int) -> Tuple[int, int]:
    start = _get_cipher_block_lower_bound(start)
    end = _get_cipher_block_upper_bound(end)  # Copied from teh JAVA

    return start, end


def _get_cipher_block_lower_bound(value: int) -> int:
    lower_bound = value - (value % AES_BLOCK_SIZE) - AES_BLOCK_SIZE
    return max(lower_bound, 0)


def _get_cipher_block_upper_bound(value: int) -> int:
    offset = AES_BLOCK_SIZE - (value % AES_BLOCK_SIZE)
    upper_bound = value + offset + AES_BLOCK_SIZE
    return min(upper_bound, JAVA_LONG_MAX_VALUE)


def _compute_j0(iv: bytes) -> bytes:
    j0 = iv + (b'\x00' * (AES_BLOCK_SIZE_BYTES - 13)) + b'\x01'   # iv must be of length 12

    return _increment_blocks(j0, 1)


def _increment_blocks(counter: bytes, block_delta: int) -> bytes:
    if block_delta == 0:
        return counter

    if not counter or len(counter) != 16:
        raise ValueError('Counter must be 16 bytes long')

    byte_buffer = [0] * 8

    i = 12
    while i <= 15:
        byte_buffer[i-8] = counter[i]
        i += 1

    result = struct.pack('>Q', struct.unpack('>Q', bytes(byte_buffer))[0] + block_delta)

    counter = counter[:12] + result[4:8]

    return counter
