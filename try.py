version: '3'
services:
  db:
    image: mariadb:latest
    ports:
      - "3306:3306"
    volumes:
      - ./tmp/db:/var/lib/mysql
    environment:
      MYSQL_DATABASE: 'dental_db'
      MYSQL_USER: 'dental'
      MYSQL_PASSWORD: 'dental_password'
      MYSQL_ROOT_PASSWORD: 'dental_root_password'

  redis:
    image: "redis:alpine"

  web:
    build: 
      context: ./
      dockerfile: docker/app.Dockerfile
    volumes:
      - .:/code
    ports:
      - "3000:3000"
    command: ["./docker/entry.sh"]
    depends_on:
      - db
      - redis
    environment:
      SECRET_KEY: 'tg7703_ddewirye6t0d^mam7-=42&!k&wv5dhi$$(35kouzi3ks'
      DATABASE_ENGINE: django.db.backends.mysql
      DATABASE_HOST: db
      DATABASE_NAME: dental_db
      DATABASE_USER: dental
      DATABASE_PASSWORD: dental_root_password
      DATABASE_PORT: 3306
  celery:
    build: 
      context: ./
      dockerfile: docker/app.Dockerfile
    command: celery -A dental worker -l info
    volumes:
      - .:/code
    depends_on:
      - db
      - redis
  celery-beat:
    build: 
      context: ./
      dockerfile: docker/app.Dockerfile
    command: celery -A dental beat -l info
    volumes:
      - .:/code
    depends_on:
      - db
      - redis

