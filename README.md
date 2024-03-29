
<a name="readme-top"></a>


# Nginx HTTP Authentication

<!-- ABOUT THE PROJECT -->
## About The Project

This project provide a simple way to manage users and provide basic access control using HTTP basic authentication and nginx auth_request. 

Notes: this project current only support HTTP basic authentication which must be used with SSL.

## Installation

### Docker Compose
```yaml
services:
    http-basic-auth-request:
        image: ghcr.io/klementng/http-basic-auth-request:main
        container_name: http-basic-auth-request
        environment:
            - CONFIG_DIR=/config
            - CONFIG_PATH=/config/config.yml
            - USER_DB_PATH=/config/users.yml
            - LOG_LEVEL=INFO
            - FLASK_SESSION_COOKIE_DOMAIN=.example.com
        volumes:
            - /path/to/data:/config
        ports:
            - 9999:9999
        restart: unless-stopped
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage:

### Server Setup
Docker environmental variables:
<table>
  <tr>
    <th>Name</th>
    <th>Description</th>
    <th>Allowed values</th>
    <th>Default values</th>
  </tr>
  <tr>
    <td>CONFIG_DIR</td>
    <td>Working directory for storing configuration & data </td>
    <td>Any</td>
    <td>/config</td>
  </tr>

  <tr>
    <td>CONFIG_PATH</td>
    <td>Path to config file</td>
    <td>Any</td>
    <td>${CONFIG_DIR}/config.yml</td>
  </tr>
  <tr>
    <td>LOG_LEVEL</td>
    <td>Set Logging</td>
    <td>INFO, DEBUG, WARNING</td>
    <td>INFO</td>
  </tr>

  <tr>
    <td>FLASK_SESSION_COOKIE_DOMAIN</td>
    <td>Associated cookie domain</td>
    <td>Any</td>
    <td>-</td>
  </tr>

  <tr>
    <td>FLASK_*</td>
    <td>Flask app config</td>
    <td>Any</td>
    <td>-</td>
  </tr>

</table>  

### Managing Users
```bash
sudo docker exec -it http-basic-auth-request server.users add <username>
sudo docker exec -it http-basic-auth-request server.users edit <username>
sudo docker exec -it http-basic-auth-request server.users delete <username>
```

## Examples :

### Server
see [default.yml](examples/default.yml)

### Nginx
see [auth-request.conf](examples/auth-request.conf)
and [nginx.conf](examples/nginx.conf)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
