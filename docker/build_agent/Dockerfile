FROM node:14-alpine

COPY pyproject.toml /

RUN apk add --no-cache --virtual .pipeline-deps readline linux-pam \
  && apk add bash make sudo shadow curl python3 python3-dev py3-pip gcc musl-dev libffi-dev openssl-dev openjdk11 openjdk11-jre rsync \
  && pip3 install --upgrade pip setuptools wheel \
  && pip3 install poetry awscli \
  && ln -s /usr/bin/python3 /usr/bin/python \
  && apk del .pipeline-deps

LABEL "com.azure.dev.pipelines.agent.handler.node.path"="/usr/local/bin/node"

CMD [ "node" ]
