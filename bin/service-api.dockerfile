FROM python:3.7-alpine

RUN apk update && \
 apk add libpq postgresql-dev build-base && \
 apk add --no-cache git openssh && \
 apk add --virtual .build-deps gcc musl-dev && \
 apk --purge del .build-deps

RUN pip install -U pip
COPY requirements.frozen.pip /tmp/requirements.pip
RUN pip install -r /tmp/requirements.pip

ENV PYTHONPATH=/opt/application/chat

COPY bin/run.sh /entrypoint/run.sh
RUN chmod -R 755 /entrypoint/
ENV PATH /entrypoint:$PATH

WORKDIR /opt/application

CMD ["/entrypoint/run.sh"]

