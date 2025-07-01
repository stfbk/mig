import os
import ast

# FIXED STATUS CODES
HTTP_OK = 200
HTTP_INTERNAL_SERVER_ERROR = 500

# ENDPOINTS USED BY THE RESOURCE SERVER

INTROSPECTION_ENDPOINT = os.environ.get(
    "INTROSPECTION_ENDPOINT",
    "https://keycloak/realms/myrealm/protocol/openid-connect/token/introspect"
)
TOKEN_ENDPOINT = os.environ.get(
    "TOKEN_ENDPOINT",
    "https://keycloak/realms/myrealm/protocol/openid-connect/token"
)
JWKS_ENDPOINT = os.environ.get(
    "JWKS_ENDPOINT",
    "https://keycloak:8112/realms/mytestrealm/protocol/openid-connect/certs"
)

ISSUER_URL = (
    "ISSUER_URL",
    "https://keycloak.client.oauth2.fbktesting.fbk.eu:8111/realms/mytestrealm"
)

# LOGIN TO THE INSPECTION ENDPOINT

RESOURCESERVER_CLIENT_ID = os.environ.get(
    "RESOURCESERVER_CLIENT_ID",
    "ResourceServerClientIdForIntrospect"
)
RESOURCESERVER_CLIENT_SECRET = os.environ.get(
    "RESOURCESERVER_CLIENT_SECRET",
    "RUYGFS2k4lt4Gn65S18kgUTf5XD96C6aFqIMwn4iW1g"
)

# ENDPOINTS PROVIDED

RESOURCESERVER_SECURE_ENDPOINT = os.environ.get(
    "RESOURCESERVER_SECURE_ENDPOINT",
    "/secure"
)
RESOURCESERVER_HEALTH_ENDPOINT = os.environ.get(
    "RESOURCESERVER_HEALTH_ENDPOINT",
    "/healthcheck"
)

RESOURCESERVER_BASE_RESOURCE_ENDPOINT = os.environ.get(
    "RESOURCESERVER_BASE_RESOURCE_ENDPOINT",
    "/resource"
)

# Verification of tokens

RESOURCESERVER_REQUIREDSCOPES = ast.literal_eval(
    os.environ.get(
        "RESOURCESERVER_REQUIREDSCOPES",
        []
    )
)

ACF_CLIENT_ID = os.environ.get(
    "ACF_CLIENT_ID",
    "ACF_PUBCLIENT_test"
)

# Logout

LOGOUT_ENDPOINT = os.environ.get(
    "LOGOUT_ENDPOINT",
    "https://oauth2proxy.client.oauth2.fbktesting.fbk.eu:8001/oauth2/sign_out"
)

# DEBUG

DEBUG_RESOURCESERVER_PRINT_TOKENS = ast.literal_eval(
    os.environ.get(
        "DEBUG_RESOURCESERVER_PRINT_TOKENS",
        "False"
    )
)
DEBUG_RESOURCESERVER_HEALTHCHECK_PRINTREQUEST=ast.literal_eval(
    os.environ.get(
        "DEBUG_RESOURCESERVER_HEALTHCHECK_PRINTREQUEST",
        "False"
    )
)


# Folder where it is possible to find the certificate

CA_SYSTEM_VERIFICATION_PATH="/etc/ssl/certs/ca-certificates.crt"