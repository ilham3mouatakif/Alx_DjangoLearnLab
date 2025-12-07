# Nginx Configuration for HTTPS

This configuration ensures that your Django application is served securely over HTTPS using Nginx.

## Prerequisites
- A domain name pointing to your server.
- SSL/TLS certificates (e.g., from Let's Encrypt).

## Configuration Example

Save this to `/etc/nginx/sites-available/library_project`:

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    # Redirect all HTTP requests to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # SSL Certificates
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # SSL Protocols and Ciphers (Modern configuration)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";

    # HSTS Header (already handled by Django, but good redundancy)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/project/static/;
    }

    location /media/ {
        alias /path/to/your/project/media/;
    }
}
```

## Applying Changes
1.  Link the configuration:
    ```bash
    sudo ln -s /etc/nginx/sites-available/library_project /etc/nginx/sites-enabled/
    ```
2.  Test configuration:
    ```bash
    sudo nginx -t
    ```
3.  Restart Nginx:
    ```bash
    sudo systemctl restart nginx
    ```
