# flask-cms-admin

a simple cms dashborad build using flask,just like a name this project is not a full cms because you need a front end display your content.

## How to run

clone this repo
```bash
git clone https://github.com/AlphaBeta1906/flask-cms-admin.git

cd flask-cms-admin
```

activate virtual environment
```bash
. venv/bin/activate
```

install dependencies
```bash
pip install -r requirements.txt
```

change project configuration in `cms/config.py`,especially the database uri
```python
...
SQLALCHEMY_DATABASE_URI = (
        "your_database_url"    
)
...
```

if database already configured now you can do the migration by running follwing command:
```bash
python manage.py migration
# yeah just a shorthand of flask migration command
```

and then add new admin by running command:
```bash
python manage.py add_admin
# a input will appear and you can insert your admin data(e.g:username,password,email)
```

now you can run the server by :
```bash
python manage.py dev
```
to enable live reload or
```bash
python wsgi.py
# i dont know why how to make template livereload
```
or just using
```bash
flask run
```

## Endpoint
flask-cms-admin is only for back end and you can connect to front end with rest api,wich can be accesed by following endpoint:

**GET**
1. ```bash
    GET /api/v1
    ```
    and
    ```bash
    GET /api/v1/blogs
    ```
    get all blogs

2. ```bash
    GET /api/v1/blogs?page={n}
    ```
    get blogs by page(5 blog per page)  
    `n` = page number
