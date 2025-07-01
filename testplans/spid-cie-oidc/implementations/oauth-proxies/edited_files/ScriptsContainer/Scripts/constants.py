import os
import ast

# FIXED ONES!

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NOCONTENT = 204
HTTP_UNAUTHORIZED = 401
HTTP_CONFLICT = 409
ACTION = "C" # Just for debugging purposes... Creating with C and deleting with something else.
ADMIN_CLIENT_ID = "admin-cli"
KEYCLOAK_ADMIN_REALM = "master"

# AuthorizationCodeFlow

ACF_HASH_ALGORITHM = "S256"
ACF_CLIENT_ID = os.environ.get(
    "ACF_CLIENT_ID",
    "ACF_PUBCLIENT_test"
)
ACF_USER_FIRSTNAME = "ACF_firstname"
ACF_USER_LASTNAME = "ACF_lastname"
ACF_USER_PASSWORD = os.environ.get(
    "ACF_USER_PASSWORD",
    "ACF_password"
)
ACF_USER_EMAIL = "ACF_email@test.com"
ACF_USER_USERNAME = os.environ.get(
    "ACF_USER_USERNAME",
    "ACF_username"
)
ACF_OAUTH2_PROXY_REDIRECT_URL = os.environ.get(
    "OAUTH2_PROXY_REDIRECT_URL",
    "http://oauth2-proxy:8001/oauth2-proxy/callback"
)

# CCF flow

CCF_CLIENT_ID = os.environ.get(
    "CCF_CLIENT_ID",
    "CCF_CONFCLIENT_test"
)
CCF_CLIENT_SECRET = os.environ.get(
    "CCF_CLIENT_SECRET",
    "RUYGFS2k4lt4Gn65S18kgUTf5XD96C6sCqIMwn4iW1g"
)

# Extra scope for testing purposes
EXTRA_SCOPE_AS_OPTIONALS = ast.literal_eval(
    os.environ.get(
        "EXTRA_SCOPE_AS_OPTIONALS",
        "[]"
    )
)
EXTRA_SCOPE_NAMES = ast.literal_eval(
    os.environ.get(
        "EXTRA_SCOPE_NAMES",
        "[]"
    )
)
EXTRA_SCOPE_GIVE = ast.literal_eval(
    os.environ.get(
        "EXTRA_SCOPE_GIVE",
        "[]"
    )
)

# KEYCLOAK
KEYCLOAK_ADMIN = os.environ.get(
    "KEYCLOAK_ADMIN",
    "admin"
)
KEYCLOAK_ADMIN_PASSWORD = os.environ.get(
    "KEYCLOAK_ADMIN_PASSWORD",
    "admin"
)
KEYCLOAK_NEW_REALM = os.environ.get(
    "KEYCLOAK_NEW_REALM",
    "mytestrealm"
)
KEYCLOAK_URL = os.environ.get(
    "KEYCLOAK_URL",
    "http://keycloak"
)
KEYCLOAK_ACCESS_TOKEN_SIGNED_RESPONSE_ALG = os.environ.get(
    "KEYCLOAK_ACCESS_TOKEN_SIGNED_RESPONSE_ALG",
    "none"
)
KEYCLOAK_HEALTH_CHECK_INTERVAL= int(
    os.environ.get(
        "KEYCLOAK_HEALTH_CHECK_INTERVAL",
        "60"
    )
)

# Resource server credentials

RESOURCESERVER_CLIENT_ID = os.environ.get(
    "RESOURCESERVER_CLIENT_ID",
    "ResourceServerClientIdForIntrospect"
)
RESOURCESERVER_CLIENT_SECRET = os.environ.get(
    "RESOURCESERVER_CLIENT_SECRET",
    "RUYGFS2k4lt4Gn65S18kgUTf5XD96C6aFqIMwn4iW1g"
)

# Debug

DEBUG_CONFIGURER_PRINTJTWKEYS=ast.literal_eval(
    os.environ.get("DEBUG_CONFIGURER_PRINTJTWKEYS","False")
)