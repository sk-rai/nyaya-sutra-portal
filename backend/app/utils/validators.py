"""Input validation utilities for the Nyaya Sutra Backend API.

Provides validation functions for email addresses and Indian mobile phone numbers.
"""

import re


# Email regex: basic but covers standard formats
_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

# Indian mobile: exactly 10 digits, starting with 6-9
_PHONE_REGEX = re.compile(r"^[6-9]\d{9}$")


def validate_email(email: str) -> bool:
    """Validate that a string is a valid email format.

    Args:
        email: The string to validate.

    Returns:
        True if the string matches a valid email format, False otherwise.
    """
    if not email or not isinstance(email, str):
        return False
    return bool(_EMAIL_REGEX.match(email.strip()))


def validate_phone(phone: str) -> bool:
    """Validate that a string is a valid 10-digit Indian mobile number.

    Indian mobile numbers start with 6, 7, 8, or 9 and are exactly 10 digits.

    Args:
        phone: The string to validate.

    Returns:
        True if the string is a valid Indian mobile number, False otherwise.
    """
    if not phone or not isinstance(phone, str):
        return False
    return bool(_PHONE_REGEX.match(phone.strip()))
