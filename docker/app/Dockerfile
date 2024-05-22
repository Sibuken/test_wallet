# syntax=docker/dockerfile:1.0.0-experimental
FROM python:3.11-slim AS compile-image

ARG POETRY_EXPORT_EXTRA_ARGS=""

RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ build-essential default-libmysqlclient-dev \
    git openssh-client pkg-config \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*


RUN mkdir -m 700 /root/.ssh; \
  touch -m 600 /root/.ssh/known_hosts; \
  ssh-keyscan github.com bitbucket.com > /root/.ssh/known_hosts && eval $(ssh-agent) && echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

WORKDIR /opt/venv
RUN python -m venv /opt/venv && /opt/venv/bin/pip install --upgrade pip && /opt/venv/bin/pip install --no-cache-dir httpx poetry

COPY ./pyproject.toml ./poetry.lock ./
RUN --mount=type=ssh /opt/venv/bin/poetry export --without-hashes ${POETRY_EXPORT_EXTRA_ARGS} > requirements.txt \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


FROM python:3.11-slim AS runtime-image

RUN apt-get update && apt-get install -y --no-install-recommends gettext default-libmysqlclient-dev  \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

COPY ./app /app
COPY --from=compile-image /opt/venv /opt/venv

COPY ./docker/app/start.sh /start.sh
COPY ./docker/app/gunicorn_conf.py /gunicorn_conf.py
COPY ./docker/app/prestart.sh /prestart.sh
RUN chmod +x /start.sh



ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
EXPOSE 80

CMD ["/start.sh"]
