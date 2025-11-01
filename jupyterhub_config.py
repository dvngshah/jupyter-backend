import os

c = get_config()

# Use DockerSpawner for isolated containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ.get('DOCKER_NOTEBOOK_IMAGE', 'jupyter-notebook-server')
c.DockerSpawner.network_name = os.environ.get('DOCKER_NETWORK_NAME', 'jupyter-backend_default')

# CRITICAL: Stateless - remove containers immediately after use
c.DockerSpawner.remove = True
c.DockerSpawner.remove_containers = True

# Per-user resource limits
c.DockerSpawner.mem_limit = '1G'
c.DockerSpawner.cpu_limit = 0.5
c.DockerSpawner.cpu_guarantee = 0.25

# NO persistent storage
c.DockerSpawner.volumes = {}

# Hub configuration
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'

# ENABLE NAMED SERVERS
c.JupyterHub.allow_named_servers = True

# Authentication
c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'
c.DummyAuthenticator.password = 'anything'

# ✅ FIXED: Enhanced CORS and WebSocket settings
c.JupyterHub.tornado_settings = {
    'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS, CONNECT, PATCH',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Credentials': 'true',
    },
    'ws_ping_interval': 30,
    'ws_ping_timeout': 10,
    'allow_origin_with_credentials': True,
    'max_buffer_size': 10_000_000,
}

# API service token for iOS app
c.JupyterHub.services = [
    {
        'name': 'ios-app',
        'api_token': os.environ.get('JUPYTERHUB_API_TOKEN', '658b70e1f2e36ea2b26a31b0ca3ac61400fe945731caf162daa2b804db76f7d0'),
        'admin': True
    }
]

# Auto-cleanup: stop idle servers after 30 minutes
c.JupyterHub.active_server_limit = 10  # ✅ FIXED: Use correct name (not inactive_servers_timeout)

# Graceful shutdown
c.JupyterHub.shutdown_on_logout = True

# Base URL configuration
c.JupyterHub.base_url = '/'
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000
