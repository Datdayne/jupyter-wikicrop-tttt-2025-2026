import os
from oauthenticator.generic import GenericOAuthenticator
from dockerspawner import DockerSpawner

c = get_config()

# --- CẤU HÌNH QUAN TRỌNG NHẤT (MẠNG) ---
c.JupyterHub.hub_ip = '0.0.0.0'
c.DockerSpawner.hub_connect_url = "http://jupyterhub:8081"

c.DockerSpawner.network_name = 'my-jupyterhub_default' 

# --- CẤU HÌNH DOCKER SPAWNER ---
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = "jupyter/minimal-notebook:latest"


# --- CẤU HÌNH KEYCLOAK (OAUTH) ---
c.JupyterHub.authenticator_class = GenericOAuthenticator

keycloak_url = os.environ.get('KEYCLOAK_URL')
realm = os.environ.get('KEYCLOAK_REALM')

c.GenericOAuthenticator.client_id = 'jupyterhub'
c.GenericOAuthenticator.client_secret = os.environ.get('KEYCLOAK_CLIENT_SECRET')

c.GenericOAuthenticator.authorize_url = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/auth"
c.GenericOAuthenticator.token_url = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/token"
c.GenericOAuthenticator.userdata_url = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/userinfo"

c.GenericOAuthenticator.login_service = "Keycloak"
c.GenericOAuthenticator.username_claim = "preferred_username"
c.GenericOAuthenticator.scope = ["openid", "profile", "email"]

c.GenericOAuthenticator.enable_auth_state = True
c.LocalAuthenticator.create_system_users = True
c.Authenticator.allow_all = True

# Timeout
c.Spawner.start_timeout = 600
c.Spawner.http_timeout = 600