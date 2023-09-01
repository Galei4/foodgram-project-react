
### Опиание проекта.
Сайт Foodgram, «Продуктовый помощник». Это онлайн-сервис и API для него. Сервис на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Foodgram - позволяет:

- Просматривать все рецепты
- Подписываться на авторов
- Фильровать рецепты по тэгам
- Добавлять рецепты в избранное
- Добавлять рецепты в список покупок
- Создавать, удалять и редактировать собственные рецепты
- Скачивать список покупок в виде txt файла

## Проект доступен по ссылке:

```
- http://62.84.123.176/
- http://62.84.123.176/admin/
- http://62.84.123.176/api/docs/
```

## Учетная запись администратора:

```
- логин: user
- почта: user@user.ru 
- пароль: qwerW345
```

## Учетная запись пользователя:

```
- логин: malay
- почта: test2@yandex.ru 
- пароль: qwerw345
```
## Инструкции по установке
***- Склонируйте репозиторий:***
```
git clone git@github.com:Galei4/foodgram-project-react.git
```

***- Установите и активируйте виртуальное окружение:***
```
python3 -m venv venv
```
***- Зайдите в папку backend'a***
```
cd backend
```
 
***- Установите зависимости для работы приложения из файла requirements.txt:***
```
pip install -r requirements.txt
```

***- Примените миграции:***
```
python3 manage.py migrate
```

***- В папке с файлом manage.py выполните команду для запуска локально:***
```
python3 manage.py runserver
```
***- Локально Документация доступна по адресу:***
```
http://127.0.0.1/api/docs/ или http://localhost/api/docs
```
## Деплой на сервер:  
Подключитесь к своему серверу:
```
ssh username@server_ip
```

Обновите существующие пакеты:
```
sudo apt update
```

Установите докер:
```
sudo apt install docker.io
```

Загрузите файл Docker Compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Установите пермишены для запуска Docker Compose:
```
sudo chmod +x /usr/local/bin/docker-compose
```

Создайте необходимые папки
```
mkdir infra
mkdir docs
```

Перенесите необходимые файлы на сервер
```
scp docker-compose.yml username@server_ip:/home/username/infra/
scp nginx.conf username@server_ip:/home/username/infra/
scp .env username@server_ip:/home/username/infra/
scp openapi-schema.yml username@server_ip:/home/username/docs/
scp redoc.html username@server_ip:/home/username/docs/
```

Пример файла .env
```
DB_ENGINE=вид БД
DB_NAME=имя БД
POSTGRES_USER=юзер БД
POSTGRES_PASSWORD=пароль БД
DB_HOST=хост
DB_PORT=5432
TOKEN=
```

### Собираем контейнерыы:

Из папки infra/ разверните контейнеры при помощи docker-compose:
```
docker-compose up -d --build
```
Выполните миграции:
```
docker-compose exec backend python manage.py migrate
```
Создайте суперпользователя:
```
winpty docker-compose exec backend python manage.py createsuperuser
```
Соберите статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```
Наполните базу данных ингредиентами и тегами. Выполняйте команду из дериктории где находится файл manage.py:
```
docker-compose exec backend python manage.py import_ingredients

```

## Автор проекта:  
Линар Галеев [```Galei4```](https://github.com/Galei4)  
