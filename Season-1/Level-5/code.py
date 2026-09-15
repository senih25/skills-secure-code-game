# Welcome to Secure Code Game Season-1/Level-5!

# This is the last level of our first season, good luck!

import binascii
import secrets
import hashlib
import os
import bcrypt


class Random_generator:

    # generates a random token using a cryptographically secure source
    def generate_token(self, length=8, alphabet=(
        '0123456789'
        'abcdefghijklmnopqrstuvwxyz'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    )):
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    # generates salt using bcrypt's reviewed implementation
    def generate_salt(self, rounds=12):
        return bcrypt.gensalt(rounds)


class SHA256_hasher:

    # produces the password hash by combining a SHA-256 prehash with bcrypt
    def password_hash(self, password, salt):
        password = binascii.hexlify(hashlib.sha256(password.encode()).digest())
        password_hash = bcrypt.hashpw(password, salt)
        return password_hash.decode('ascii')

    # verifies the supplied password against the bcrypt hash
    def password_verification(self, password, password_hash):
        password = binascii.hexlify(hashlib.sha256(password.encode()).digest())
        password_hash = password_hash.encode('ascii')
        return bcrypt.checkpw(password, password_hash)


class MD5_hasher:
    """Backward-compatible interface implemented securely without MD5."""

    def password_hash(self, password):
        return SHA256_hasher().password_hash(password, bcrypt.gensalt())

    def password_verification(self, password, password_hash):
        return SHA256_hasher().password_verification(password, password_hash)


# Sensitive values are supplied by the runtime environment, never source code.
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
PUBLIC_KEY = os.environ.get('PUBLIC_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
PASSWORD_HASHER = 'SHA256_hasher'
