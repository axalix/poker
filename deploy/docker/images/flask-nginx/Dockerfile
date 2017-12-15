FROM alpine:latest

# basic flask environment

RUN apk add --no-cache bash \
    python3 \
    python3-dev \
    build-base \
    linux-headers \
    pcre-dev \
    postgresql-dev \
    musl-dev \
    libxml2-dev \
    libxslt-dev \
    nginx \
    curl \
    supervisor && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

# install Flask an related packages
COPY requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt


# app dir
RUN mkdir /app \
	&& chown -R nginx:nginx /app \
	&& chmod 777 /run/ -R \
	&& chmod 777 /root/ -R


# copy config files into filesystem
COPY nginx.conf /etc/nginx/nginx.conf
COPY app.ini /app.ini
COPY entrypoint.sh /entrypoint.sh

# exectute start up script
ENTRYPOINT ["/entrypoint.sh"]
