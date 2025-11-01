import os

c = get_config()

# Use DockerSpawner for isolated containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ.get('DOCKER_NOTEBOOK_IMAGE', 'jupyter-notebook-server')
c.DockerSpawner.network_name = os.environ.get('DOCKER_NETWORK_NAME', 'jupyter-backend_default')

# CRITICAL: Stateless - remove containers immediately after use
c.DockerSpawner.remove = True
c.DockerSpawner.remove_containers = True

# Per-user resource limits (production safe)
c.DockerSpawner.mem_limit = '1G'
c.DockerSpawner.cpu_limit = 0.5
c.DockerSpawner.cpu_guarantee = 0.25

# NO persistent storage - everything is temporary
c.DockerSpawner.volumes = {}

# Hub configuration
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'  # Internal docker hostname

# ENABLE NAMED SERVERS for multiple concurrent sessions per user
c.JupyterHub.allow_named_servers = True

# Authentication: DummyAuthenticator allows any password (stateless)
c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'
c.DummyAuthenticator.password = 'anything'

# CORS headers for mobile app - allow all origins
c.JupyterHub.tornado_settings = {
    'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    }
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
c.JupyterHub.inactive_servers_timeout = 1800

# Graceful shutdown
c.JupyterHub.shutdown_on_logout = True

# Base URL configuration
c.JupyterHub.base_url = '/'
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000

# Allow origin from anywhere (for mobile)
c.JupyterHub.allow_origin = '*'
