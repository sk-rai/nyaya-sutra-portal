"""OTP generation and verification utilities.

Provides functions for generating random 6-digit OTPs,
hashing them with bcrypt, and verifying codes against hashes.
"""

import random
import string

import bcrypt


def generate_otp() -> str:
    """Generate a random 6-digit OTP code.

    Returns:
        A zero-padded 6-digit string (e.g., "003421", "123456").
    """
    code = random.randint(0, 999999)
    return f"{code:06d}"


def hash_otp(code: str) -> str:
    """Hash an OTP code using bcrypt.

    Args:
        code: The plaintext OTP code to hash.

    Returns:
        The bcrypt hash as a UTF-8 string.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(code.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_otp_hash(code: str, hashed: str) -> bool:
    """Verify an OTP code against a bcrypt hash.

    Args:
        code: The plaintext OTP code to verify.
        hashed: The bcrypt hash to verify against.

    Returns:
        True if the code matches the hash, False otherwise.
    """
    try:
        return bcrypt.checkpw(code.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False
