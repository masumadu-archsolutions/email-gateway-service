FROM python:3.10-slim as base

FROM base as builder

RUN apt-get update && apt-get upgrade -y && apt-get install python3-dev -y && apt-get install libc-dev && apt-get install gcc -y

RUN apt-get install -y git

ARG username=username
ARG token=token
ARG repo=repo

RUN mkdir /install

WORKDIR /install

COPY requirements.txt /requirements.txt

RUN git clone https://$username:$token@$repo .

RUN pip install --prefix=/install .

RUN pip install --prefix=/install -r /requirements.txt

FROM base

ENV PYTHONDONTWRITEBYTECODE 1

COPY --from=builder /install /usr/local

COPY . /app_dir

WORKDIR /app_dir

EXPOSE 8000

CMD "./start_web.sh"
