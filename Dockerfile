FROM python:3-alpine
MAINTAINER Charlie Gildawie <charles.gildawie@gmail.com>

LABEL org.label-schema.name="dembones" \
      org.label-schema.description="Example Asyncio Web Scraper" \
      org.label-schema.vcs-url="https://github.com/TransactCharlie/dembones" \
      org.label-schema.usage="README.md" \
      org.label-schema.vcs-ref="${VCS_REF}" \
      org.label-schema.vendor="TransactCharlie" \
      org.label-schema.schema-version="1.0" \
      org.label-schema.version="${BUILD_NUMBER}"

COPY src src/
COPY tests tests/
COPY cli.py cli.py
COPY requirements.txt requirements.txt

RUN apk add --update py-pip \
 && pip3 install -r requirements.txt \
 && apk del py-pip

ENV PYTHONPATH=src
ENTRYPOINT ["python", "cli.py"]