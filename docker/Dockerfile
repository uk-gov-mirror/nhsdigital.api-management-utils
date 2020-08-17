FROM node:current-alpine

LABEL "com.azure.dev.pipelines.agent.handler.node.path"="/usr/local/bin/node"

RUN apk update && apk upgrade && \
    apk add --no-cache bash && \
    apk add --no-cache sudo && \
    apk add --no-cache shadow && \
    apk add --no-cache gcc && \
    apk add --no-cache musl-dev && \
    apk add --no-cache openssl-dev && \
    apk add --no-cache libffi-dev && \
    apk add --no-cache git && \
    apk add --no-cache make && \
    apk add --no-cache rsync && \
    apk add --no-cache docker && \
    apk add --no-cache python3-dev && \
    apk add --no-cache py3-virtualenv

RUN pip3 install --upgrade pip setuptools wheel && pip install poetry

COPY pyproject.toml /

# This allows us to de-facto share virtualenvs between utils and service
# this should speed up 
RUN poetry config virtualenvs.create false

RUN poetry install

CMD ["node"]
