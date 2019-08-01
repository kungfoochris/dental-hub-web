FROM python:3.6
ENV PYTHONUNBUFFERED 1
 RUN apt-get update -qq && apt-get install -y build-essential postgresql-client && rm -rf /var/lib/apt/lists/*
RUN mkdir /code
WORKDIR /code
ADD requirements/base.txt /code/
ADD requirements/local.txt /code/
RUN pip install -r base.txt
RUN pip install -r local.txt
RUN pip install -U matplotlib
ADD docker/entry.sh /code/docker/entry.sh
RUN chmod +x /code/docker/entry.sh
RUN pwd
RUN ls -al
ADD . /code/