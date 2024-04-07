#!/usr/bin/env bash
# script that sets up web servers for the deployment of web_static
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

# Configure Nginx
sudo bash -c 'cat > /etc/nginx/sites-available/web_static' <<EOF
server {
    listen 80;
    listen [::]:80 default_server;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm;
    }
}
EOF

sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

sudo service nginx restart
