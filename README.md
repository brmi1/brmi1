# Клонируем репозиторий
```
git clone https://github.com/brmi1/brmi1.git
```

# Устанаваливаем необходимые пакеты
```
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv python3-dev mariadb-client mariadb-server default-libmysqlclient-dev build-essential pkg-config nginx
sudo mariadb-secure-installation
```

# Настраиваем базу данных
```
sudo mysql -u root -p
> CREATE DATABASE django_upload;
> CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'password';
> GRANT ALL PRIVILEGES ON django_upload.* TO 'django_user'@'localhost';
> FLUSH PRIVILEGES;
> EXIT;
```

# Создаем .env файл с ключами:
- SECRET_KEY
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT

# Создаем и активируем виртуальное окружение
```
python3 -m venv venv
source venv/bin/activate
```

# Устанавливаем необходимые библиотеки
```
pip install django dotenv mysqlclient uwsgi
```

# Выполняем миграции
```
python manage.py migrate
```

# Настраиваем uWSGI
```
sudo mkdir -p /etc/uwsgi/sites /run/uwsgi
sudo chown -R www-data:www-data /run/uwsgi
```

```
sudo nano /etc/uwsgi/sites/brmi1.ini
```

```
[uwsgi]
project = brmi1
base = /home/brmi1

chdir = %(base)
home = %(base)/venv
module = %(project).wsgi:application

master = true
processes = 4
threads = 2

socket = /run/uwsgi/brmi1.sock
chmod-socket = 660
vacuum = true
die-on-term = true
env = DJANGO_SETTINGS_MODULE=brmi1.settings
```

```
sudo nano /etc/systemd/system/uwsgi.service
```

```
[Unit]
Description=uWSGI Emperor service
After=network.target

[Service]
User=www-data
Group=www-data
ExecStart=/home/brmi1/venv/bin/uwsgi --emperor /etc/uwsgi/sites
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

# Активируем и запускаем службы
```
sudo systemctl daemon-reload
sudo systemctl start uwsgi
sudo systemctl enable uwsgi
```

# Создаем конфигурацию nginx
```
sudo nano /etc/nginx/sites-available/brmi1
```

```
server {
    listen 80;
    server_name 92.255.110.225;

    location = /uploader/icons/favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/brmi1/uploader/static/;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/run/uwsgi/brmi1.sock;
    }
}
```

# Запускаем службы
```
sudo ln -s /etc/nginx/sites-available/brmi1 /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```