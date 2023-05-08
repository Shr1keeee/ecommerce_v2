# DJANGO, NGINX, POSTGRESQL, GUNICORN on Ubuntu 20.04

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
    $ sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
    
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
    $ python manage.py runserver
    
    В адресной строке ввести: 127.0.0.1:8000
```
### Структура:
![struct](https://user-images.githubusercontent.com/107879305/236841909-78ed3398-fff1-49bb-a28a-0ca2359ee13b.png)

### Демонстрация:
![test (1)-min](https://user-images.githubusercontent.com/107879305/236841515-dd734896-0f03-4c95-b26d-e1219eb4af63.gif)

