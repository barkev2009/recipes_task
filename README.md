# recipes_task

REST API for working with recipes' and users' database (scroll down for Russian version).

#### Technology stack:
* Language: Python 3.6
* Database: PostgreSQL 13.3
* Main libraries:
  - aiohttp
  - sqlalchemy
  - pytest

**Postman** is advised to be installed for better experience 
of testing the API.

To start working with the API please follow the steps:
1. Install requirements with command ```pip install -r requirements.txt```
2. Initialize the database **recipes_db** and all tables with the help of 
```recipes/recipe_tables/init_db.py``` and
```recipes/recipe_tables/create_tables.py```. 
The name of the database can be changed in ```recipes/config/config.yaml```.
3. Admin configurations for API have been already set for you in 
```recipes/config/config.yaml```. You are free to alter them.
4. Start ```recipes/aiohttp_server/main.py``` and feel free to test the API, 
either through ```recipes/tests/tests.py``` or via **Postman** app.
>All configurations for working with PostgreSQL and API
>are available in ```recipes/config/config.yaml```.


The API detailed description can be accessed via ```openapi.json```. 
Check it out [here](https://editor.swagger.io/) for better document view.

![screenshot of sample](https://i0.wp.com/marketplace-cdn.atlassian.com/files/images/3a8b0e69-dbfa-474f-9eb3-101d1449087e.png?resize=650,400)

# recipes_task

REST API для работы с базой данных пользователей и рецептов.

Для более удобного тестирования и работы с API рекомендуется установить **Postman**.

Для начала работы с API следуйте, пожалуйста, инструкции ниже:
1. Установите библиотеки через команду ```pip install -r requirements.txt```
2. Инициализируйте базу данных **recipes_db** и все таблицы с помощью
```recipes/recipe_tables/init_db.py``` и . ```recipes/recipe_tables/create_tables.py```
Название БД может быть изменено в ```recipes/config/config.yaml```.
3. Параметры администратора для API уже были настроены для Вас в
```recipes/config/config.yaml```. Можете их при желании изменить.
4. Запустите ```recipes/aiohttp_server/main.py``` и тестируйте API либо через 
```recipes/tests/tests.py```, либо через приложение **Postman**.
>Все конфигурации для работы с PostgreSQL и API
>доступны в файле ```recipes/config/config.yaml```.

Подробное описание API смотрите в файле ```openapi.json```. 
Проследуйте по [ссылке](https://editor.swagger.io/) для более наглядного интерфейса.
