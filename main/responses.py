def format_api_response(
    content=None, status=200, message="Request success", error=False
):

    response = {"status": status, "message": message}

    if content:
        response["body"] = content

    if error:
        response["error"] = True
    return response
