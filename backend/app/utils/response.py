"""Standard response envelope utilities for the Nyaya Sutra Backend API.

All API responses follow a consistent JSON envelope format:
{
    "success": bool,
    "data": object | null,
    "error": object | null
}
"""

from flask import jsonify


def success_response(data, status=200):
    """Create a success response in the standard envelope format.

    Args:
        data: The response payload (dict, list, or any JSON-serializable value).
        status: HTTP status code (default 200).

    Returns:
        A Flask Response with JSON body and the given HTTP status.
    """
    response = jsonify({
        "success": True,
        "data": data,
        "error": None,
    })
    response.status_code = status
    return response


def error_response(code, message, details=None, status=400):
    """Create an error response in the standard envelope format.

    Args:
        code: Machine-readable error code (e.g. "RATE_LIMIT_EXCEEDED").
        message: Human-readable error message.
        details: Optional dict with additional error context.
        status: HTTP status code (default 400).

    Returns:
        A Flask Response with JSON error body and the given HTTP status.
    """
    error_obj = {
        "code": code,
        "message": message,
    }
    if details is not None:
        error_obj["details"] = details

    response = jsonify({
        "success": False,
        "data": None,
        "error": error_obj,
    })
    response.status_code = status
    return response
