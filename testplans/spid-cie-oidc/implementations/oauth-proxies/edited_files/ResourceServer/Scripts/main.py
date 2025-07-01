from fastapi import FastAPI, Depends, HTTPException, status, Header, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from datetime import datetime, timezone
from fastapi.responses import HTMLResponse
import httpx
from jose import jwt
import constants as CONST
import os
app = FastAPI()
JWKS = None

# OAuth2 Bearer Token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=CONST.TOKEN_ENDPOINT)

# Web Origin of Jinja. He will substitute dynamically both the url and the username
templates = Jinja2Templates(directory="/webOrigin")

async def get_jwks():
    global JWKS
    if JWKS is None:
        async with httpx.AsyncClient(verify=CONST.CA_SYSTEM_VERIFICATION_PATH) as client:
            response = await client.get(CONST.JWKS_ENDPOINT)
            response.raise_for_status()
            JWKS = response.json()
    return JWKS

async def decode_jwt(token: str):
    try:
        # Get the header first (without verifying) to extract 'kid'
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        if not kid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing 'kid' header")

        # Fetch JWKS
        jwks = await get_jwks()

        # Find the key
        key = next((k for k in jwks["keys"] if k["kid"] == kid), None)
        if not key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Public key not found for 'kid'")

        # Decode the jwt using the key
        decoded = jwt.decode(
            token,
            key,
            algorithms=[key["alg"]],
            audience=CONST.ACF_CLIENT_ID,  # Client ID expected as...
            issuer=CONST.ISSUER_URL,  # Issuer expected as...
            options={"verify_at_hash": False},
        )

        return decoded
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token verification failed: {str(e)}")

# Token introspection function
async def introspect_token_ID(token):
    async with httpx.AsyncClient(verify=CONST.CA_SYSTEM_VERIFICATION_PATH) as client:
        print(f"Doing introspection to {CONST.INTROSPECTION_ENDPOINT} for ID token")
        response = await client.post(
            CONST.INTROSPECTION_ENDPOINT,
            data={"token": token},
            auth=(CONST.RESOURCESERVER_CLIENT_ID, CONST.RESOURCESERVER_CLIENT_SECRET), # The introspection endpoint is authenticated by standard!
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error contacting introspection endpoint")

        token_data = response.json()
        if CONST.DEBUG_RESOURCESERVER_PRINT_TOKENS:
            print(f"Info on the ID token received: {token_data}")
        if not token_data.get("active"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or inactive token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data

# Auth dependency that validates token, scope, and expiration
async def require_token_ID(token: str = Depends(oauth2_scheme)):
    token_data = await introspect_token_ID(token)
    # introspection allows to check expiration and active
    exp = token_data.get("exp")
    if not exp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing expiration (exp)")
    now = datetime.now(timezone.utc).timestamp()
    if now > exp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    token_decoded = await decode_jwt(token)
    if CONST.DEBUG_RESOURCESERVER_PRINT_TOKENS:
        print(f"decoded token: {token_decoded}")
    return token_data


async def get_access_token_from_header(x_forwarded_access_token: str = Header(None, alias="x-forwarded-access-token")): # Header into which the oauth2proxy places the access token
    if not x_forwarded_access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Access Token")
    return x_forwarded_access_token


# Token introspection function for the access token
async def introspect_token_ACCESS(token):
    async with httpx.AsyncClient(verify=CONST.CA_SYSTEM_VERIFICATION_PATH) as client:
        print(f"Doing introspection to {CONST.INTROSPECTION_ENDPOINT} for ACCESS token")
        response = await client.post(
            CONST.INTROSPECTION_ENDPOINT,
            data={"token": token},
            auth=(CONST.RESOURCESERVER_CLIENT_ID, CONST.RESOURCESERVER_CLIENT_SECRET), # The introspection endpoint is authenticated by standard!
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error contacting introspection endpoint")

        token_data = response.json()
        if CONST.DEBUG_RESOURCESERVER_PRINT_TOKENS:
            print(f"Info on the ACCESS token received: {token_data}")
        if not token_data.get("active"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or inactive access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data


# Updated Auth dependency for the Access Token validation with introspection
async def require_token_ACCESS(access_token: str = Depends(get_access_token_from_header)):
    # Introspect the access token to validate if it's active
    token_data = await introspect_token_ACCESS(access_token)

    # If token is valid, proceed to decode
    try:
        decoded_token = await decode_jwt(access_token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Token verification failed: {str(e)}")

    if CONST.DEBUG_RESOURCESERVER_PRINT_TOKENS:
        print(f"Decoded ACCESS token: {decoded_token}")

    # Check expiration
    exp = decoded_token.get("exp")
    if not exp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access Token missing expiration (exp)")

    now = datetime.now(timezone.utc).timestamp()
    if now > exp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access Token has expired")

    # Check for required scopes
    scope_str = decoded_token.get("scope", "")
    scopes = scope_str.split()
    if CONST.DEBUG_RESOURCESERVER_PRINT_TOKENS:
        print(f"Access Token scopes: {scopes}")

    required_scopes = set(CONST.RESOURCESERVER_REQUIREDSCOPES)
    missing_scopes = required_scopes - set(scopes)
    if missing_scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing required scopes: {', '.join(missing_scopes)}",
        )

    return decoded_token

# Secured route
@app.get(CONST.RESOURCESERVER_BASE_RESOURCE_ENDPOINT+CONST.RESOURCESERVER_SECURE_ENDPOINT, response_class=HTMLResponse)
async def secure_endpoint(
    request: Request,
    id_token_data: dict = Depends(require_token_ID),
    access_token_data: dict = Depends(require_token_ACCESS)
):
    template_path = "/webOrigin/secret.html.j2"

    # Check if the Jinja2 template file exists
    if not os.path.exists(template_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secure template not found")
    # Render and return the HTML response
    return templates.TemplateResponse("secret.html.j2", {
        "request": request,
        "username": id_token_data["username"],
        "logout_endpoint": CONST.LOGOUT_ENDPOINT,
    })

# Healthcheck used as debug during the development
@app.get(CONST.RESOURCESERVER_BASE_RESOURCE_ENDPOINT+CONST.RESOURCESERVER_HEALTH_ENDPOINT)
async def healthcheck(request: Request):
    file_path = "/webOrigin/healthcheck.html"

    if CONST.DEBUG_RESOURCESERVER_HEALTHCHECK_PRINTREQUEST:
        print("------- FULL REQUEST DEBUG -------")
        print(f"URL: {request.url}")
        print(f"Method: {request.method}")
        print("Headers:")
        for name, value in request.headers.items():
            print(f"  {name}: {value}")
        print("------- END REQUEST DEBUG -------")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Healthcheck file not found")

    # Serve the file as HTML directly in the browser
    with open(file_path, 'r') as file:
        content = file.read()

    return HTMLResponse(content=content)