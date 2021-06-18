from urllib.parse import urljoin

from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Sanic
from sanic.request import Request
from sanic.response import text, BaseHTTPResponse, html

import settings
from gateway.graphql import GraphQLView, TokenDebugView, ManifestView, UploadView, GraphQLSchemaView


def prefix_url(url: str) -> str:
    if not settings.PUBLIC_API_URL_PREFIX:
        return url
    prefix = settings.PUBLIC_API_URL_PREFIX
    return urljoin(prefix, url)


async def welcome(request: Request) -> BaseHTTPResponse:  # noqa
    return text("Welcome to Unikube Service Gateway.")


env = Environment(loader=PackageLoader("gateway", "templates"), autoescape=select_autoescape(["html"]))


async def playground(request: Request) -> BaseHTTPResponse:  # noqa
    template = env.get_template("playground.html")
    return html(template.render())


def setup_routes(app: Sanic):
    app.add_route(welcome, prefix_url(""))
    app.add_route(playground, prefix_url("playground/"))
    app.add_route(GraphQLView.as_view(), prefix_url("graphql/"))
    app.add_route(GraphQLSchemaView.as_view(), prefix_url("schema.json"))
    app.add_route(ManifestView.as_view(), prefix_url("manifests/<path:path>"))
    app.add_route(UploadView.as_view(), prefix_url("upload/<path:path>"))
    app.add_route(TokenDebugView.as_view(), prefix_url("token/"))
