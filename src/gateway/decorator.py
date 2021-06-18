from functools import wraps


def inject_organization():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            orga_uuid = request.headers.get("x-orga")
            response = await f(request, orga=orga_uuid, *args, **kwargs)
            return response

        return decorated_function

    return decorator
