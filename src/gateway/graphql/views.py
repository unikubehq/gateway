from urllib.parse import urljoin

import jwt
import requests
from requests.exceptions import HTTPError
from sanic import response
from sanic.request import Request
from sanic.response import BaseHTTPResponse, json, text
from sanic.views import HTTPMethodView

import settings
from gateway.base import OrganizationScopedView


class GraphQLView(OrganizationScopedView):
    async def post(self, request: Request, orga: str) -> BaseHTTPResponse:  # noqa
        """Retrieve information for an organization

        :type orga: UUID of user's current organization
        :param request: Sanic request object.
        :returns: HTTPResponse
        """
        # enrich ...
        request.headers["x-orga"] = orga
        url = settings.APOLLO_GQL_URL
        if request.query_string:
            url += f"?{request.query_string}"

        # ... and proxy request
        r = requests.post(url, data=request.body, headers=request.headers,)
        return response.raw(r.content)


class GraphQLSchemaView(HTTPMethodView):
    async def get(self, request: Request) -> BaseHTTPResponse:  # noqa
        url = settings.APOLLO_GQL_URL
        body = {
            "operationName": "IntrospectionQuery",
            "variables": {},
            "query": "query IntrospectionQuery { __schema { queryType { name } mutationType { name } "
            "subscriptionType { name } types { ...FullType } directives { name description  "
            " locations args {  ...InputValue   } }  }}fragment FullType on __Type {  kind  name "
            " description  fields(includeDeprecated: true) { name    description    args {    "
            "  ...InputValue    }    type {      ...TypeRef    }    isDeprecated    deprecationReason  }"
            "  inputFields {    ...InputValue  }  interfaces {    ...TypeRef  }  "
            "enumValues(includeDeprecated: true) {    name    description    isDeprecated  "
            "  deprecationReason  }  possibleTypes {    ...TypeRef  }}fragment InputValue on __InputValue "
            "{  name  description  type {    ...TypeRef  }  defaultValue}fragment TypeRef on __Type "
            "{  kind  name  ofType { kind name  ofType {  kind  name  ofType { kind  name ofType { "
            " kind  name  ofType {kind name ofType {  kind  name  ofType {kind name   } } } } } } }}",
        }

        # ... and proxy request
        r = requests.post(url, json=body)
        return response.raw(r.content)


class TokenDebugView(HTTPMethodView):
    async def get(self, request: Request) -> BaseHTTPResponse:  # noqa
        try:
            token_raw = request.headers["x-forwarded-access-token"]
            token = jwt.decode(token_raw, options={"verify_signature": False})
        except:
            token_raw = None
            token = None
        if token:
            payload = {
                "token_raw": token_raw,
                "token": token,
            }
        else:
            payload = {
                "headers": dict(request.headers),
                "cookies": request.cookies,
                "query": request.query_string,
            }
        return json(payload, indent=2)


class ManifestView(HTTPMethodView):
    async def get(self, request: Request, path: str) -> BaseHTTPResponse:  # noqa
        # this directly passes to manifest service
        if settings.MANIFEST_SVC_URL:
            r = requests.get(urljoin(settings.MANIFEST_SVC_URL, path), data=request.body, headers=request.headers,)
            return response.raw(r.content, headers=r.headers, status=r.status_code)
        else:
            return text("Backend service not available", status=500)


class UploadView(HTTPMethodView):
    async def post(self, request: Request, path: str) -> BaseHTTPResponse:
        path_split = path.split("/")
        port = 8082
        service = path_split[0]
        service_path = "/".join(path_split[1:])
        try:
            r = requests.post(f"http://{service}:{port}/{service_path}", data=request.body, headers=request.headers,)
            r.raise_for_status()
        except HTTPError:
            return text("Error", status=r.status_code)
        else:
            return response.raw(r.content, headers=r.headers, status=r.status_code)
