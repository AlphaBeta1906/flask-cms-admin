# flask-cms-admin

a simple cms dashborad build using flask,just like a name this project is not a full cms because you need a front end display your content,flask-cms-admin is only for back end and you can connect to front end with rest api,wich can be accesed by following endpoint:

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
