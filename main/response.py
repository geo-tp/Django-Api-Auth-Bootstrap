def format_api_response(
    content=None,
    status=200,
    message="",
    error=False,
    pagination=False,
    next_=False,
    previous=False,
    page_count=False,
):
    """
    Harmonize api json response :
    {
        status: 200,
        body: {...},
        message: "Request Success",
        error: False,
        pagination: True,
        next: URL,
        previous: URL,
        page_count: 4
    }
    """
    response = {"status": status, "message": message}
    response["error"] = True if error else False

    if pagination and page_count:
        response["pagination"] = True
        response["next"] = next_
        response["previous"] = previous
        response["page_count"] = page_count

    else:
        response["pagination"] = False

    if content:
        response["body"] = content

    return response
