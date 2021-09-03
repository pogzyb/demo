FROM python:3.9-alpine3.12

ENV HOME=/search-service
ENV PYTHONPATH=${PYTHONPATH}:/${HOME}
COPY requirements.txt /tmp/requirements.txt

RUN apk update && apk add bash \
    && pip3 install --upgrade pip \
    && pip3 install -r /tmp/requirements.txt

WORKDIR ${HOME}

COPY app app
COPY config.py config.py
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE ${PORT}
CMD ["entrypoint.sh"]
