FROM node:10-alpine

RUN apk add --no-cache --virtual .pipeline-deps readline linux-pam \
  && apk add bash sudo shadow curl python3 python3-dev py3-pip gcc musl-dev libffi-dev openssl-dev \
  && pip3 install --upgrade pip setuptools wheel \
  && pip3 install poetry \
  && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
  && unzip awscliv2.zip \
  && sudo ./aws/install \
  && apk del .pipeline-deps


LABEL "com.azure.dev.pipelines.agent.handler.node.path"="/usr/local/bin/node"

CMD [ "node" ]
