from rest_framework.views import exception_handler
import copy


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if not response:
        return response

    # Now add the custom data to the response.
    formatted_data = {}

    if response.get("detail", 0):
        message = response.data["detail"]
        del response.data["detail"]
    else:
        message = "Your request can't be perfomed"

    if response is not None:
        body = response.data
        formatted_data["body"] = body

    formatted_data["message"] = message
    formatted_data["status"] = response.status_code
    formatted_data["error"] = True

    response.data = formatted_data

    return response
