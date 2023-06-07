# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim

EXPOSE 8000

ENV \
    # Keeps Python from generating .pyc files in the container
    PYTHONDONTWRITEBYTECODE=1 \
    # Turns off buffering for easier container logging
    PYTHONUNBUFFERED=1 \
    # PIP
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Flask
    FLASK_APP=webapp


RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential \
        default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install poetry 

COPY ./poetry.lock ./pyproject.toml ./
WORKDIR /app
COPY . /app

RUN poetry config virtualenvs.create false && \ 
    poetry install

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "web_project.wsgi"]
