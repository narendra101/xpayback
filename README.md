# User Registration

## Overview

User Registration using FastAPI, Postgress, MongoDB.

## Prerequisites

Before you start, make sure you have the following installed:

- [PgAdmin](https://www.pgadmin.org/) - PostgreSQL administration and management tool.
- [MongoDB](https://www.mongodb.com/) - MongoDB database.
- [MongoDB Compass](https://www.mongodb.com/products/compass) - MongoDB GUI.
- [Python](https://www.python.org/) - Python programming language.

## Setup and Check

1. Clone the repository:

   ```
   git clone https://github.com/narendra101/xpayback.git
   cd xpayback
   ```

2. Create a virtual environment:

    ```
    python -m venv venv
    ```

3. Activate virtualenv
    ```
    .\venv\Scripts\activate
    ```    

4. Install requirements
    ```
    pip install -r requirements.txt
    ```

5. give required creadentials, for postgress user password in db*.py files.
5. Check Test1
    ```
    uvicorn server1:app --reload
    ```

6. Check Test2
    ```
    uvicorn server2:app --reload
    ```

7. Check output [here](http://loclahost:7000/docs)