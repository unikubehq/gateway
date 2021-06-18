import os

from sanic import Sanic
from sanic_cors import CORS

import settings
from gateway.routes import setup_routes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "version.txt")) as v_file:
    VERSION = v_file.read()

try:
    import sentry_sdk
    from sentry_sdk.integrations.sanic import SanicIntegration

    if settings.SENTRY_ENVIRONMENT:
        sentry_release = VERSION
        sentry_sdk.init(integrations=[SanicIntegration()], release=sentry_release)
except ImportError:
    sentry_sdk = SanicIntegration = None


app = Sanic(__file__, strict_slashes=False)

setup_routes(app)
CORS(app)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=settings.PORT, auto_reload=settings.AUTO_RELOAD, workers=settings.WORKERS,
    )
