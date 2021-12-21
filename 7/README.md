# TLS CONF

In this lab, we gonna to secure our web apps. 

We need to generate our certificates by openssl lib:
`openssl req -x509 -newkey rsa:4096 -keyout vorlov.com.key -out vorlov.com.crt -sha256 -days 365`

Then we need to install these certs in our nginx configuration. Nginx configuration:
```
server {
    listen 80;
    listen [::]:80;
    server_name vorlov.com;
    return 302 https://$server_name$request_uri;
}

server {

    # SSL configuration

    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    ssl_certificate         /etc/ssl/custom_vorlov.com/vorlov.com.crt;
    ssl_certificate_key     /etc/ssl/custom_vorlov.com/vorlov.com.key;
    ssl_prefer_server_ciphers on;
    ssl_protocols TLSv1.2 TLSv1.3;

    root /var/www/vorlov.com;
    server_name vorlov.com;

    location / {
        index index.html;
    }
}
```

In this configuration we see path to generated certificates, and we are redirecting the http traffic to https. 
Also, we define that we support only tls 1.2 and tls 1.3, tls lower versions won't be supported.