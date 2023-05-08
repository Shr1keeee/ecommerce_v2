# DJANGO, NGINX, POSTGRESQL, GUNICORN on Ubuntu 20.04

### Архитектура :
![struct](https://user-images.githubusercontent.com/107879305/236865724-7e440a93-1122-4fa9-8926-39f37deca9a9.png)

![test (1)-min](https://user-images.githubusercontent.com/107879305/236841515-dd734896-0f03-4c95-b26d-e1219eb4af63.gif)

1. Клонирование git репозитория.
```
- Создаем директорию, где будет располагаться наше приложение: 
    $ mkdir myapp $$ cd myapp
- Предоставляем текущему пользователю все права для работы с файлами директории: 
    $ sudo chown -R $USER:$USER  
- Клонируем репозиторий: 
    $ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
```
2. Установка python и postgresql 

```
- Установка:
    $ sudo apt update
    $ sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
    
- Создание базы данных и пользователя:
    Подключение к psql:
        $ sudo -u postgres psql
    
    Создание БД и пользователя:
    1. CREATE DATABASE e_store;
    2. CREATE USER estoreadmindb WITH PASSWORD 'admin777';
    3.
    ALTER ROLE estoreadmindb SET client_encoding TO 'utf8';
    ALTER ROLE estoreadmindb SET default_transaction_isolation TO 'read committed';
    ALTER ROLE estoreadmindb SET timezone TO 'UTC';
    4. GRANT ALL PRIVILEGES ON DATABASE e_store TO estoreadmindb;
    
- Подключение к БД: 
    $ psql -h localhost -U estoreadmindb -W e_store
```

3. Cоздание виртуального окружения.
```
- Переходим в директорию с приложением /home/user/myapp/app, создаем и активируем venv:
    $ python3 -m venv *enter_name_venv*
    $ source *enter_name_venv*/bin/activate 
```

4. Установка необходимых инструментов из requirements.txt
```
 $ pip install -r requirements.txt
```
5. Создание таблиц в БД и суперпользователя Django:
```
- Миграция:
     $ python manage.py migrate 
 
 - Создание суперпользователя:
    $ python manage.py createsuperuser
```
6. Запуск сервера.
```
-Создать исключение для порта 8000 с помощью следующей команды:
    $sudo ufw allow 8000
        
-Запуск сервера:
    $ python manage.py runserver
    
- В адресной строке ввести: 127.0.0.1:8000
```

## Настройка GUNICORN

1. Создание файлов сокета и служебных файлов systemd для Gunicorn
```
- Тестирование способности Gunicorn обслуживать проект:
    $ gunicorn --bind 127.0.0.1:8000 ecommerce.wsgi
    
- Создание файла сокета systemd для Gunicorn:
    $ sudo nano /etc/systemd/system/gunicorn.socket
    
    Заполнить файл /etc/systemd/system/gunicorn.socket:
    [Unit]
    Description=gunicorn socket

    [Socket]
    ListenStream=/run/gunicorn.sock

    [Install]
    WantedBy=sockets.target

- Cоздайте служебного файла systemd для Gunicorn:
    $ sudo nano /etc/systemd/system/gunicorn.service
    
    Заполнить файл /etc/systemd/system/gunicorn.service:
    [Unit]
    Description=gunicorn daemon
    Requires=gunicorn.socket
    After=network.target

    [Service]
    User=shrikeeee
    Group=www-data
    WorkingDirectory=/home/shrikeeee/projects/ecommerce #/home/user/projectdir/app
    ExecStart=/home/shrikeeee/projects/store_env/bin/gunicorn \ #/home/user/projectdir/app/venv
              --access-logfile - \
              --workers 3 \
              --bind unix:/run/gunicorn.sock \
              ecommerce.wsgi:application #/home/user/projectdir/app/appname.wsgi

    [Install]
    WantedBy=multi-user.target

- Запустите и активируйте сокет Gunicorn:
    $ sudo systemctl start gunicorn.socket
    $ sudo systemctl enable gunicorn.socket
```
2. Проверка файла сокета Gunicorn
```
- Проверка состояния процесса:
    $ sudo systemctl status gunicorn.socket
    
- Проверка наличие файла gunicorn.sock в /run:
    $ file /run/gunicorn.sock

- Проверка жруналов сокета Gunicorn:
    $ sudo journalctl -u gunicorn.socket
    
- Перезагрузка демона и процесса Gunicorn:
    $ sudo systemctl daemon-reload
    $ sudo systemctl restart gunicorn
```
## Настройка Nginx как прокси для Gunicorn

1. Создание нового серверного блока в каталоге Nginx
```
- Открываем новый блок в sites-available:
    $ sudo nano /etc/nginx/sites-available/ecommerce
    
- Заполнить и сохранить файл /etc/nginx/sites-available/ecommerce:
    server {
    listen 80;
    server_name 127.0.0.1;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/shrikeeee/projects/ecommerce; #/home/user/projectdir/app
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
    }

- Активируем файл, привязав его к каталогу sites-enabled:
  $ sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled

- Тестирование конфигурации NGINX:
    $ sudo nginx -t

- Если ошибок нет, перезапускаем Nginx:
    $ sudo systemctl restart nginx

- Открываем 80 порт для приема обычного трафика:
    $ sudo ufw allow 'Nginx Full'
```

