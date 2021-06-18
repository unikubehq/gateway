
FROM quay.io/blueshoe/python3.8-slim as base

FROM base as builder

ENV PYTHONUNBUFFERED 1

RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

#
# Production container
#
FROM base
# puts binaries like uwsgi/celery in $PATH
COPY --from=builder /install /usr/local
RUN mkdir /app
COPY src/ /app
WORKDIR /app

EXPOSE 8000
COPY deployment/run_app.sh /usr/src/run_app.sh
RUN chmod +x /usr/src/run_app.sh
CMD /usr/src/run_app.sh