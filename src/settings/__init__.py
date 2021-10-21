import os

AUTO_RELOAD = os.getenv("AUTO_RELOAD", "False").lower() in (
    "true",
    "t",
    "yes",
    "y",
    "1",
)

SENTRY_ENVIRONMENT = os.getenv("SENTRY_ENVIRONMENT", None)
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "t", "yes", "y", "1")
PORT = int(os.getenv("PORT", "8080"))
WORKERS = int(os.getenv("WORKERS", 4))

PUBLIC_API_URL_PREFIX = os.getenv("PUBLIC_API_URL_PREFIX", "")
SECRET = os.getenv("JWT_SECRET", "This is a big secret.")

APOLLO_HOST = os.getenv("APOLLO_HOST", "apollo")
APOLLO_PORT = os.getenv("APOLLO_PORT", "8090")
APOLLO_GQL_URL = f"http://{APOLLO_HOST}:{APOLLO_PORT}/"

GQL_TIMEOUT = int(os.getenv("GQL_TIMEOUT", "5"))

MANIFEST_SVC_URL = os.getenv("MANIFESTS_HTTP_PORT", "").replace("tcp://", "http://")
PROJECTS_SVC_URL = os.getenv("PROJECTS_HTTP_PORT", "").replace("tcp://", "http://")
ORGAS_SVC_URL = os.getenv("ORGAS_HTTP_PORT", "").replace("tcp://", "http://")
