from datetime import datetime
from functools import wraps

from flask import jsonify, request


def validate_datetime(field_name, format="%Y-%m-%dT%H:%M:%S"):
    """
    Decorator to validate the datetime field in the request body.
    :param field_name: Name of the field to validate (e.g., 'reminder_date')
    :param format: The expected date format (default is ISO 8601).
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            date_str = data.get(field_name)

            if date_str:
                try:
                    # Try to parse the date
                    reminder_date = datetime.strptime(date_str, format)

                    # Optionally, check if the date is not in the past
                    if reminder_date < datetime.now():
                        return jsonify(
                            {"error": f"{field_name} must be a future date."}
                        ), 400
                except ValueError:
                    # If the date format is wrong
                    return jsonify(
                        {"error": f"Invalid {field_name}. Expected format: {format}"}
                    ), 400

            return f(*args, **kwargs)

        return decorated_function

    return decorator
