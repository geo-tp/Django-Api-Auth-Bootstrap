def format_api_response(content=None, status=200, message="", error=False):
    """
    Harmonize api json response : {status: 200, body: {...}, message: "Request Success", error: false}
    """
    response = {"status": status, "message": message}

    if content:
        response["body"] = content

    if error:
        response["error"] = True

    else:
        response["error"] = False

    return response
