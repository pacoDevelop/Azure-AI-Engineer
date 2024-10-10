from flask import Flask, redirect, url_for, session, request
from msal import ConfidentialClientApplication
import requests

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia esto a una clave secreta segura

# Configuración de Microsoft Entra ID
CLIENT_ID = '<Tu_Cliente_ID>'
CLIENT_SECRET = '<Tu_Secreto_Cliente>'
TENANT_ID = '<Tu_Tenant_ID>'
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
REDIRECT_URI = 'http://localhost:5000/auth/redirect'
SCOPE = ['User.Read']  # Puedes ajustar los permisos según tus necesidades

# Crear una instancia de la aplicación confidencial
app_msal = ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)


##################################################
# Decorador para rutas protegidas
##################################################
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            # Si el usuario no está autenticado, redirigir a la página de login
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


##################################################
# Hacer una solicitud a Microsoft Graph para
# obtener información del usuario autenticado
##################################################
def get_user_info(token):
    graph_url = 'https://graph.microsoft.com/v1.0/me'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(graph_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {
            'name': data.get('displayName'),
            'email': data.get('mail') or data.get('userPrincipalName')
        }
    return None


##################################################
# Ruta para el servicio de autenticación
##################################################
@app.route('/login')
def login():
    # Crear URL de autenticación para Microsoft Entra ID
    auth_url = app_msal.get_authorization_request_url(SCOPE, redirect_uri=REDIRECT_URI)
    return redirect(auth_url)


@app.route('/auth/redirect')
def auth_redirect():
    # Obtener el código de autorización de la URL
    code = request.args.get('code')

    # Intercambiar el código por un token de acceso
    result = app_msal.acquire_token_by_authorization_code(code, scopes=SCOPE, redirect_uri=REDIRECT_URI)

    if 'access_token' in result:
        user_info = get_user_info(result['access_token'])
        session['user'] = user_info
        return redirect(url_for('index'))
    else:
        return f"Error al autenticarse: {result.get('error_description')}"


@app.route('/logout')
def logout():
    # Limpiar la sesión para cerrar la sesión del usuario
    session.clear()
    return redirect(f'{AUTHORITY}/oauth2/v2.0/logout?post_logout_redirect_uri=http://localhost:5000')


##################################################
# Ruta pública
##################################################
@app.route('/public')
def public():
    return 'Esta es una página pública. <a href="/login">Iniciar sesión</a>'


##################################################
# Ruta protegida (analiza la autenticación)
##################################################
@app.route('/')
def index():
    # Verificar si el usuario ya está autenticado
    if not session.get('user'):
        return redirect(url_for('login'))

    user = session['user']
    return f'Bienvenido, {user["name"]}! <a href="/logout">Cerrar sesión</a>'


##################################################
# Ruta protegida (requiere autenticación)
##################################################
@app.route('/protected')
@login_required
def protected():
    user = session['user']
    return f'Hola, {user["name"]}. Esta es una página protegida. <a href="/logout">Cerrar sesión</a>'


if __name__ == '__main__':
    app.run(debug=True)