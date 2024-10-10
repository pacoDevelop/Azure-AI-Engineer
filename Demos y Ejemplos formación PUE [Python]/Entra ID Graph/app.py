import msal
import requests
import json

# Configuración de la aplicación
CLIENT_ID = "<Id Application>"
CLIENT_SECRET = "<Secret Application>"
TENANT_ID = "<Id Tenant>"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

# Crear la aplicación confidencial para autenticarse
app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

# Obtener el token


def get_token():
    result = None
    result = app.acquire_token_for_client(SCOPES)

    if "access_token" in result:
        return result['access_token']
    else:
        print("Error al obtener el token:", result.get("error_description"))
        return None


token = get_token()

if token:
    print("Token:", token)

    # Listado de usuarios mediante un cliente HTTP
    print("\nListado de usuarios usando HTTP Client:\n")
    url = "https://graph.microsoft.com/v1.0/users"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data_json = response.json()
        users = data_json.get("value", [])

        for user in users:
            print(
                f" -> {user.get('displayName')} - {user.get('userPrincipalName')}")
    else:
        print(f"Error {response.status_code}: {response.text}")

    # Listado de usuarios usando Graph SDK
    print("\nListado de usuarios usando Graph SDK:\n")

    from msgraph.core import GraphClient
    graph_client = GraphClient(credential=app)

    users_response = graph_client.get("/users")
    users_list = users_response.json().get("value", [])

    for user in users_list:
        print(f" -> {user.get('displayName')} {user.get('userPrincipalName')}")
else:
    print("No se pudo obtener el token de autenticación.")
