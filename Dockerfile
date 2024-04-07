# Use the latest Ubuntu image as base
FROM --platform=linux/amd64 ubuntu:latest

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-dev \
    python3-pip \
    postgresql-client

ADD requirements.txt /src/requirements.txt
ADD /src/settings.py /src/settings.py
ADD /src/app.py /src/app.py
ADD /src/client.py /src/client.py
ADD /src/crypto.py /src/crypto.py
ADD /src/errors.py /src/errors.py
ADD /src/jwt.py /src/jwt.py
ADD /src/sqlite_delegate.py /src/sqlite_delegate.py
ADD data/sqlite-chcs-delegate.db /src/data/sqlite-chcs-delegate.db

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN python -m pip install -U pip
RUN pip install -r /src/requirements.txt

RUN mkdir /logs

WORKDIR /src

CMD ["/bin/bash"]

