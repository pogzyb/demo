FROM python:3.9-alpine3.12 as stage

COPY requirements.txt /tmp/requirements.txt

RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:${PATH}

RUN apk update \
    && pip3 install --upgrade pip \
    && pip3 install -r /tmp/requirements.txt

FROM python:3.9-alpine3.12 as build

COPY --from=stage /opt/venv /opt/venv
ENV PATH=/opt/venv/bin:${PATH}
ENV HOME=/search-service
ENV PYTHONPATH=${PYTHONPATH}:/${HOME}

WORKDIR ${HOME}

COPY app app
COPY config.py config.py
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE ${PORT}
CMD ["entrypoint.sh"]
