FROM python:3.8.5 as builder

ENV PYTHONUNBUFFERED=TRUE
WORKDIR /app
COPY . .
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN make html

FROM nginx:stable
COPY --from=builder /app/_build/html /var/www
COPY nginx/nginx.conf.template /etc/nginx/.
CMD envsubst < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'
