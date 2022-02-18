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
flask-cms-admin is only for back end and you can connect to the front end with rest api,wich can be accesed by following endpoint:

*note: the rest api prefix is `/api/v1`*


**GET**
1. ```bash
    GET /
    ```
    and
    ```bash
    GET /blogs
    ```
    get all blogs

2. ```bash
    GET /blogs?page={n}
    ```
    get blogs by page(5 blog per page)  
    `n` = page number

3. ```bash
   GET /read/<param>
   ```
   `param` can be blog id or blog slug/blog title with `-` instead of spaces

4. ```bash
   GET /t?page={n}
   ```
   get tags by page if page query string is not none it will return 10 tags per page else it will return all tags

5. ```bash
   GET /t/<tag>?page={n}
   ```
   get blogs categorize by tags and if page query is not none it will return 10 blogs per page else it will return all blogs categorize by tags


## Creating content
if you want to start creating content you need login first wich by default the route is `/login`,and then you need to inserting username and password you make when running command `add_admin`,after the login success you can start writing content by clicking `new blog` button

note: in this project the default editor is tinymce,but maybe you can change later whatever you want