
### Project Description

Foodgram – Your Grocery Assistant is an online service with an accompanying API. It allows users to publish recipes, add others’ recipes to favorites, and subscribe to authors. Users can also create a shopping list of ingredients needed to cook selected recipes.

Foodgram allows users to:
	•	Browse all recipes
	•	Subscribe to authors
	•	Filter recipes by tags
	•	Add recipes to favorites
	•	Add recipes to the shopping list
	•	Create, delete, and edit personal recipes
	•	Download the shopping list as a .txt file

## Project is available at:

```
- http://158.160.31.98:9000/
- http://158.160.31.98:9000/admin/
- https://foodgramgaleev.hopto.org/
```

## Admin Account:

```
- Username: user  
- Email: user@user.ru  
- Password: qwerW345
```

User Account:

```
- Username: malay  
- Email: test2@yandex.ru  
- Password: qwerw345
```
## Installation Instructions
***- Clone the repository:***
```
git clone git@github.com:Galei4/foodgram-project-react.git
```

***- Create and activate a virtual environment:***
```
python3 -m venv venv
```
***- Navigate to the backend folder:***
```
cd backend
```
 
***- Install dependencies from requirements.txt:***
```
pip install -r requirements.txt
```

***- Apply database migrations:***
```
python3 manage.py migrate
```

***- To run the app locally, execute in the folder with manage.py:***
```
python3 manage.py runserver
```
***- Local API documentation is available at:***
```
http://127.0.0.1/api/docs/ или http://localhost/api/docs
```
## Deployment on Server:
Connect to your server:
```
ssh username@server_ip
```

Update packages:
```
sudo apt update
```

Install Docker:
```
sudo apt install docker.io
```

Download Docker Compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Grant permission to run Docker Compose:
```
sudo chmod +x /usr/local/bin/docker-compose
```

Create the necessary directories:
```
mkdir infra
mkdir docs
```

Transfer the required files to the server:
```
scp docker-compose.yml username@server_ip:/home/username/infra/
scp nginx.conf username@server_ip:/home/username/infra/
scp .env username@server_ip:/home/username/infra/
scp openapi-schema.yml username@server_ip:/home/username/docs/
scp redoc.html username@server_ip:/home/username/docs/
```

Example .env file:
```
DB_ENGINE=вид БД
DB_NAME=имя БД
POSTGRES_USER=юзер БД
POSTGRES_PASSWORD=пароль БД
DB_HOST=хост
DB_PORT=5432
TOKEN=
```

### Populating the Project:

Create a superuser:
```
winpty docker-compose exec backend python manage.py createsuperuser
```
Populate the database with ingredients and tags (run from the directory containing manage.py):
```
docker-compose exec backend python manage.py import_ingredients

```

## Project Author:
Linar Galeev [```Galei4```](https://github.com/Galei4)  
