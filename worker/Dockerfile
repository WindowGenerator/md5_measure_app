FROM python:3.9.12-slim-bullseye as python-base

############ ENV CONFIG ############

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.13 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN groupadd --system services && useradd --system -g services worker

############ PRE-INSTALL ############

FROM python-base as builder-base

RUN apt-get update ; \
    apt-get install -y \
		curl \
	    gcc \
		libc6-dev \
		libssl-dev \
		libpq-dev \
		build-essential

############ INSTALL POETRY ############
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev --no-root

RUN mkdir -p /opt/app
ENV APP_DIR /opt/app

############ RUN LINTER AND TESTS ############

FROM python-base as development

ENV BOT_ENV=development
WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
# RUN poetry install

COPY src $APP_DIR/src/

############ FINISH ############

FROM python-base as production

ENV BOT_ENV=production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

RUN mkdir -p /opt/app
ENV APP_DIR /opt/app

WORKDIR $APP_DIR

COPY src $APP_DIR/src/

USER worker
