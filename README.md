
# E-commerce API

API dedicada para uma solução ecommerce

***Read Me em construção***
## Installation

Create environment and activate
```bash
python3 -m venv venv && . /venv/bin/activate
```
Install the project dependencies
```bash
pip install -r requirements.txt
```



## API Reference

- /users

    Get user data
    ```http
    GET /api/users/  *Login Required*
    ```
    Create an user
    ```http
    POST /api/users/
    ```
    Partial Update
    ```http
    PATCH /api/users/  *Login Required*
    ```

    Update
    ```http
    PUT /api/users/  *Login Required*
    ```

    Delete
    ```http
    DELETE /api/users/  *Login Required*
    ```

- /products

    Get all products
    ```http
    GET /api/products/  *Login Required*
    ```
    Get product

    ```http
    GET /api/products/<slug>/
    ```

    Create a product
    ```http
    POST /api/products/  *Login Required*
    ```

    Update one field of the product
    ```http
    PATCH /api/products/<slug>/  *Login Required*
    ```

    Update all fields of the product
    ```http
    PUT /api/products/<slug>/  *Login Required*
    ```

    Delete the product
    ```http
    DELETE /api/products/<slug>/  *Login Required*
    ```
