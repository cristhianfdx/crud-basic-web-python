FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # Translations dependencies
  && apk add gettext \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  && apk add postgresql-client \

  && apk add curl wget bash

RUN pip install --upgrade pip

RUN addgroup -S django \
    && adduser -S -G django django

#RUN rm /bin/sh && ln -s /bin/bash /bin/sh
#
#RUN mkdir /usr/local/nvm
#
#ENV NVM_DIR /usr/local/nvm
#ENV NODE_VERSION 12.16.3
#
#RUN curl --silent -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash

# install node and npm
#RUN source $NVM_DIR/nvm.sh \
#    && nvm install $NODE_VERSION

# add node and npm to path so the commands are available
#ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
#ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

#RUN cd /app/frontend && npm install \
#    && npm run build && cd && ls

# Requirements are installed here to ensure they will be cached.
RUN mkdir requirements
COPY ./requirements.txt /requirements
RUN pip install --no-cache-dir -r /requirements/requirements.txt \
    && rm -rf /requirements

COPY ./compose/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
RUN chown -R django /entrypoint

COPY ./compose/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown -R django /start

COPY . /app
RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]