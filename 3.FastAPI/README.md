# A small tasks management API using FastAPI

## How to run

### Create a virtual env and install packages

```
python -m venv .venv
source .venv/bin/activate
pip install -u pip
pip install -r requirements.txt
```

### Run uvicorn server
```
uvicorn app:app --reload --port 8000
```

## How to run tests
```
python -m pytest
```

