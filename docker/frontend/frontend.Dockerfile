FROM nginx:1.15.8
RUN apt-get update -qq && rm -rf /var/lib/apt/lists/*
RUN rm /etc/nginx/conf.d/default.conf
COPY docker/frontend/nginx.conf /etc/nginx/conf.d
WORKDIR /usr/share/nginx/html
