from sanic import exceptions
from sanic.request import Request
from sanic.views import HTTPMethodView

from gateway.decorator import inject_organization


class OrganizationScopedView(HTTPMethodView):
    def organization_id_scope(request: Request, *args, **kwargs):  # noqa
        uuid = request.headers.get("x-orga") or kwargs.get("uuid")
        if uuid is None:
            raise exceptions.InvalidUsage("Please add the x-orga header to your request")
        return uuid

    decorators = [inject_organization()]
