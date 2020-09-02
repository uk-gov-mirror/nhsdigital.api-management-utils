FROM ubuntu:20.04

LABEL "com.azure.dev.pipelines.agent.handler.node.path"="/usr/local/bin/node"

# Update and get global reqs
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y default-jre default-jdk software-properties-common wget \
  curl build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
  libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils \
  tk-dev libffi-dev liblzma-dev python-openssl git

# Node install
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

# Python install
RUN curl https://pyenv.run | SHELL=bash bash

# Having env issues here
RUN $(~/.pyenv/bin/pyenv init -)
RUN ~/.pyenv/bin/pyenv install 3.8.2 && ~/.pyenv/bin/pyenv global 3.8.2
RUN which python
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m install poetry

# Install python requirements
COPY pyproject.toml /
# RUN poetry config virtualenvs.create false # Install all in one env
RUN poetry install

CMD ["node"]
