FROM node:10-alpine

RUN apk add --no-cache --virtual .pipeline-deps readline linux-pam \
  && apk add bash sudo shadow curl python3 python3-dev py3-pip gcc musl-dev libffi-dev openssl-dev \
  && pip3 install --upgrade pip setuptools wheel \
  && pip3 install poetry awscli \
  && apk del .pipeline-deps


LABEL "com.azure.dev.pipelines.agent.handler.node.path"="/usr/local/bin/node"

CMD [ "node" ]
