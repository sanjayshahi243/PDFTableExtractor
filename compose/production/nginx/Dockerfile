FROM nginx:latest

RUN rm /etc/nginx/conf.d/*.conf
COPY ./compose/production/nginx/nginx.conf /etc/nginx/conf.d
