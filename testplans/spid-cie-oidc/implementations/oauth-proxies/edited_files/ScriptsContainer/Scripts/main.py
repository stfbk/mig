import requests
import time
import constants as CONST

def check_keycloak():
    try:
        # Step 1: Readiness health check
        health_url = f"{CONST.KEYCLOAK_URL}/health/ready"
        health_response = requests.get(health_url)

        if health_response.status_code == CONST.HTTP_OK:
            try:
                health_data = health_response.json()
                if health_data.get("status") == "UP":
                    print("Keycloak is healthy and ready.")

                    # Step 2: Check server info endpoint
                    serverinfo_url = f"{CONST.KEYCLOAK_URL}/admin/serverinfo"
                    serverinfo_response = requests.get(serverinfo_url)

                    if serverinfo_response.status_code == CONST.HTTP_UNAUTHORIZED:
                        print("Keycloak is running but requires authentication for /admin/serverinfo.")
                        return True
                    elif serverinfo_response.status_code == CONST.HTTP_OK:
                        print("Keycloak /admin/serverinfo accessible without auth (unexpected).")
                        return True
                    else:
                        print(f"Unexpected status from /admin/serverinfo: {serverinfo_response.status_code}")
                else:
                    print(f"Keycloak health check failed: status != 'UP' (got: {health_data.get('status')})")
            except ValueError:
                print("Health check response is not valid JSON.")

        else:
            print(f"Keycloak health check failed. Status: {health_response.status_code}, Body: {health_response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Keycloak: {e}")

    return False

def get_admin_token():
    url = f"{CONST.KEYCLOAK_URL}/realms/{CONST.KEYCLOAK_ADMIN_REALM}/protocol/openid-connect/token"
    data = {
        "client_id": CONST.ADMIN_CLIENT_ID,
        "username": CONST.KEYCLOAK_ADMIN,
        "password": CONST.KEYCLOAK_ADMIN_PASSWORD,
        "grant_type": "password"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

def create_realm(token, realm_name):
    url = f"{CONST.KEYCLOAK_URL}/admin/realms"
    headers = {"Content-Type": "application/json","Authorization": f"Bearer {token}"}
    data = {"realm": realm_name, "enabled": True}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == CONST.HTTP_CREATED:
        print(f"Realm '{realm_name}' created successfully.")
    else:
        print(f"Failed to create realm: {response.text}")

def create_client_scope(token, realm_name, scope_name, optional):
    url = f"{CONST.KEYCLOAK_URL}/admin/realms/{realm_name}/client-scopes"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    scope_data = {
        "name": f"{scope_name}",
        "protocol": "openid-connect",
        "attributes": {
            "include.in.token.scope": "true",
            "display.on.consent.screen": "true" if optional else "false",
            "consent.screen.text": f"Allow access to {scope_name}"
        }
    }

    response = requests.post(url, json=scope_data, headers=headers)

    if response.status_code == CONST.HTTP_CREATED:
        print(f"Client scope '{scope_name}' created successfully.")
    elif response.status_code == CONST.HTTP_CONFLICT:  # Already exists
        print(f"Client scope '{scope_name}' already exists.")
    else:
        print(f"Failed to create client scope '{scope_name}': {response.status_code} - {response.text}")

def delete_realm(token, realm_name):
    url = f"{CONST.KEYCLOAK_URL}/admin/realms/{realm_name}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(url, headers=headers)

    if response.status_code == CONST.HTTP_NOCONTENT:
        print(f"Realm '{realm_name}' deleted successfully.")
    else:
        print(f"Failed to delete realm: {response.text}")


def create_client_authorizationCodeFlow(token, realm_name, client_id, scope_names, as_optionals, give_scopes):
    url = f"{CONST.KEYCLOAK_URL}/admin/realms/{realm_name}/clients"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    default_scopes = ["email", "profile"]
    optional_scopes = []

    # Process each scope based on the flags
    for scope, optional, give in zip(scope_names, as_optionals, give_scopes):
        if give:
            if optional:
                optional_scopes.append(scope)
            else:
                default_scopes.append(scope)

    client_data = {
        "clientId": client_id,
        "enabled": True,
        "publicClient": True, # Cannot store a client secret securely. Necessary for the use case of ACF
        "standardFlowEnabled": True, # Enabling ACF
        "implicitFlowEnabled": False,
        "directAccessGrantsEnabled": False,
        "serviceAccountsEnabled": True, # Enabling token introspection. This is needed for the redirect.
        "authorizationServicesEnabled": False,
        "redirectUris": [
            f"{CONST.ACF_OAUTH2_PROXY_REDIRECT_URL}"
        ],
        "attributes": {
            "pkce.code.challenge.method": CONST.ACF_HASH_ALGORITHM,
            "access.token.signed.response.alg": f"{CONST.KEYCLOAK_ACCESS_TOKEN_SIGNED_RESPONSE_ALG}",
            "id.token.signed.response.alg": f"{CONST.KEYCLOAK_ACCESS_TOKEN_SIGNED_RESPONSE_ALG}",
        },
        "adminUrl": "",
        "webOrigins": ["*"],
        "protocol": "openid-connect",
        "fullScopeAllowed": False,
        "defaultClientScopes": default_scopes,
        "optionalClientScopes": optional_scopes
    }
    response = requests.post(url, json=client_data, headers=headers)
    if response.status_code != CONST.HTTP_CREATED:
        print(f"Failed to create client: {response.text}")
        print(f"Tried to assign default scopes: {default_scopes}")
        print(f"Tried to assign optional scopes: {optional_scopes}")
        return
    print(f"Non-Confidential client '{client_id}' created successfully.")
    print(f"Default scopes: {default_scopes}")
    print(f"Optional scopes: {optional_scopes}")
    # Fetch client UUID
    client_uuid = get_client_uuid(token, realm_name, client_id)
    if not client_uuid:
        print("Failed to retrieve client UUID.")
        return

    # Add audience protocol mapper
    if not add_audience_mapper(token, realm_name, client_uuid, client_id):
        print("Failed to adjust audience protocol mapper.")
        return

    print("Audience protocol mapper adjusted successfully.")

def get_client_uuid(token, realm_name, client_id):
    url = f"{CONST.KEYCLOAK_URL}/admin/realms/{realm_name}/clients"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != CONST.HTTP_OK:
        print("Failed to fetch clients.")
        return None

    clients = response.json()
    client = next((c for c in clients if c['clientId'] == client_id), None)
    if not client:
        print(f"Client ID '{client_id}' not found.")
        return None

    return client['id']

def add_audience_mapper(token, realm_name, client_uuid, client_id):
    mapper_url = f"{CONST.KEYCLOAK_URL}/admin/realms/{realm_name}/clients/{client_uuid}/protocol-mappers/models"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    audience_mapper = {
        "name": "audience-mapper",
        "protocol": "openid-connect",
        "protocolMapper": "oidc-audience-mapper",
        "consentRequired": False,
        "config": {
            "included.client.audience": client_id,
            "id.token.claim": "true",
            "access.token.claim": "true",
        }
    }

    response = requests.post(mapper_url, json=audience_mapper, headers=headers)
    if response.status_code != CONST.HTTP_CREATED:
        print(f"Failed to add audience protocol mapper for client '{client_id}': {response.text}")
        return False

    print(f"Audience protocol mapper added successfully for client '{client_id}'.")
    return True

def create_client_clientCredentialsFlow(token, realm_name, client_id,client_secret,scope_names, as_optionals, give_scopes):

    url = f"{CONST.KEYCLOAK_URL}/admin/realms/{realm_name}/clients"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    default_scopes = []
    optional_scopes = []

    # Process each scope based on the flags
    for scope, optional, give in zip(scope_names, as_optionals, give_scopes):
        if give:
            if optional:
                optional_scopes.append(scope)
            else:
                default_scopes.append(scope)

    client_data = {
        "clientId": client_id,
        "enabled": True,
        "publicClient": False,  # The client is confidential! Otherwise, cannot use this type of grant
        "standardFlowEnabled": False,
        "implicitFlowEnabled": False,
        "directAccessGrantsEnabled": False,
        "serviceAccountsEnabled": True,  # Enable machine-to-machine
        "authorizationServicesEnabled": False,
        "redirectUris": [], # no need?
        "webOrigins": ["*"],
        "protocol": "openid-connect",
        "fullScopeAllowed": False,
        "secret": client_secret,
        "attributes": {
            "access.token.signed.response.alg": f"{CONST.KEYCLOAK_ACCESS_TOKEN_SIGNED_RESPONSE_ALG}",
            "id.token.signed.response.alg": f"{CONST.KEYCLOAK_ACCESS_TOKEN_SIGNED_RESPONSE_ALG}",
        },
        "defaultClientScopes": default_scopes,
        "optionalClientScopes": optional_scopes
    }

    # Send a POST request to create the client
    response = requests.post(url, json=client_data, headers=headers)

    if response.status_code == CONST.HTTP_CREATED:
        print(f"Confidential client '{client_id}' created successfully.")
        print(f"Default scopes: {default_scopes}")
        print(f"Optional scopes: {optional_scopes}")
    else:
        print(f"Failed to create client: {response.text}")
        print(f"Tried to assign default scopes: {default_scopes}")
        print(f"Tried to assign optional scopes: {optional_scopes}")


def create_user(token, realm_name, username, email, first_name, last_name, password):
    # Construct the URL for the Keycloak Admin API to create a user
    url = f"{CONST.KEYCLOAK_URL}/admin/realms/{realm_name}/users"

    # Prepare headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"  # Bearer token to authenticate the request
    }

    # Prepare the data for the new user
    user_data = {
        "username": username,
        "enabled": True,
        "email": email,
        "emailVerified": True,
        "firstName": first_name,
        "lastName": last_name,
        "credentials": [
            {
                "type": "password",
                "value": password,
                "temporary": False
            }
        ]
    }

    # Send the POST request to create the user
    response = requests.post(url, json=user_data, headers=headers)

    # Check the response and print out the result
    if response.status_code == CONST.HTTP_CREATED:
        print(f"User '{username}' created successfully.")
    else:
        print(f"Failed to create user: {response.status_code}, {response.text}")

def get_client_info(token, realm, client_uuid):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Fetch client details
    get_url = f"{CONST.KEYCLOAK_URL}/admin/realms/{realm}/clients/{client_uuid}"
    response = requests.get(get_url, headers=headers)

    if response.status_code != CONST.HTTP_OK:
        print(f"Failed to fetch client details: {response.status_code} {response.text}")
        return None

    return response.json()

def enable_intospection_resourceServer(token, realm_name, client_id):
    # Get the internal UUID
    client_uuid = get_client_uuid(token, realm_name, client_id)
    if not client_uuid:
        print("Failed to retrieve client UUID.")
        return
    client_data = get_client_info(token,realm_name,client_uuid)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    # Update client attributes to enable introspection
    if "attributes" not in client_data:
        client_data["attributes"] = {}

    client_data["attributes"]["introspection_enabled"] = "true"

    # Send PUT request to update the client
    url = f"{CONST.KEYCLOAK_URL}/admin/realms/{realm_name}/clients/{client_uuid}"
    put_response = requests.put(url, headers=headers, json=client_data)

    if put_response.status_code == CONST.HTTP_NOCONTENT:
        print(f"Client introspection enabled successfully for {client_id}.")
    else:
        print(f"Failed to update client: {put_response.status_code} {put_response.text}")


def print_keys(token, realm_name):
    # URL to get the keys of the specified realm
    url = f"{CONST.KEYCLOAK_URL}/admin/realms/{realm_name}/keys"

    # Set headers for authentication
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)

        # Check if the response is successful
        if response.status_code == CONST.HTTP_OK:
            keys = response.json()

            if not keys:
                print(f"No keys found for realm '{realm_name}'.")
            else:
                print(f"Keys for realm '{realm_name}':")
                print(keys)
        else:
            print(f"Failed to fetch keys for realm '{realm_name}': {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Keycloak: {e}")

if __name__ == "__main__":
    while not check_keycloak():
        print(f"Retrying in {CONST.KEYCLOAK_HEALTH_CHECK_INTERVAL} seconds...")
        time.sleep(CONST.KEYCLOAK_HEALTH_CHECK_INTERVAL)
    try:
        token = get_admin_token()
        if CONST.ACTION == "C":
            create_realm(token, CONST.KEYCLOAK_NEW_REALM)
            for name,option in zip(CONST.EXTRA_SCOPE_NAMES,CONST.EXTRA_SCOPE_AS_OPTIONALS):
                create_client_scope(token,CONST.KEYCLOAK_NEW_REALM,name,option)
            create_client_authorizationCodeFlow(token,CONST.KEYCLOAK_NEW_REALM,CONST.ACF_CLIENT_ID,CONST.EXTRA_SCOPE_NAMES,CONST.EXTRA_SCOPE_AS_OPTIONALS,CONST.EXTRA_SCOPE_GIVE)
            create_user(token,CONST.KEYCLOAK_NEW_REALM,CONST.ACF_USER_USERNAME,CONST.ACF_USER_EMAIL,CONST.ACF_USER_FIRSTNAME,CONST.ACF_USER_LASTNAME,CONST.ACF_USER_PASSWORD)
            create_client_clientCredentialsFlow(token,CONST.KEYCLOAK_NEW_REALM,CONST.CCF_CLIENT_ID,CONST.CCF_CLIENT_SECRET,CONST.EXTRA_SCOPE_NAMES,CONST.EXTRA_SCOPE_AS_OPTIONALS,CONST.EXTRA_SCOPE_GIVE)
            create_client_clientCredentialsFlow(token,CONST.KEYCLOAK_NEW_REALM,CONST.RESOURCESERVER_CLIENT_ID,CONST.RESOURCESERVER_CLIENT_SECRET,[],[],[])
            enable_intospection_resourceServer(token,CONST.KEYCLOAK_NEW_REALM,CONST.RESOURCESERVER_CLIENT_ID)

            if CONST.DEBUG_CONFIGURER_PRINTJTWKEYS:
                print_keys(token,CONST.KEYCLOAK_NEW_REALM)
        else:
            delete_realm(token, CONST.KEYCLOAK_NEW_REALM)
    except requests.exceptions.RequestException as e:
        print(f"Error during script: {e}")

