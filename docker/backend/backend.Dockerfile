FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements/base.txt /code/
ADD requirements/local.txt /code/
RUN pip install -r base.txt
RUN pip install -r local.txt
ADD docker/entry.sh /code/docker/entry.sh
RUN chmod +x /code/docker/entry.sh
ADD . /code/


RUN chmod gu+x /code/docker/entry.sh
CMD ["./docker/wait-for-mysql.sh", "db", "3306", "dental_password", "dentalhub_db", "--", "./docker/entry.sh"]
