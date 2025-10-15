FROM python:3.11 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /tmp/

RUN poetry self add poetry-plugin-export
RUN poetry add python-multipart
RUN poetry install --no-root
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --with=dev

FROM python:3.11

ENV PYTHONPATH=/src
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /src

COPY --from=requirements-stage /tmp/requirements.txt ./requirements.txt

RUN apt update \
 && apt upgrade -y \
 && apt install --no-install-recommends --no-install-suggests -y gcc libc6-dev \
 && apt-get autoremove -y \
 && apt-get clean -y \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

COPY ./alembic.ini /app/alembic.ini

RUN mkdir -p /src/storage/media \
    && mkdir -p /src/logs
