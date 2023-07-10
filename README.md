## To run the server:
```bash
python server.py
```
## To add a new user:

```python
import requests
usename = "dummy"
#adds new user:
resp = requests.request(
    "POST",
    url="http://ec2-54-82-21-40.compute-1.amazonaws.com:8000/api/add-user",
    data={
        "username": usename
    },
)
print(resp.json())
```

## Important Note:
Frontend communicates with backend server via reverse proxies which are set up with nginx. Sample nginx file is as follows:
```conf

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log notice;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    keepalive_timeout   65;
    types_hash_max_size 4096;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

# Settings for a TLS enabled server.

    server {
        listen       443 ssl http2;
        listen       [::]:443 ssl http2;
        server_name  _;
        root         /usr/share/nginx/html;

        ssl_certificate "/etc/nginx/nginx-selfsigned.crt";
        ssl_certificate_key "/etc/nginx/nginx-selfsigned.key";
        
        location / {
		proxy_pass http://localhost:5173;
	    }
        location /api {
		proxy_pass http://127.0.0.1:8000; 
		client_max_body_size 10M;
       }
 
    }
}
```
Important part is as follows:
```
location /api {
    proxy_pass http://127.0.0.1:8000; 
    client_max_body_size 10M;
}
```
It handles the CORS problem that emerges when calling endpoints from frontend on the browser. Besides you hide api url from the browser as well ;)
