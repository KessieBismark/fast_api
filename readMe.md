# create a virtual env.
    python -m venv .venv 
 
# activate
    source .venv/bin/activate

# install fast api
    pip install "fastapi[all]"

# see all installed pips
    pip freeze

# run api
    uvicorn main:app   

# reload 
    uvicorn main:app --reload
     uvicorn app.main:app --reload

# install postgres plugin
    pip install "psycopg[binary]" 
    pip install passlib
    pip install bcrypt
    pip install python-jose cryptography


# token = JWT token

# install alembic to handle database migration
    pip install alembic
    alembic revision -m "initial create" 

# create dependency file
     pip freeze > requirements.txt

# to install dependency
    pip install -r requirement.txt

