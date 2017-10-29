# wechat_ebiz_helper

v0.1.0	released on 2017-09-04  
v0.2.0  released on 2017-09-07


## Conda Environment

Export
    > conda env export > environment.yml
Install
    > conda env create -f environment.yml
Update
    > conda env update -f environment.yml

## Possible Dependency Issues

* mysql_config
    > sudo yum install mysql-devel

* gcc
    > sudo yum install gcc

## SCP config.py to server
    > scp config.py hostname:/home/jingkun/app/wechat_ebiz_helper/app/config.py

## Setup nginx and gunicorn

1. install nginx
    > sudo yum install epel-release
    > sudo yum install nginx

    - nginx configuration
        Create /etc/nginx/sites-available and /etc/nginx/sites-enabled and then edit the `http` block inside /etc/nginx/nginx.conf and add this line

        include /etc/nginx/sites-enabled/*;

        and comment out default server {} block in /etc/nginx/nginx.conf
        of course all the files will be inside sites-available and then you create a symlink for them inside sites-enabled

        > touch /etc/nginx/sites-available/flask_settings
        > ln -s /etc/nginx/sites-available/flask_settings /etc/nginx/sites-enabled/flask_settings

    - edit `/etc/nginx/sites-enabled/flask_settings` file
```
server {
        location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
        }
}
```
    - `systemctl restart nginx`

2. install gunicorn in conda virtual env
    > pip install gunicorn

3. install mysql
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-centos-7

    - create new user
    > GRANT ALL PRIVILEGES ON dbTest.* To 'user'@'hostname' IDENTIFIED BY 'password';

    - grant remote access from certain ip
    > GRANT ALL PRIVILEGES
        ON database.*
        TO 'user'@'yourremotehost'
        IDENTIFIED BY 'newpassword';
